from jinja2 import Environment
from django.conf import settings


class Filter:
    """A search filter"""

    def name(self):
        """Returns the name of the filter.  This isn't the display name,
        but rather the name in the database.  For ease, it makes the most
        sense to make it like a python variable, with lower case and underscores."""
        pass

    def document_value(self, document_dict):
        """Returns a value for a given document dictionary.  Most of the time, this will
        just be a value within the document, but sometimes there is extra processing
        in order to group documents for filtering.

        The dictionary provided will be permissioned for the specific user group attached
        to the cache."""
        pass

    def sort(self, names):
        """Sorts the names, which are keys for the filter.  Defaults to alphabetical."""
        names.sort(key=lambda x: (x is None, x))
        return names

    def ignored_values(self):
        """Returns a list of ignored values, which could be set if someone doesn't
        have permissions, or just in general if they want to be ignored."""
        return []

    def is_list(self):
        """If the filter provides a list of values that can be matched against,
        this should return True.  Defaults to False."""
        return False


class ExploreRanker:
    """settings.TORQUE_EXPLORE_RANK should be set to an instance of this class,
    with the method get_rank_key(self, document_dict) overloaded."""

    def get_rank_key(self, document_dict):
        """Returns the text value that should be used to sort results when browsing
        data.  Defaults to None (natural sort).  Will also not be used when a search
        query is used."""
        return None


class IncludeInSearch:
    """settings.TORQUE_INCLUDE_IN_SEARCH should be set to an instance of this class,
    with the method include(self, document_dict) overloaded."""

    def include(self, document_dict):
        """Returns whether a document_dict available in the system should be included
        in the search and explore results.  Defaults to True (include)."""
        return True


class CsvFieldProcessor:
    def field_names(self, field_name):
        pass

    def process_value(self, value):
        pass

    def default_value(self, field_name):
        return [""] * len(self.field_names(field_name))


## A factory method for getting a jinja environment
def get_jinja_env():
    enabled_extensions = []
    if getattr(settings, "TORQUE_ENABLED_JINJA_EXTENSIONS", False):
        enabled_extensions = (
            enabled_extensions + settings.TORQUE_ENABLED_JINJA_EXTENSIONS
        )

    env = Environment(extensions=enabled_extensions)

    if getattr(settings, "TORQUE_JINJA_GLOBALS", False):
        for key, value in settings.TORQUE_JINJA_GLOBALS.items():
            env.globals[key] = value

    return env


def dirty_documents(documents, wiki_config=None):
    from torque import models

    if wiki_config:
        document_dicts = models.DocumentDictCache.objects.filter(
            document__in=documents, wiki_config=wiki_config
        )
    else:
        document_dicts = models.DocumentDictCache.objects.filter(document__in=documents)

    document_dicts.update(dirty=True)
    models.TemplateCacheDocument.objects.filter(
        document_dict__in=document_dicts
    ).update(dirty=True)
