from django.conf import settings
import orjson
from django.core.cache import cache
import datetime


def convert_searchcachedocumentquery_to_memcacheids(query):
    return [
        (
            scd["collection__name"] + "||" + scd["document__key"] + "||" + scd["group"],
            scd["collection__name"],
            scd["document__key"],
            scd["group"],
        )
        for scd in query
    ]


class ExploreCache:

    def __init__(self):
        self.local_count_cache = {}
        self.cache_last_generated = None

    def build_cache(self, ids):
        from torque import models

        if not self.cache_last_generated or (
            cache.get("last_generated_time")
            and self.cache_last_generated < cache.get("last_generated_time")
        ):
            self.local_count_cache = {}
            self.cache_last_generated = datetime.datetime.now()

        cache_missed_ids = [id for id in ids if id not in self.local_count_cache]

        for r in models.SearchCacheDocument.objects.filter(
            id__in=cache_missed_ids
        ).values("id", "filtered_data"):
            rfd = r["filtered_data"]

            count_cache_object = {}
            for target_filter in getattr(settings, "TORQUE_FILTERS", []):
                target_values = rfd.get(target_filter.name(), [])
                if not target_filter.is_list() and target_values:
                    target_values = [target_values]

                count_cache_object[target_filter.name()] = {}

                for target_value in target_values:
                    count_cache_object[target_filter.name()][target_value] = True

            self.local_count_cache[r["id"]] = {
                "filtered_data": rfd,
                "counts": count_cache_object,
            }

    def build_memcache_result_cache(self, ids):
        from torque import models

        result = cache.get_many([id[0] for id in ids])
        cache_missed_ids = [id for id in ids if id[0] not in result]

        # Short circuit here if there were no misses, we don't have to do all the dancing
        if not cache_missed_ids:
            return result

        for id in cache_missed_ids:
            cache_object = {
                "collection_name": id[1],
                "document_key": id[2],
                "fields": orjson.loads(
                    models.DocumentDictCache.objects.get(
                        document__collection__name=id[1],
                        document__key=id[2],
                        wiki_config__group=id[3],
                    ).dictionary
                )["fields"],
            }
            cache.set(id[0], cache_object)
            result[id[0]] = cache_object

        return result

    def create_counts(self, ids, filters):
        self.build_cache(ids)

        filter_results = []
        torque_filters_by_name = {
            f.name(): f for f in getattr(settings, "TORQUE_FILTERS", [])
        }

        def result_filtered_data_addable(id, filters):
            for name, values in filters.items():
                if name not in torque_filters_by_name:
                    # If you're passing something that we don't even recognize, we just skip
                    continue

                if values:
                    filter_passed = False
                    for value in values:
                        try:
                            if self.local_count_cache[id]["counts"][name][value]:
                                filter_passed = True
                                break
                        except KeyError:
                            self.local_count_cache[id]["counts"][name][value] = False

                    if not filter_passed:
                        return False
            return True

        empty_filter_list = [
            self.local_count_cache[id]["filtered_data"]
            for id in ids
            if result_filtered_data_addable(id, filters)
        ]

        for filter in getattr(settings, "TORQUE_FILTERS", []):
            filters_we_care_about = {
                name: values
                for name, values in filters.items()
                if name != filter.name()
            }

            if filter.name() not in filters or not filters[filter.name()]:
                selected_objects = empty_filter_list
            else:
                selected_objects = [
                    self.local_count_cache[id]["filtered_data"]
                    for id in ids
                    if result_filtered_data_addable(id, filters_we_care_about)
                ]

            counts = {}
            for selected_object in selected_objects:
                if filter.name() in selected_object:
                    if filter.is_list():
                        for value in selected_object[filter.name()]:
                            if value not in filter.ignored_values():
                                if value not in counts:
                                    counts[value] = {"name": value, "total": 0}

                                counts[value]["total"] += 1
                    else:
                        value = selected_object[filter.name()]
                        if value not in filter.ignored_values():
                            if value not in counts:
                                counts[value] = {"name": value, "total": 0}

                            counts[value]["total"] += 1

            for value in filters.get(filter.name(), []):
                if value not in counts:
                    counts[value] = {"name": value, "total": 0}

            filter_result = {
                "name": filter.name(),
                "counts": {
                    name: counts[name] for name in filter.sort(list(counts.keys()))
                },
            }

            filter_results.append(filter_result)

        return (filter_results, len(empty_filter_list))

    def get_results(self, scds):
        from torque import models

        memcache_ids = convert_searchcachedocumentquery_to_memcacheids(scds)
        result = self.build_memcache_result_cache(memcache_ids)
        return [result[id[0]] for id in memcache_ids]


explore_cache = ExploreCache()
