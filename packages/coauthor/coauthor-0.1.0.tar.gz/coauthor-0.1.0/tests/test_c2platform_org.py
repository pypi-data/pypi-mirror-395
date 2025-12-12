from coauthor.utils.c2platform_org import search_using_ddg
from coauthor.utils.c2platform_org import download_html_and_convert_to_markdown
import pytest


def test_search_ddg_nl():
    search_string = "what is c2 platform? site:c2platform.org language:nl"
    results = search_using_ddg(search_string, max_results=1)
    assert results[0]["href"] == "https://c2platform.org/nl/"


def test_search_ddg_en():
    search_string = "what is c2 platform? site:c2platform.org language:en"
    results = search_using_ddg(search_string, max_results=1)
    assert results[0]["href"] == "https://c2platform.org/"


def test_search_ddg_concepts_en():
    search_string = "what are the concepts of c2 platform? site:c2platform.org language:en"
    results = search_using_ddg(search_string, max_results=1)
    assert results[0]["href"] == "https://c2platform.org/docs/concepts/"


def test_search_getting_started():
    search_string = "development environment setup site:c2platform.org"
    results = search_using_ddg(search_string, max_results=1)
    assert results[0]["href"] == "https://c2platform.org/docs/howto/dev-environment/setup/"
    results = search_using_ddg(search_string, max_results=1, return_docs=False)
    assert results[0]["href"] == "https://c2platform.org/docs/howto/dev-environment/setup/"


def test_download_html_and_convert_to_markdown():
    url = "https://c2platform.org/docs/getting-started/"
    getting_started_md = download_html_and_convert_to_markdown(url)
    assert "set up a local development environment" in getting_started_md


def test_download_html_and_convert_to_markdown_exception():
    url = "https://c2platform.org/docs/getting-started-does-not-exist/"

    with pytest.raises(RuntimeError, match="404 Client Error: Not Found for url"):
        download_html_and_convert_to_markdown(url)
