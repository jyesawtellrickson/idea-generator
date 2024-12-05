# src/utils/api_helpers.py
import requests
from bs4 import BeautifulSoup

# from openai import OpenAI
# import os
# from dotenv import load_dotenv

# from ollama import chat
# from ollama import ChatResponse


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
    soup = BeautifulSoup(response.content, 'lxml')
    entries = soup.find_all('entry')
    results = []
    
    for entry in entries:
        title = entry.title.text
        summary = entry.summary.text
        results.append({'title': title, 'summary': summary})
    
    return results



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
                    'role': 'system',
                    'content': system_prompt,
                },
                {
                    'role': 'user',
                    'content': prompt
                },
            ],
        )
        
        # Claculate the cost of this request
        prompt_tokens = response.usage.prompt_tokens
        competion_tokens = response.usage.completion_tokens
        cost = (prompt_tokens/1000000) * 0.15 + (competion_tokens/1000000) * 0.6
        # Extract the message content from the response
        return response.choices[0].message.content, cost
    
    except Exception as e:
        return f"An error occurred: {str(e)}"


def get_local_response(system_prompt, prompt, model='llama3.2:latest'):
    response: ChatResponse = chat(model=model, messages=[
        {
        'role': 'system',
        'content': system_prompt,
        },
        {
        'role': 'user',
        'content': system_prompt + '\n\n' + prompt
        },
    ],)
    response = response['message']['content']

    return response