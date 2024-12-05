# src/utils/api_helpers.py
import requests
from bs4 import BeautifulSoup

def fetch_related_papers(query, api_config):
    """
    Fetches related research papers using an API.
    
    Args:
        query (str): User's research query.
        api_config (dict): Configuration for the API.
    
    Returns:
        list: List of paper metadata.
    """
    response = requests.get(
        api_config['endpoint'],
        headers={"Authorization": f"Bearer {api_config['api_key']}"},
        params={"query": query, "limit": 5}
    )
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"Error fetching papers: {response.status_code}")
        return []


# Example of using ArXiv API
def query_arxiv(keywords):
    url = f"http://export.arxiv.org/api/query?search_query=all:{keywords}&start=0&max_results=5"
    response = requests.get(url)
    if response.status_code != 200:
        return []
    
    # Parse the XML response
    soup = BeautifulSoup(response.content, 'xml')
    entries = soup.find_all('entry')
    results = []
    
    for entry in entries:
        title = entry.title.text
        summary = entry.summary.text
        results.append({'title': title, 'summary': summary})
    
    return results