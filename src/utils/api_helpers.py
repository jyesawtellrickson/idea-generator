# src/utils/api_helpers.py

import requests

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
