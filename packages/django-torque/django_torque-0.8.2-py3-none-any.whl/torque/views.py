import json
import urllib.parse
from django.db import connection
from werkzeug.utils import secure_filename
from datetime import datetime
from django.core.files.base import ContentFile
from django.db.models import Q, F, Value
from django.http import HttpResponse, JsonResponse, FileResponse
from django.dispatch import receiver
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchHeadline
from django.conf import settings
from torque import utils
from torque import models
from torque.version import __version__
from torque.explore_cache import explore_cache
from torque.signals import search_filter

import magic
import csv
import io
import re
import xlsxwriter

jinja_env = utils.get_jinja_env()


DEFAULT_RANK_CONSTANT = 60


def execute_raw_query(sql, params):
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return results


def get_wiki(dictionary, collection_name):
    wiki_key = dictionary["wiki_key"]

    if "wiki_keys" in dictionary:
        wiki_keys = dictionary["wiki_keys"].split(",")
        collection_names = dictionary["collection_names"].split(",")
        mapping = dict(zip(collection_names, wiki_keys))

        if collection_name in mapping:
            wiki_key = mapping[collection_name]

    return models.Wiki.objects.get_or_create(wiki_key=wiki_key)[0]


def get_wiki_from_request(request, collection_name):
    return get_wiki(request.GET, collection_name)


def remove_stop_patterns(qs, stop_patterns):
    for phrase in stop_patterns:
        qs = [re.sub(phrase, "", q, flags=re.IGNORECASE).strip() for q in qs]
    return qs


def get_system_information(request, fmt):
    if fmt == "json":
        information = {}
        if getattr(settings, "TORQUE_COLLECTIONS_ALIAS", False) and getattr(
            settings, "TORQUE_DOCUMENTS_ALIAS", False
        ):
            information["collections_alias"] = settings.TORQUE_COLLECTIONS_ALIAS
            information["documents_alias"] = settings.TORQUE_DOCUMENTS_ALIAS

        information["server_version"] = __version__
        return JsonResponse(
            information,
            safe=False,
        )
    else:
        raise Exception(f"Invalid format {fmt}")

@receiver(search_filter)
def text_filter(sender, **kwargs):
    cache_documents = kwargs["cache_documents"]
    qs = kwargs.get("qs")
    include_snippets = kwargs.get("include_snippets", False)

    search_type = "websearch"

    if qs:
        search_query = SearchQuery(qs[0], search_type=search_type)
        for q in qs[1:]:
            search_query |= SearchQuery(q, search_type=search_type)
        data_vector_q = Q(data_vector=search_query)

        cache_documents = cache_documents.filter(data_vector_q).annotate(
            score=SearchRank(F("data_vector"), search_query),
        )

        if include_snippets:
            cache_documents = cache_documents.annotate(
                snippets=SearchHeadline(
                    "data",
                    search_query,
                    start_sel="",
                    stop_sel="",
                ),
            )

    return cache_documents

def search_data(
    qs,
    filters,
    wiki_configs,
    documents_limited_to,
    omit_filter_results=False,
    limit=None,
    offset=0,
    rank_constant=DEFAULT_RANK_CONSTANT,
    include_snippets=False,
):
    document_limit_or = Q()
    for collection, document in documents_limited_to:
        document_limit_or |= Q(collection__name=collection, document__key=document)

    cache_documents = models.SearchCacheDocument.objects

    wiki_config_values = list(wiki_configs.values('collection', 'wiki_id', 'group', 'id'))

    results = cache_documents.filter(
        document_limit_or,
        collection__in=[wiki_config['collection'] for wiki_config in wiki_config_values],
        wiki__in=[wiki_config['wiki_id'] for wiki_config in wiki_config_values],
        group__in=[wiki_config['group'] for wiki_config in wiki_config_values],
        wiki_config__id__in=[wiki_config['id'] for wiki_config in wiki_config_values],
    )

    searches = []

    if qs:
        stop_patterns = getattr(settings, "TORQUE_STOP_PATTERNS", [])
        qs = remove_stop_patterns(qs, stop_patterns)

        searches = [
            search
            for identity, search in search_filter.send(
                sender=None,
                cache_documents=results,
                qs=qs,
                include_snippets=include_snippets,
            )
            if search is not None
        ]

        if searches:
            results = searches[0].union(*searches[1:])

    torque_filters_by_name = {
        f.name(): f for f in getattr(settings, "TORQUE_FILTERS", [])
    }
    if not omit_filter_results:
        all_ids = list(results.values_list("id", flat=True))
        (filter_results, num_results) = explore_cache.create_counts(all_ids, filters)
    else:
        filter_results = None
        num_results = None

    additional_filters = []
    for name, values in filters.items():
        if name not in torque_filters_by_name:
            # If you're passing something that we don't even recognize, we just skip rather
            # than returning zero results
            continue

        q_objects = Q()
        if torque_filters_by_name[name].is_list():
            key = "filtered_data__%s__contains" % name
        else:
            key = "filtered_data__%s" % name
        for value in values:
            q_dict = {key: value}
            q_objects |= Q(**q_dict)
        additional_filters.append(q_objects)

    if searches:
        filtered_searches = [
            search.filter(*additional_filters).only("id").annotate(scd_id=F("id"), source=Value(source)) for source, search in enumerate(searches)
        ]

        combined_searches = filtered_searches[0].union(*filtered_searches[1:], all=True)

        sql, params = combined_searches.query.sql_with_params()

        # Using raw SQL to work around Django ORM's inability to combine union and
        # group by in a single query
        returned_results = execute_raw_query(f"""
            SELECT
                "torque_searchcachedocument"."id",
                "torque_searchcachedocument"."group",
                "torque_searchcachedocument"."document_id",
                "torque_searchcachedocument"."wiki_config_id",
                "torque_collection"."name" as "collection__name",
                "torque_document"."key" as "document__key"
                {', "results"."snippets"' if include_snippets else ''}
            FROM
            (
                SELECT
                    "id",
                    sum(1.0 / ({rank_constant} + rank)) as "rank"
                    {', array_agg(snippets) as "snippets"' if include_snippets else ''}
                FROM (
                    SELECT * FROM
                        (SELECT "scd_id" as "id",
                        DENSE_RANK() OVER (
                            PARTITION BY "source"
                            ORDER BY "score" DESC
                        ) as "rank"
                        {', DENSE_RANK() OVER (' if include_snippets else ''}
                        {'    PARTITION BY "source", "scd_id"' if include_snippets else ''}
                        {'    ORDER BY "score" DESC' if include_snippets else ''}
                        {') as "doc_rank",' if include_snippets else ''}
                        {'"snippets"' if include_snippets else ''}
                        FROM
                        ({sql}) as "results")
                    {'WHERE "doc_rank" <= 3' if include_snippets else ''}
                )
                as "results"
                GROUP BY "id"
                ORDER BY "rank" DESC
                {f'LIMIT {limit}' if limit else ''}
                {f'OFFSET {offset}' if offset else ''}
            ) as "results"
            JOIN "torque_searchcachedocument" USING ("id")
            JOIN "torque_document" ON "torque_document"."id" = "torque_searchcachedocument"."document_id"
            JOIN "torque_collection" ON "torque_collection"."id" = "torque_searchcachedocument"."collection_id"
        """, params)
    else:
        returned_results = (results.filter(*additional_filters))

        if not qs and getattr(settings, "TORQUE_EXPLORE_RANK", None):
            returned_results = returned_results.order_by("explore_rank")

        returned_results = returned_results[
            offset : None if not limit else offset + limit
        ]

        returned_results = returned_results.values(
            "id",
            "group",
            "document_id",
            "wiki_config_id",
            "collection__name",
            "document__key",
        )


    return (returned_results, filter_results, num_results, qs)


def search(
    q, filters, offset, num_per_page, template_config, wiki_configs, documents_limited_to, fmt, include_snippets
):
    # search_data requires filter values to be lists
    filters = {name: [value] for (name, value) in filters.items()}

    (returned_results, filter_results, num_results, final_qs) = search_data(
        [q],
        filters,
        wiki_configs,
        documents_limited_to,
        False,
        num_per_page,
        offset,
        DEFAULT_RANK_CONSTANT,
        include_snippets,
    )
    # While this result isn't actually mwiki text, this result is intended
    # for the mediawiki Torque extension.  Probably better to keep
    # the mwiki format than to do something like create a new "torque" format.
    # But, if we decide we need results to go to another renderer, it may
    # be worth being more clear about what we're doing here via the interface.
    #
    # This has gotten weird because the results are actually html from cached
    # results
    if fmt == "mwiki":
        template = models.Template.objects.get(
            type="Search",
            collection=template_config.collection,
            wiki=template_config.wiki,
        )

        cache_or = Q()
        for r in returned_results:
            cache_or |= Q(
                document_dict__wiki_config_id=r["wiki_config_id"],
                document_dict__document_id=r["document_id"],
            )

        mwiki_text = []

        if len(returned_results) != 0:
            cached_results = models.TemplateCacheDocument.objects.filter(
                template=template,
            ).filter(cache_or)

            for c in cached_results:
                if c.dirty or c.rendered_text == "":
                    mwiki_text.append({"text": c.to_mwiki(), "fmt": "mwiki"})
                else:
                    mwiki_text.append({"text": c.rendered_text, "fmt": "html"})

        return JsonResponse(
            {
                "num_results": num_results,
                "mwiki_text": json.dumps(mwiki_text),
                "filter_results": filter_results,
                "final_qs": final_qs,
            },
            safe=False,
        )
    elif fmt == "json":
        response = [
            {
                "uri": "/%s/%s/%s/%s"
                % (
                    getattr(settings, 'TORQUE_COLLECTIONS_ALIAS', "collections"),
                    result["collection__name"],
                    getattr(settings, 'TORQUE_DOCUMENTS_ALIAS', "documents"),
                    result["document__key"],
                ),
                "snippets": result.get("snippets", None),
            }
            for result in returned_results
        ]

        return JsonResponse(response, safe=False)
    else:
        raise Exception(f"Invalid format {fmt}")


def search_global(request, fmt):
    q = request.GET["q"]
    f = json.loads(request.GET["f"]) if "f" in request.GET and request.GET["f"] else {}
    results_limit_json = json.loads(request.body) if request.body else None
    results_limit = results_limit_json if results_limit_json else []
    offset = int(request.GET.get("offset", 0))
    num_per_page = int(request.GET.get("num_per_page", 20))
    include_snippets = bool(request.GET.get("include_snippets", False))
    group = request.GET["group"]
    global_wiki_key = request.GET["wiki_key"]
    global_collection_name = request.GET["collection_name"]
    wiki_keys = request.GET["wiki_keys"].split(",")
    collection_names = request.GET["collection_names"].split(",")
    global_config = models.WikiConfig.objects.get(
        collection__name=global_collection_name,
        wiki__wiki_key=global_wiki_key,
        group=group,
    )
    configs = models.WikiConfig.objects.filter(
        collection__name__in=collection_names, wiki__wiki_key__in=wiki_keys, group=group
    ).all()
    return search(q, f, offset, num_per_page, global_config, configs, results_limit, fmt, include_snippets)


def search_collection(request, collection_name, fmt):
    q = request.GET["q"]
    f = json.loads(request.GET["f"]) if "f" in request.GET and request.GET["f"] else {}
    results_limit_json = json.loads(request.body) if request.body else None
    results_limit = (
        [[collection_name, key] for key in results_limit_json]
        if results_limit_json
        else []
    )
    offset = int(request.GET.get("offset", 0))
    num_per_page = int(request.GET.get("num_per_page", 20))
    include_snippets = bool(request.GET.get("include_snippets", False))
    group = request.GET["group"]
    wiki = get_wiki_from_request(request, collection_name)
    configs = models.WikiConfig.objects.filter(
        collection__name=collection_name, wiki=wiki, group=group
    )
    return search(q, f, offset, num_per_page, configs.first(), configs, results_limit, fmt, include_snippets)


def explore(
    qs,
    filters,
    offset,
    num_per_page,
    template_name,
    template_config,
    wiki_configs,
    results_limit,
    filters_only=False,
    with_ids=False,
):
    (returned_results, filter_results, num_results, final_qs) = search_data(
        qs,
        filters,
        wiki_configs,
        results_limit,
        not filters_only,
        None if with_ids else num_per_page,
        None if with_ids else offset,
    )

    response = {
        "final_qs": final_qs,
        "num_results": num_results,
        "filter_results": filter_results,
    }

    if not filters_only:
        mwiki_text = ""

        result_set = explore_cache.get_results(
            returned_results[offset : (offset + num_per_page)]
            if with_ids
            else returned_results
        )
        if not num_results:
            response["num_results"] = len(result_set)

        explore_templates = models.Template.objects.filter(
            type="Explore",
            collection=template_config.collection,
        )
        if explore_templates:
            if template_name:
                template = jinja_env.from_string(
                    explore_templates.get(name=template_name).get_file_contents()
                )
            else:
                template = jinja_env.from_string(
                    explore_templates.get(is_default=True).get_file_contents()
                )
            mwiki_text += template.render(
                {
                    template_config.collection.object_data_name(): [
                        r["fields"] for r in result_set
                    ]
                }
            )
        else:
            template = jinja_env.from_string(
                models.Template.objects.get(
                    name="Search", collection=template_config.collection
                ).get_file_contents()
            )
            for result in result_set:
                mwiki_text += (
                    "<div class='result'><div class='result--actions'><div class='result--select--holder' data-collection='%s' data-document='%s'></div></div>"
                    % (
                        result["collection_name"],
                        result["document_key"],
                    )
                )
                mwiki_text += template.render(
                    {template_config.collection.object_name: result["fields"]}
                )
                mwiki_text += "</div>"
                mwiki_text += "\n\n"

        if with_ids:
            response["results"] = [
                (r["collection__name"] , r["document__key"])
                for r in returned_results
            ]
        response["mwiki_text"] = mwiki_text

    return JsonResponse(response, safe=False)


def explore_global(request):
    qs = (
        json.loads(request.GET["qs"])
        if "qs" in request.GET and request.GET["qs"]
        else []
    )
    f = json.loads(request.GET["f"]) if "f" in request.GET and request.GET["f"] else {}
    template_name = request.GET.get("template")
    results_limit_json = json.loads(request.body) if request.body else None
    results_limit = results_limit_json if results_limit_json else []
    offset = int(request.GET.get("offset", 0))
    num_per_page = int(request.GET.get("num_per_page", 100))
    group = request.GET["group"]
    global_wiki_key = request.GET["wiki_key"]
    global_collection_name = request.GET["collection_name"]
    filter_only = request.GET.get("filter_only", False)
    with_ids = request.GET.get("with_ids", False)
    wiki_keys = request.GET["wiki_keys"].split(",")
    collection_names = request.GET["collection_names"].split(",")
    global_config = models.WikiConfig.objects.get(
        collection__name=global_collection_name,
        wiki__wiki_key=global_wiki_key,
        group=group,
    )
    configs = models.WikiConfig.objects.filter(
        collection__name__in=collection_names, wiki__wiki_key__in=wiki_keys, group=group
    ).all()
    return explore(
        qs,
        f,
        offset,
        num_per_page,
        template_name,
        global_config,
        configs,
        results_limit,
        filter_only,
        with_ids,
    )


def explore_collection(request, collection_name):
    qs = (
        json.loads(request.GET["qs"])
        if "qs" in request.GET and request.GET["qs"]
        else []
    )
    results_limit_json = json.loads(request.body) if request.body else None
    results_limit = (
        [[collection_name, key] for key in results_limit_json]
        if results_limit_json
        else []
    )
    f = json.loads(request.GET["f"]) if "f" in request.GET and request.GET["f"] else {}
    template_name = request.GET.get("template")
    offset = int(request.GET.get("offset", 0))
    num_per_page = int(request.GET.get("num_per_page", 100))
    group = request.GET["group"]
    filter_only = request.GET.get("filter_only", False)
    with_ids = request.GET.get("with_ids", False)
    wiki = get_wiki_from_request(request, collection_name)
    configs = models.WikiConfig.objects.filter(
        collection__name=collection_name, wiki=wiki, group=group
    )
    return explore(
        qs,
        f,
        offset,
        num_per_page,
        template_name,
        configs.first(),
        configs,
        results_limit,
        filter_only,
        with_ids,
    )


def edit_record(collection_name, key, group, wiki, field, new_value):
    collection = models.Collection.objects.get(name=collection_name)
    document = models.Document.objects.get(collection=collection, key=key)
    wiki_config = models.WikiConfig.objects.get(
        collection=collection,
        wiki=wiki,
        group=group,
    )

    levels = field.split("||")

    if levels[0] in [field.name for field in wiki_config.valid_fields.all()]:
        value = document.values.get(field__name=levels[0])

        if len(levels) == 1:
            to_save = new_value
        else:
            to_save = value.to_python()

            inner_save = to_save
            for idx in range(1, len(levels)):
                level = levels[idx]
                if isinstance(inner_save, list):
                    level = int(level)

                if idx + 1 == len(levels):
                    inner_save[level] = new_value
                else:
                    inner_save = inner_save[level]

        value.latest = json.dumps(to_save)
        value.save()
        edit_record = models.ValueEdit(
            collection=collection,
            value=value,
            updated=json.dumps(to_save),
            message="",
            edit_timestamp=datetime.now,
            wiki=wiki,
        )
        edit_record.save()

    models.TableOfContentsCache.objects.filter(
        toc__in=collection.tables_of_contents.all()
    ).update(dirty=True)
    utils.dirty_documents([document])
    # Rebuild immediately because whoever is doing the editing probably
    # wants to see the fruits of their efforts.
    document.rebuild_cache(wiki_config)

    wiki.invalidate_linked_wiki_toc_cache()
    models.SearchCacheDocument.objects.filter(document=document).update(dirty=True)

    # This is overkill, but that's ok.  There's a bit of work to make it so
    # the individaul template cache documents have a dirty method
    collection.templates.update(dirty=True)

    collection.last_updated = datetime.now
    collection.save()


@csrf_exempt
@require_http_methods(["POST"])
def parse_for_edit(request):
    post_fields = json.loads(request.body)

    if getattr(settings, "TORQUE_EDIT_PROCESSOR", False):
        return JsonResponse(
            {"data": settings.TORQUE_EDIT_PROCESSOR(post_fields["data"])}
        )
    else:
        return JsonResponse({"data": post_fields["data"]})


def get_collections(request, fmt):
    collection_names = [x for x in request.GET["collection_names"].split(",") if x]

    return JsonResponse(collection_names, safe=False)


def get_collection(request, collection_name, fmt):
    if fmt == "json":
        response = {"name": collection_name}

        collection = models.Collection.objects.get(name=collection_name)

        if "group" in request.GET:
            group = request.GET["group"]
            wiki = get_wiki_from_request(request, collection_name)
            wiki_config = models.WikiConfig.objects.get(
                collection=collection,
                wiki=wiki,
                group=group,
            )

            response["fields"] = [
                field.name for field in wiki_config.valid_fields.all()
            ]
        elif "admin" in request.GET:
            response["fields"] = [field.name for field in collection.fields.all()]

        response["last_updated"] = collection.last_updated.isoformat()

        return JsonResponse(response)
    else:
        raise Exception(f"Invalid format {fmt}")


def get_toc(request, collection_name, toc_name, fmt):
    group = request.GET["group"]

    results_limit_json = json.loads(request.body) if request.body else None
    results_limit = results_limit_json if results_limit_json else []

    wiki = get_wiki_from_request(request, collection_name)
    collection = models.Collection.objects.get(name=collection_name)

    try:
        wiki_config = models.WikiConfig.objects.get(
            collection=collection,
            wiki=wiki,
            group=group,
        )
    except:
        return HttpResponse(status=403)

    toc = models.TableOfContents.objects.get(collection=collection, name=toc_name)

    if group == "":
        return HttpResponse(status=403)

    if fmt == "mwiki":
        return HttpResponse(toc.render_to_mwiki(wiki_config, results_limit))
    elif fmt == "html":
        if not results_limit:
            cached_toc = wiki_config.cached_tocs.get(toc=toc)
            if cached_toc.dirty:
                cached_toc.rebuild()
            return HttpResponse(cached_toc.rendered_html)
        else:
            return HttpResponse()
    else:
        raise Exception(f"Invalid format {fmt}")


def get_documents(request, collection_name, fmt):
    collection = models.Collection.objects.get(name=collection_name)
    group = request.GET.get("group")
    admin = request.GET.get("admin")
    wiki = get_wiki_from_request(request, collection_name)

    if fmt == "json":
        if group:
            wiki_config = models.WikiConfig.objects.get(
                collection=collection,
                wiki=wiki,
                group=group,
            )
            return JsonResponse(
                [document.key for document in wiki_config.valid_ids.all()], safe=False
            )
        elif admin:
            return JsonResponse(
                [document.key for document in collection.documents.all()], safe=False
            )
    else:
        raise Exception(f"Invalid format {fmt}")


def get_document(group, admin, wiki, key, version, fmt, collection_name, view=None):
    collection = models.Collection.objects.get(name=collection_name)

    wiki_config = None
    if group or not admin:
        wiki_config = models.WikiConfig.objects.get(
            collection=collection,
            wiki=wiki,
            group=group,
        )

        document = wiki_config.valid_ids.get(key=key, collection=collection).to_dict(
            wiki_config, version
        )["fields"]
    # We only allow admin style access to documents when using them from a data/api
    # point of view, just to be extra sure that normal wiki viewership remains group
    # based from both a permissions point of view, but also from a cache one
    elif admin and fmt in ["json", "dict"]:
        document = collection.documents.get(key=key).to_dict(None, version)["fields"]

    if fmt == "json":
        return JsonResponse(document)
    elif fmt == "dict":
        return document

    templates = models.Template.objects.filter(
        collection=collection,
        wiki=wiki,
        type="View",
    )

    if view is not None:
        try:
            view_object = json.loads(view)

            view_wiki = models.Wiki.objects.get(wiki_key=view_object["wiki_key"])
            view = view_object["view"]
            template = models.Template.objects.get(
                wiki=view_wiki, type="View", name=view
            )
        except json.JSONDecodeError:
            template = templates.get(name=view)
    else:
        template = templates.get(is_default=True)

    if fmt == "mwiki":
        rendered_template = jinja_env.from_string(template.get_file_contents()).render(
            {collection.object_name: document}
        )
        return HttpResponse(rendered_template)
    elif fmt == "html":
        try:
            ddc = models.DocumentDictCache.objects.get(
                wiki_config=wiki_config,
                document=wiki_config.valid_ids.get(key=key, collection=collection),
            )
            cache = models.TemplateCacheDocument.objects.get(
                template=template, document_dict=ddc
            )
            if cache.dirty:
                cache.rebuild()
            return HttpResponse(cache.rendered_text)
        except models.TemplateCacheDocument.DoesNotExist:
            return HttpResponse("")
    else:
        raise Exception(f"Invalid format {fmt}")


def get_document_view(request, collection_name, key, fmt, version="latest"):
    group = request.GET.get("group")
    admin = request.GET.get("admin")
    wiki = get_wiki_from_request(request, collection_name)

    return get_document(
        group,
        admin,
        wiki,
        key,
        version,
        fmt,
        collection_name,
        request.GET.get("view", None),
    )


def field(request, collection_name, key, field, fmt):
    field = urllib.parse.unquote_plus(field)
    if request.method == "GET":
        group = request.GET.get("group")
        admin = request.GET.get("admin")
        wiki = get_wiki_from_request(request, collection_name)
        document = get_document(
            group, admin, wiki, key, None, "dict", collection_name, None
        )

        value = document
        for level in field.split("||"):
            if isinstance(value, list):
                level = int(level)

            value = value[level]

        return JsonResponse(value, safe=False)
    elif request.method == "POST":
        post_fields = json.loads(request.body)
        group = post_fields["group"]
        wiki = get_wiki(post_fields, collection_name)
        new_value = post_fields["new_value"]
        edit_record(collection_name, key, group, wiki, field, new_value)
        return HttpResponse(201)


def get_attachments(request, collection_name, key, fmt):
    group = request.GET.get("group")
    admin = request.GET.get("admin")
    wiki = get_wiki_from_request(request, collection_name)

    attachments = []
    collection = models.Collection.objects.get(name=collection_name)
    document = collection.documents.get(key=key)

    if group:
        wiki_config = models.WikiConfig.objects.get(
            collection=collection,
            wiki=wiki,
            group=group,
        )
        attachments = []

        for potential_attachment in models.Attachment.objects.filter(document=document):
            if wiki_config.valid_fields.filter(
                id=potential_attachment.permissions_field.id
            ).exists():
                attachments.append(potential_attachment)
    elif admin:
        attachments = models.Attachment.objects.filter(document=document)

    if fmt == "json":
        return JsonResponse(
            [
                {
                    "name": a.name,
                    "size": a.file.size,
                }
                for a in attachments
            ],
            safe=False,
        )
    else:
        raise Exception(f"Invalid format {fmt}")


def get_attachment(request, collection_name, key, attachment):
    group = request.GET.get("group")
    admin = request.GET.get("admin")
    wiki = get_wiki_from_request(request, collection_name)
    attachment_name = secure_filename(urllib.parse.unquote_plus(attachment))

    collection = models.Collection.objects.get(name=collection_name)
    document = collection.documents.get(key=key)
    attachment = models.Attachment.objects.get(name=attachment_name, document=document)

    if group or not admin:
        wiki_config = models.WikiConfig.objects.get(
            collection=collection,
            wiki=wiki,
            group=group,
        )
        if not wiki_config.valid_fields.filter(
            id=attachment.permissions_field.id
        ).exists():
            raise Exception("Not permitted to see this attachment.")

    content_type = magic.from_buffer(attachment.file.open("rb").read(1024), mime=True)
    return FileResponse(
        attachment.file.open("rb"), filename=attachment_name, content_type=content_type
    )


def reset_config(request, collection_name, wiki_key):
    wiki = models.Wiki.objects.get_or_create(wiki_key=wiki_key)[0]
    wiki.username = None
    wiki.password = None
    wiki.script_path = None
    wiki.server = None
    wiki.linked_wiki_keys = list()
    wiki.save()

    models.WikiConfig.objects.filter(
        collection__name=collection_name, wiki=wiki
    ).update(in_config=False)

    models.Template.objects.filter(collection__name=collection_name, wiki=wiki).update(
        in_config=False
    )

    return HttpResponse(status=200)


@csrf_exempt
@require_http_methods(["POST"])
# Even though collection_name isn't user here, we add it so that the urls
# all nicely line up with the other config requests
def set_wiki_config(request, collection_name, wiki_key):
    wiki = models.Wiki.objects.get_or_create(wiki_key=wiki_key)[0]
    wiki_config = json.loads(request.body)
    wiki.username = wiki_config["username"]
    wiki.password = wiki_config["password"]
    wiki.script_path = wiki_config["script_path"]
    wiki.server = wiki_config["server"]
    wiki.linked_wiki_keys = wiki_config["linked_wiki_keys"]
    wiki.save()

    return HttpResponse(status=200)


@csrf_exempt
@require_http_methods(["POST"])
def set_group_config(request, collection_name, wiki_key):
    import hashlib

    new_config = json.loads(request.body)
    collection = models.Collection.objects.get(name=collection_name)
    wiki = models.Wiki.objects.get(wiki_key=wiki_key)

    try:
        config = models.WikiConfig.objects.get(
            collection=collection, wiki=wiki, group=new_config["group"]
        )
    except models.WikiConfig.DoesNotExist:
        config = None

    permissions_sha = hashlib.sha224(
        collection_name.encode("utf-8")
        + str(new_config.get("valid_ids")).encode("utf-8")
        + str(new_config.get("fields")).encode("utf-8")
    ).hexdigest()

    if config is None or permissions_sha != config.search_cache_sha:
        if config is not None:
            config.valid_ids.clear()
            config.valid_fields.clear()
        else:
            config = models.WikiConfig(
                collection=collection, wiki=wiki, group=new_config["group"]
            )
            config.save()

        for toc in collection.tables_of_contents.all():
            (cache, created) = models.TableOfContentsCache.objects.update_or_create(
                toc=toc, wiki_config=config
            )
            cache.dirty = True
            cache.save()

        config.search_cache_sha = permissions_sha

        valid_documents = models.Document.objects.filter(
            collection=collection, key__in=new_config.get("valid_ids")
        )
        valid_fields = models.Field.objects.filter(
            name__in=new_config.get("fields"), collection=collection
        )
        config.save()
        config.valid_ids.add(*valid_documents)
        config.valid_fields.add(*valid_fields)
        config.cache_dirty = True
        utils.dirty_documents(config.valid_ids.all(), config)

        for linked_wiki in models.Wiki.objects.filter(
            linked_wiki_keys__contains=[wiki_key]
        ):
            try:
                linked_wiki_config = models.WikiConfig.objects.get(
                    wiki=linked_wiki, group=config.group
                )
                models.TableOfContentsCache.objects.filter(
                    wiki_config=linked_wiki_config
                ).update(dirty=True)
            except models.WikiConfig.DoesNotExist:
                # If there's no proper config, do nothing
                pass

    config.in_config = True
    config.save()

    return HttpResponse(status=200)


def complete_config(request, collection_name, wiki_key):
    models.WikiConfig.objects.filter(
        collection__name=collection_name, wiki__wiki_key=wiki_key, in_config=False
    ).delete()
    models.Template.objects.filter(
        collection__name=collection_name, wiki__wiki_key=wiki_key, in_config=False
    ).delete()

    return HttpResponse(status=200)


@csrf_exempt
@require_http_methods(["POST"])
def set_template_config(request, collection_name, wiki_key):
    new_config = json.loads(request.body)

    conf_name = new_config["name"]
    conf_type = new_config["type"]
    default = new_config["default"]

    collection = models.Collection.objects.get(name=collection_name)
    wiki = models.Wiki.objects.get(wiki_key=wiki_key)
    template = models.Template.objects.get_or_create(
        collection=collection, wiki=wiki, type=conf_type, name=conf_name
    )[0]

    if template.get_file_contents() != new_config["template"]:
        template.template_file.save(
            f"{wiki_key}-{conf_name}", ContentFile(new_config["template"])
        )
        template.dirty = True

    template.in_config = True
    template.is_default = default
    template.save()

    return HttpResponse(status=200)


@csrf_exempt
@require_http_methods(["POST"])
def upload_collection(request):
    with request.FILES["data_file"].open(mode="rt") as f:
        collection, documents = models.Collection.from_json(
            name=request.POST["collection_name"],
            object_name=request.POST["object_name"],
            key_field=request.POST["key_field"],
            file=f,
        )
    collection.save()
    collection.templates.update(dirty=True)

    # Regenerate search caches in case data has changed.  We assume that the
    # cache is invalid, making uploading a collection be a very expensive operation,
    # but that's probably better than attempting to analyze cache invalidation
    # and failing.

    for config in models.WikiConfig.objects.filter(collection=collection):
        config.cache_dirty = True
        config.save()

    for wiki in models.Wiki.objects.filter(configs__collection=collection):
        wiki.invalidate_linked_wiki_toc_cache()

    return HttpResponse(status=200)


@csrf_exempt
@require_http_methods(["POST"])
def upload_toc(request):
    collection = models.Collection.objects.get(name=request.POST["collection_name"])
    (template, created) = models.Template.objects.update_or_create(
        collection=collection,
        type="uploaded_template",
        name=request.POST["toc_name"],
    )
    template.template_file = request.FILES["template"]
    template.save()
    json_file = request.FILES["json"].read().decode("utf-8")
    (toc, created) = models.TableOfContents.objects.update_or_create(
        collection=collection,
        name=request.POST["toc_name"],
        defaults={
            "json_file": json_file,
            "template": template,
        },
    )
    # Have to repeat this because we need to have it when we create, if
    # we do create (above), but we also need to set it in the case that
    # the TOC already exists in the database
    toc.json_file = json_file
    toc.template = template
    toc.raw = bool(request.POST["raw"])
    toc.save()

    for config in collection.configs.all():
        (cache, created) = models.TableOfContentsCache.objects.update_or_create(
            toc=toc,
            wiki_config=config,
        )
        cache.dirty = True
        cache.save()

    return HttpResponse(status=200)


@csrf_exempt
@require_http_methods(["POST"])
def upload_attachment(request):
    collection = models.Collection.objects.get(name=request.POST["collection_name"])
    permissions_field = models.Field.objects.get(
        collection=collection, name=request.POST["permissions_field"]
    )
    document = collection.documents.get(key=request.POST["object_id"])

    # Can't use update_or_create here because permissions field is not part
    # of the unique key (collection, name, document), but also not nullable,
    # so we have to manually do the update or create.
    try:
        attachment = models.Attachment.objects.get(
            collection=collection,
            name=secure_filename(request.POST["attachment_name"]),
            document=document,
        )
        attachment.permissions_field = permissions_field
    except models.Attachment.DoesNotExist:
        attachment = models.Attachment.objects.create(
            collection=collection,
            name=secure_filename(request.POST["attachment_name"]),
            document=document,
            permissions_field=permissions_field,
        )

    attachment.file = request.FILES["attachment"]
    attachment.save()

    return HttpResponse(status=200)


def user_by_username(request, username):
    # create user if doesn't exist
    try:
        user = models.User.objects.get(username=username)
    except models.User.DoesNotExist:
        user = models.User(username=username)
        user.save()

    return JsonResponse({"username": user.username, "id": user.pk})


@csrf_exempt
@require_http_methods(["POST"])
def add_spreadsheet(request):
    def determine_name():
        import string
        import random

        characters = string.ascii_lowercase + string.ascii_uppercase + string.digits
        possible_name = "".join([random.choice(characters) for i in range(6)])
        if (
            models.SpreadsheetSpecification.objects.filter(name=possible_name).count()
            > 0
        ):
            return determine_name()
        else:
            return possible_name

    name = determine_name()
    post_fields = json.loads(request.body)

    massive_or = Q()
    for post_doc in post_fields["documents"]:
        massive_or |= Q(collection__name=post_doc[0], key=post_doc[1])

    documents = models.Document.objects.filter(massive_or)

    spreadsheet_spec = models.SpreadsheetSpecification(
        name=name, filename=post_fields["filename"], fields=post_fields["fields"]
    )
    # Save first so the many to many below works correctly
    spreadsheet_spec.save()
    spreadsheet_spec.documents.set(documents)
    spreadsheet_spec.save()
    return JsonResponse(
        {
            "name": name,
        }
    )


def get_spreadsheet(request, name, fmt):
    spreadsheet_spec = models.SpreadsheetSpecification.objects.get(name=name)

    group = request.GET["group"]

    valid_documents = spreadsheet_spec.documents.filter(
        wiki_config__group=group
    ).prefetch_related("collection")

    if fmt == "json":
        document_information = {}
        for document in valid_documents:
            if document.collection.name not in document_information:
                document_information[document.collection.name] = []
            document_information[document.collection.name].append(document.key)
        return JsonResponse(
            {
                "name": name,
                "filename": spreadsheet_spec.filename,
                "fields": spreadsheet_spec.fields,
                "documents": document_information,
            }
        )
    elif fmt in ["xlsx", "csv"]:

        def add_csv_header(spreadSheetWriter, columns):
            spreadSheetWriter.writerow(columns)

        def add_xlsx_header(spreadSheetWriter, columns):
            spreadSheetWriter.write_row(0, 0, [str(item) for item in columns])
            header_row_format = workbook.add_format({"bold": True})
            spreadSheetWriter.set_row(0, None, header_row_format)

        def add_csv_row(spreadSheetWriter, row):
            spreadSheetWriter.writerow(row)

        def add_xlsx_row(spreadSheetWriter, row):
            if not hasattr(add_xlsx_row, "cnt"):
                add_xlsx_row.cnt = 1
            cnt = add_xlsx_row.cnt
            spreadSheetWriter.write_row(
                "A{}".format(cnt + 1), [str(element) for element in row]
            )
            add_xlsx_row.cnt += 1

        def write_spreadsheet(add_header, add_row, spreadSheetWriter):
            spreadsheet_field_names = spreadsheet_spec.fields

            wiki_configs_for_spreadsheet = models.WikiConfig.objects.filter(
                group=group, valid_ids__in=spreadsheet_spec.documents.all()
            ).distinct()

            valid_field_names = [
                field.name
                for field in models.Field.objects.filter(
                    wiki_config__in=wiki_configs_for_spreadsheet
                ).distinct()
            ]

            field_names = [
                fn for fn in spreadsheet_field_names if fn in valid_field_names
            ]

            columns = []
            for field_name in field_names:
                if field_name in getattr(settings, "TORQUE_CSV_PROCESSORS", {}):
                    columns.extend(
                        settings.TORQUE_CSV_PROCESSORS[field_name].field_names(
                            field_name
                        )
                    )
                else:
                    columns.append(field_name)

            add_header(spreadSheetWriter, columns)

            all_pertinent_values = (
                models.Value.objects.filter(
                    field__name__in=field_names, document__in=valid_documents
                )
                .prefetch_related("field")
                .prefetch_related("document")
            )

            values_by_documents_and_fields = {}

            for value in all_pertinent_values:
                if value.document not in values_by_documents_and_fields:
                    values_by_documents_and_fields[value.document] = {}
                values_by_documents_and_fields[value.document][value.field.name] = value

            for document in valid_documents:
                row = []
                values_by_field = values_by_documents_and_fields[document]
                for field_name in field_names:
                    python_value = None
                    if field_name in values_by_field:
                        python_value = values_by_field[field_name].to_python()
                    if python_value and field_name in getattr(
                        settings, "TORQUE_CSV_PROCESSORS", {}
                    ):
                        row.extend(
                            settings.TORQUE_CSV_PROCESSORS[field_name].process_value(
                                python_value
                            )
                        )
                    elif field_name in getattr(settings, "TORQUE_CSV_PROCESSORS", {}):
                        row.extend(
                            settings.TORQUE_CSV_PROCESSORS[field_name].default_value(
                                field_name
                            )
                        )
                    elif python_value:
                        row.append(python_value)
                    else:
                        row.append("")
                add_row(spreadSheetWriter, row)

        filename = f'{spreadsheet_spec.filename}'
        if not filename.lower().endswith(fmt):
            filename = f'{spreadsheet_spec.filename}.{fmt}'

        response = HttpResponse(
            content_type=('text/csv' if fmt == 'csv' else 'application/vnd.ms-excel'),
            headers={
                "Content-Disposition": (
                    f'attachment; filename="{filename}"'
                )
            },
        )


        if fmt == "csv":
            writer = csv.writer(response)
            write_spreadsheet(add_csv_header,add_csv_row,writer)
            return response
        elif fmt == "xlsx":
            workbook = xlsxwriter.Workbook(response)
            writer = workbook.add_worksheet()
            write_spreadsheet(add_xlsx_header,add_xlsx_row,writer)
            workbook.close()
            return response
        else:
            raise Exception(f"Invalid format {fmt}")
    else:
        raise Exception(f"Invalid format {fmt}")
