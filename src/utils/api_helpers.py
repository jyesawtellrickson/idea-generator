# src/utils/api_helpers.py
import requests
from bs4 import BeautifulSoup

# from openai import OpenAI
# import os
from dotenv import load_dotenv
import os

# from ollama import chat
# from ollama import ChatResponse

load_dotenv()


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
        api_config["endpoint"],
        headers={"Authorization": f"Bearer {api_config['api_key']}"},
        params={"query": query, "limit": 5},
    )
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"Error fetching papers: {response.status_code}")
        return []


# Example of using ArXiv API
def get_arxiv_papers(keywords, num_results):
    url = f"http://export.arxiv.org/api/query?search_query=all:{keywords}&start=0&max_results={num_results}"
    response = requests.get(url)
    if response.status_code != 200:
        return []

    # Parse the XML response
    soup = BeautifulSoup(response.content, "lxml")
    entries = soup.find_all("entry")
    results = []

    for entry in entries:
        title = entry.title.text
        summary = entry.summary.text
        results.append({"title": title, "summary": summary})

    return results


def query_semantic_scholar(keywords):
    pass
    """config = {
        "paper_api": {
            "endpoint": "https://api.semanticscholar.org/v1/papers",
            "api_key": "YOUR_API_KEY_HERE"
        },
        "llm": {
            "model": "gpt-4",
            "temperature": 0.7
        }
    }"""


def init_openai():
    # Load environment variables from .env file
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ask_openai(client, system_prompt, prompt):
    try:
        # Call OpenAI ChatCompletion API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {"role": "user", "content": prompt},
            ],
        )

        # Claculate the cost of this request
        prompt_tokens = response.usage.prompt_tokens
        competion_tokens = response.usage.completion_tokens
        cost = (prompt_tokens / 1000000) * 0.15 + (competion_tokens / 1000000) * 0.6
        # Extract the message content from the response
        return response.choices[0].message.content, cost

    except Exception as e:
        return f"An error occurred: {str(e)}"


def get_local_response(system_prompt, prompt, model="llama3.2:latest"):
    response: ChatResponse = chat(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {"role": "user", "content": system_prompt + "\n\n" + prompt},
        ],
    )
    response = response["message"]["content"]

    return response


# Define tools to fetch research papers from multiple sources
def get_pubmed_papers(keyword: str, num_results: int = 5) -> list[dict]:
    """
    Fetches the latest research papers from PubMed.
    Requires `requests` and may require an API key for advanced access.
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "pubmed", "term": keyword, "retmax": num_results, "retmode": "json"}
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        ids = data.get("esearchresult", {}).get("idlist", [])
        details_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        details_params = {"db": "pubmed", "id": ",".join(ids), "retmode": "json"}
        details_response = requests.get(details_url, params=details_params)
        if details_response.status_code == 200:
            details_data = details_response.json()
            return list(details_data.get("result", {}).values())[1:]
    return []


def get_ieee_papers(keyword: str, num_results: int = 5) -> list[dict]:
    """
    Fetches research papers from IEEE Xplore.
    Requires an API key.
    """
    base_url = "http://ieeexploreapi.ieee.org/api/v1/search/articles"
    api_key = os.getenv("IEEE_API_KEY")
    params = {"apikey": api_key, "querytext": keyword, "max_records": num_results, "format": "json"}
    response = requests.get(base_url, params=params)
    print(response)
    if response.status_code == 200:
        return response.json().get("articles", [])
    return []


def get_springer_papers(keyword: str, num_results: int = 5) -> list[dict]:
    """
    Fetches research papers from Springer.
    Requires an API key. Replace 'YOUR_API_KEY' with a valid key.
    """
    base_url = "http://api.springernature.com/metadata/json"
    api_key = os.getenv("SPRINGER_NATURE_API_KEY")
    params = {"q": keyword, "api_key": api_key, "p": num_results}
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json().get("records", [])
    return []
