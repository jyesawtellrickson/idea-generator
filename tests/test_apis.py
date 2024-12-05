

from src.utils.api_helpers import query_arxiv

def test_arxiv():
    results = query_arxiv("machine learning") 
    assert len(results) > 0
    assert all([key in results[0].keys() for key in ["title", "summary"]])
