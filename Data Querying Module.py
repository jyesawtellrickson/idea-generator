import requests
from bs4 import BeautifulSoup

# Example of using ArXiv API
def query_data(keywords):
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