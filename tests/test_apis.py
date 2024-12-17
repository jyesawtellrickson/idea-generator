from src.utils.api_helpers import (
    get_arxiv_papers,
    get_springer_papers,
    get_ieee_papers,
    get_pubmed_papers,
)

num_results_test = 2


def test_arxiv():
    results = get_arxiv_papers("machine learning", num_results_test)
    assert len(results) == num_results_test
    assert all([key in results[0].keys() for key in ["title", "summary"]])


def test_springer_nature():
    results = get_springer_papers("machine learning", num_results_test)
    assert len(results) == num_results_test
    assert all([key in results[0].keys() for key in ["title", "abstract"]])


def test_ieee():
    results = get_ieee_papers("machine learning", num_results_test)
    assert len(results) == num_results_test
    assert all([key in results[0].keys() for key in ["title", "summary"]])


def test_pubmed():
    results = get_pubmed_papers("machine learning", num_results_test)
    print(results)
    assert len(results) == num_results_test
    assert all([key in results[0].keys() for key in ["title", "sortpubdate"]])
