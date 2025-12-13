import json
from contextlib import contextmanager
from unittest.mock import patch

import pytest
from torque import models
from torque.views import explore, remove_stop_patterns, search, search_data


def build_search_index(wiki_configs):
    """Helper function to build search index for given wiki configs."""
    for wiki_config in wiki_configs:
        wiki_config.rebuild_document_dict_cache()
        wiki_config.rebuild_search_index()


def create_value(document, field, content):
    """Helper function to create a Value object."""
    return models.Value.objects.create(
        document=document,
        field=field,
        latest=json.dumps({field.name: content}),
    )


@contextmanager
def mock_template_content(return_value):
    """Context manager for patching Template.get_file_contents."""
    with patch.object(
        models.Template, "get_file_contents", return_value=return_value
    ) as mock:
        yield mock


@pytest.mark.django_db(transaction=True)
def test_search_data(wiki_test_setup):
    wiki_config = wiki_test_setup["wiki_configs"][0]
    field = wiki_test_setup["fields"][0]
    docs = wiki_test_setup["docs"]

    wiki_configs = models.WikiConfig.objects.filter(id=wiki_config.id)

    create_value(docs[0], field, "test")
    create_value(docs[1], field, "wheee")
    build_search_index([wiki_config])

    returned_results, filter_results, num_results = search_data(
        qs=[],
        filters={},
        wiki_configs=wiki_configs,
        documents_limited_to=[],
    )

    assert len(returned_results) == 2
    assert num_results == 2


@pytest.mark.django_db(transaction=True)
def test_search_data_with_qs(wiki_test_setup):
    wiki_config = wiki_test_setup["wiki_configs"][0]
    field = wiki_test_setup["fields"][0]
    docs = wiki_test_setup["docs"]

    wiki_configs = models.WikiConfig.objects.filter(id=wiki_config.id)

    create_value(docs[0], field, "test")
    create_value(docs[1], field, "wheee")
    build_search_index([wiki_config])

    returned_results, filter_results, num_results = search_data(
        qs=["test"],
        filters={},
        wiki_configs=wiki_configs,
        documents_limited_to=[],
    )

    assert len(returned_results) == 1
    assert num_results == 1

@pytest.mark.django_db(transaction=True)
def test_search_data_with_stop_phrases(wiki_test_setup, use_stop_patterns):
    wiki_config = wiki_test_setup["wiki_configs"][0]
    field = wiki_test_setup["fields"][0]
    docs = wiki_test_setup["docs"]

    wiki_configs = models.WikiConfig.objects.filter(id=wiki_config.id)

    create_value(docs[0], field, "test")
    create_value(docs[1], field, "proposals")
    build_search_index([wiki_config])

    returned_results, filter_results, num_results = search_data(
        qs=["can you find me proposals related to test"],
        filters={},
        wiki_configs=wiki_configs,
        documents_limited_to=[],
    )

    assert len(returned_results) == 1
    assert num_results == 1
    assert returned_results[0]['document__key'] == docs[0].key


@pytest.mark.django_db(transaction=True)
def test_search_data_with_snippets(wiki_test_setup):
    wiki_config = wiki_test_setup["wiki_configs"][0]
    field = wiki_test_setup["fields"][0]
    docs = wiki_test_setup["docs"]

    wiki_configs = models.WikiConfig.objects.filter(id=wiki_config.id)

    create_value(
        docs[0],
        field,
        "This is a test document. It is only a test. Please do not adjust your television set. Please stand by.",
    )
    create_value(docs[1], field, "wheee")
    build_search_index([wiki_config])

    returned_results, filter_results, num_results = search_data(
        qs=["document"],
        filters={},
        wiki_configs=wiki_configs,
        documents_limited_to=[],
        include_snippets=True,
    )

    assert "snippets" in returned_results[0]
    assert returned_results[0]["snippets"] == [
        "document. It is only a test. Please do not adjust your television set. Please stand"
    ]


@pytest.mark.django_db(transaction=True)
def test_search_data_with_documents_limited_to(wiki_test_setup):
    collection = wiki_test_setup["collections"][0]
    wiki_config = wiki_test_setup["wiki_configs"][0]
    field = wiki_test_setup["fields"][0]
    docs = wiki_test_setup["docs"]

    wiki_configs = models.WikiConfig.objects.filter(id=wiki_config.id)

    create_value(docs[0], field, "test")
    create_value(docs[1], field, "wheee")
    build_search_index([wiki_config])

    returned_results, filter_results, num_results = search_data(
        qs=[],
        filters={},
        wiki_configs=wiki_configs,
        documents_limited_to=[(collection.name, docs[0].key)],
    )

    assert len(returned_results) == 1
    assert returned_results[0]["document__key"] == docs[0].key
    assert num_results == 1


@pytest.mark.django_db(transaction=True)
def test_search_data_with_documents_limited_to_and_qs(wiki_test_setup):
    collection = wiki_test_setup["collections"][0]
    wiki_config = wiki_test_setup["wiki_configs"][0]
    field = wiki_test_setup["fields"][0]
    docs = wiki_test_setup["docs"]

    wiki_configs = models.WikiConfig.objects.filter(id=wiki_config.id)

    create_value(docs[0], field, "test")
    create_value(docs[1], field, "wheee")
    build_search_index([wiki_config])

    returned_results, filter_results, num_results = search_data(
        qs=["test", "wheee"],
        filters={},
        wiki_configs=wiki_configs,
        documents_limited_to=[(collection.name, docs[0].key)],
    )

    assert len(returned_results) == 1
    assert returned_results[0]["document__key"] == docs[0].key
    assert num_results == 1


@pytest.mark.django_db(transaction=True)
def test_search_with_search_template_num_per_page_and_json_format(wiki_test_setup):
    wiki_config = wiki_test_setup["wiki_configs"][0]
    field = wiki_test_setup["fields"][0]
    docs = wiki_test_setup["docs"]

    wiki_configs = models.WikiConfig.objects.filter(id=wiki_config.id)

    create_value(docs[0], field, "test")
    create_value(docs[1], field, "test")
    build_search_index([wiki_config])

    response = search(
        q="test",
        filters={},
        offset=0,
        num_per_page=1,
        template_config=wiki_config,
        wiki_configs=wiki_configs,
        documents_limited_to=[],
        fmt="json",
        include_snippets=True,
    )

    assert response.status_code == 200
    results_list = json.loads(response.content)
    assert len(results_list) == 1
    assert "snippets" in results_list[0]


@pytest.mark.django_db(transaction=True)
def test_search_with_search_template_num_per_page_and_mwiki_format(wiki_test_setup):
    template = wiki_test_setup["templates"][0]
    wiki_config = wiki_test_setup["wiki_configs"][0]
    field = wiki_test_setup["fields"][0]
    docs = wiki_test_setup["docs"]

    wiki_configs = models.WikiConfig.objects.filter(id=wiki_config.id)

    create_value(docs[0], field, "test")
    create_value(docs[1], field, "test")
    build_search_index([wiki_config])
    wiki_config.populate_template_cache(template=template)

    with mock_template_content(
        "{% for key, value in test_object_1.items() %}{{ key }}: {{ value[key] }}\n{% endfor %}"
    ):
        response = search(
            q="test",
            filters={},
            offset=0,
            num_per_page=1,
            template_config=wiki_config,
            wiki_configs=wiki_configs,
            documents_limited_to=[],
            fmt="mwiki",
            include_snippets=False,
        )

    assert response.status_code == 200
    response_data = json.loads(response.content)
    total_results = response_data[  # not just the number returned in this context
        "num_results"
    ]
    assert total_results == 2
    assert "mwiki_text" in response_data
    result_list = json.loads(response_data["mwiki_text"])
    assert len(result_list) == 1


@pytest.mark.django_db(transaction=True)
def test_explore_with_filters_only(wiki_test_setup):
    wiki_config = wiki_test_setup["wiki_configs"][0]
    field = wiki_test_setup["fields"][0]
    docs = wiki_test_setup["docs"]

    wiki_configs = models.WikiConfig.objects.filter(id=wiki_config.id)

    create_value(docs[0], field, "test")
    create_value(docs[1], field, "wheee")
    build_search_index([wiki_config])

    response = explore(
        qs=[],
        filters={},
        offset=0,
        num_per_page=1,
        template_name=None,
        template_config=wiki_config,
        wiki_configs=wiki_configs,
        results_limit=[],
        filters_only=True,
    )

    assert response.status_code == 200
    response_data = json.loads(response.content)
    assert "results" not in response_data
    assert "filter_results" in response_data
    total_results = (
        response_data[  # not just the number that would be returned in this context
            "num_results"
        ]
    )
    assert total_results == 2


@pytest.mark.django_db(transaction=True)
def test_explore_with_search_template_and_num_per_page(wiki_test_setup):
    wiki_config = wiki_test_setup["wiki_configs"][0]
    field = wiki_test_setup["fields"][0]
    docs = wiki_test_setup["docs"]

    wiki_configs = models.WikiConfig.objects.filter(id=wiki_config.id)

    create_value(docs[0], field, "test")
    create_value(docs[1], field, "wheee")
    build_search_index([wiki_config])

    with mock_template_content(
        "{% for key, value in test_object_1.items() %}{{ key }}: {{ value[key] }}\n{% endfor %}"
    ):
        response = explore(
            qs=[],
            filters={},
            offset=0,
            num_per_page=1,
            template_name="Search",
            template_config=wiki_config,
            wiki_configs=wiki_configs,
            results_limit=[],
            filters_only=False,
        )

    assert response.status_code == 200
    response_data = json.loads(response.content)
    assert "filter_results" in response_data
    assert not response_data[
        "filter_results"  # filters_only=False so no filters, default behavior
    ]
    assert (
        response_data["num_results"] == 1
    )  # just the count of results returned, not the total in this context
    assert "mwiki_text" in response_data


@pytest.mark.django_db(transaction=True)
def test_explore_with_search_template_num_per_page_and_with_ids(wiki_test_setup):
    wiki_config = wiki_test_setup["wiki_configs"][0]
    field = wiki_test_setup["fields"][0]
    docs = wiki_test_setup["docs"]

    wiki_configs = models.WikiConfig.objects.filter(id=wiki_config.id)

    create_value(docs[0], field, "test")
    create_value(docs[1], field, "wheee")
    build_search_index([wiki_config])

    with mock_template_content(
        "{% for key, value in test_object_1.items() %}{{ key }}: {{ value[key] }}\n{% endfor %}"
    ):
        response = explore(
            qs=[],
            filters={},
            offset=0,
            num_per_page=1,
            template_name="Search",
            template_config=wiki_config,
            wiki_configs=wiki_configs,
            results_limit=[],
            with_ids=True,
        )

    assert response.status_code == 200
    response_data = json.loads(response.content)
    assert response_data["num_results"] == 1
    assert "results" in response_data
    # despite setting num_per_page to 1 which results in num_results=1, we get 2 results because with_ids=True
    assert len(response_data["results"]) == 2


@pytest.mark.parametrize(
    "qs,expected_result",
    [
        (["I want to find all proposals about climate change"], ["climate change"]),
        (
            ["I would like to find all proposals about education reform"],
            ["education reform"],
        ),
        (["can you find me proposals related to water issues"], ["water issues"]),
        (["can you show me a proposal related to health"], ["health"]),
        (["can you retrieve proposals related to faith"], ["faith"]),
        (["can you please find me a proposal related to Texas"], ["Texas"]),
        (["can you show me any proposals concerning broadband"], ["broadband"]),
        (
            ["an unrelated query about healthcare"],
            ["an unrelated query about healthcare"],
        ),
    ],
)
def test_remove_stop_patterns(qs, expected_result, use_stop_patterns, settings):
    stop_patterns = getattr(settings, "TORQUE_STOP_PATTERNS", [])

    cleaned_qs = remove_stop_patterns(qs, stop_patterns)

    assert cleaned_qs == expected_result
