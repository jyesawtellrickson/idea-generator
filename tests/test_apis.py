from src.utils.api_helpers import (
    get_arxiv_papers,
    get_springer_papers,
    get_ieee_papers,
    get_pubmed_papers,
)


def test_arxiv():
    results = get_arxiv_papers("machine learning", 5)
    assert len(results) == 5
    assert all([key in results[0].keys() for key in ["title", "summary"]])


def test_springer_nature():
    results = get_springer_papers("machine learning", 5)
    assert len(results) == 5
    assert all([key in results[0].keys() for key in ["title", "abstract"]])


def test_ieee():
    results = get_ieee_papers("machine learning", 5)
    assert len(results) == 5
    assert all([key in results[0].keys() for key in ["title", "summary"]])


def test_pubmed():
    results = get_pubmed_papers("machine learning", 5)
    print(results)
    assert len(results) == 5
    assert all([key in results[0].keys() for key in ["title", "sortpubdate"]])
