import time
from multiprocessing import Process
from django.db import transaction
from django import db
import sys
from django.contrib.postgres.search import SearchVector
import traceback
from django.core.cache import cache
from torque.explore_cache import (
    explore_cache,
    convert_searchcachedocumentquery_to_memcacheids,
)
from torque.signals import update_cache_document
import datetime
from django.conf import settings


class RebuildWikiConfigs:
    def run(self):
        from torque import models

        config = models.WikiConfig.objects.filter(cache_dirty=True).first()
        if config:
            # We do this outside of the transaction, because if someone comes
            # along and dirties it again while we're rebuilding, we want to
            # rebuild it after we're done rebuilding it.
            config.cache_dirty = False
            config.save()

            print(
                "Populating unbuilt template caches for %s in %s"
                % (config.group, config.wiki.wiki_key)
            )
            for view_template in models.Template.objects.filter(
                type="View", wiki=config.wiki
            ):
                config.populate_template_cache(view_template)

            for search_template in models.Template.objects.filter(
                type="Search", wiki=config.wiki
            ):
                config.populate_template_cache(search_template, True)

            print(
                "Rebuilding search index for %s: %s"
                % (config.wiki.wiki_key, config.group)
            )
            cache.delete_many(
                [
                    id[0]
                    for id in convert_searchcachedocumentquery_to_memcacheids(
                        models.SearchCacheDocument.objects.filter(wiki_config=config).values(
                            "id",
                            "group",
                            "document_id",
                            "wiki_config_id",
                            "collection__name",
                            "document__key",
                        )
                    )
                ]
            )
            with transaction.atomic():
                config.rebuild_search_index()
            cache.set("last_generated_time", datetime.datetime.now())

            return True


class PropagateTemplateDirty:
    """When a template gets dirty, we need to update all the caches that depend on it"""

    def run(self):
        from torque import models

        for template in models.Template.objects.filter(dirty=True).all():
            template.dirty = False
            template.save()

            models.TemplateCacheDocument.objects.filter(template=template).update(
                dirty=True
            )

            if template.type == "TOC":
                models.TableOfContentsCache.objects.filter(
                    toc__in=template.collection.tables_of_contents.all()
                ).update(dirty=True)


class RebuildTOCs:
    def run(self):
        from torque import models

        toc_cache = models.TableOfContentsCache.objects.filter(dirty=True).first()
        if toc_cache:
            # As above, we do this outside of the transaction, because if someone comes
            # along and dirties it again while we're rebuilding, we want to
            # rebuild it after we're done rebuilding it.
            print(
                "Rebuilding toc %s (%s): %s..."
                % (
                    toc_cache.toc.collection.name,
                    toc_cache.wiki_config.group,
                    toc_cache.toc.name,
                ),
                end="",
            )
            toc_cache.dirty = False
            toc_cache.save()
            with transaction.atomic():
                toc_cache.rebuild()
            print("Rebuilt")
            return True


class RebuildSearchCacheDocuments:
    def run(self):
        from torque import models

        num = models.SearchCacheDocument.objects.filter(dirty=True).count()
        if num > 0:
            print("Rebuilding %s search cache documents" % num)
        else:
            return False

        cache.delete_many(
            [
                id[0]
                for id in convert_searchcachedocumentquery_to_memcacheids(
                    models.SearchCacheDocument.objects.filter(dirty=True).values(
                        "id",
                        "group",
                        "document_id",
                        "wiki_config_id",
                        "collection__name",
                        "document__key",
                    )
                )
            ]
        )

        for dirty_cache_document in models.SearchCacheDocument.objects.filter(dirty=True):
            # It's possible that the logic below (going over sibling SCDs) updated
            # this document, in which case we can go ahead and move on.
            dirty_cache_document.refresh_from_db()
            if not dirty_cache_document.dirty:
                continue

            # If a search cache document got dirtied, it was probably due to an edit
            # which affects only a single SCD.  However, it's most likely true that
            # all the SCDs that operate on the same document should be dirty as well.
            # So we iterate over all of them!
            for cache_document_to_update in models.SearchCacheDocument.objects.filter(document=dirty_cache_document.document):
                document_dict = cache_document_to_update.document.to_dict(cache_document_to_update.wiki_config, None)
                cache_document_to_update.data = " ".join(list(map(str, document_dict.values())))

                filtered_data = {}
                for filter in getattr(settings, "TORQUE_FILTERS", []):
                    filtered_data[filter.name()] = filter.document_value(
                        document_dict["fields"]
                    )
                cache_document_to_update.filtered_data = filtered_data

                cache_document_to_update.dirty = False
                cache_document_to_update.save()
                models.SearchCacheDocument.objects.filter(id=cache_document_to_update.id).update(
                    data_vector=SearchVector("data")
                )

                update_cache_document.send(
                    sender=self.__class__,
                    cache_document=cache_document_to_update,
                    filtered_data=filtered_data,
                    document_dict=document_dict["fields"]
                )


        cache.set("last_generated_time", datetime.datetime.now())
        return True


class RebuildTemplateCacheDocuments:
    def run(self):
        from torque import models

        template_cache = models.TemplateCacheDocument.objects.filter(dirty=True).first()
        if template_cache:
            print(
                "Rebuilding template cache for (%s: %s), %s left"
                % (
                    template_cache.document_dict.wiki_config.wiki.wiki_key,
                    template_cache.document_dict.document.key,
                    models.TemplateCacheDocument.objects.filter(dirty=True).count(),
                )
            )

            for tc in models.TemplateCacheDocument.objects.filter(
                document_dict=template_cache.document_dict, dirty=True
            ):
                template_cache.rebuild()

            return True


class CreateUnbuiltDocumentDicts:
    def run(self):
        from torque import models

        for wiki_config in models.WikiConfig.objects.all():
            if (
                wiki_config.valid_ids.count()
                != models.DocumentDictCache.objects.filter(
                    document__in=wiki_config.valid_ids.all(), wiki_config=wiki_config
                ).count()
            ):
                print(
                    "Add unbuilt document dictionaries for %s in %s"
                    % (wiki_config.group, wiki_config.wiki.wiki_key)
                )
                wiki_config.rebuild_document_dict_cache()
                return True


class RegenerateMemcacheDocumentCache:
    def __init__(self):
        self.cache_last_generated = None

    def run(self):
        from torque import models

        if self.cache_last_generated and (
            not cache.get("last_generated_time")
            or self.cache_last_generated > cache.get("last_generated_time")
        ):
            return False

        self.local_count_cache = {}
        self.cache_last_generated = datetime.datetime.now()
        print("Rebuilding memcache")

        memcache_ids = convert_searchcachedocumentquery_to_memcacheids(
            models.SearchCacheDocument.objects.values(
                "id",
                "group",
                "document_id",
                "wiki_config_id",
                "collection__name",
                "document__key",
            )
        )
        result = explore_cache.build_memcache_result_cache(memcache_ids)

        if not result:
            return True


class RebuildDocumentDicts:
    def run(self):
        from torque import models

        ddcs = models.DocumentDictCache.objects.filter(dirty=True).all()
        if len(ddcs) > 0:
            print("Rebuilding %s Document Dicts" % len(ddcs))
            for ddc in ddcs:
                ddc.document.rebuild_cache(ddc.wiki_config)
            return True


class CacheRebuilder(Process):
    def __init__(self):
        super().__init__()
        self.daemon = True

    def run(self):
        db.connections.close_all()

        memcache_rebuilder = RegenerateMemcacheDocumentCache()

        while True:
            try:
                # We always want to do the dictionary caches if they exist,
                # and for the rest of the caches, they shouldn't do very many just
                # in case there's new document dict cache invalidation that's happened
                (
                    CreateUnbuiltDocumentDicts().run()
                    or RebuildDocumentDicts().run()
                    or memcache_rebuilder.run()
                    or PropagateTemplateDirty().run()
                    or RebuildWikiConfigs().run()
                    or RebuildSearchCacheDocuments().run()
                    or RebuildTOCs().run()
                    or RebuildTemplateCacheDocuments().run()
                    or time.sleep(5)
                )
            except KeyboardInterrupt:
                return
            except:
                print("Rebuilder failed a loop due to %s" % sys.exc_info()[0])
                print(traceback.format_exc())
