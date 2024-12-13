# 使用 Semantic Scholar API，加入排名分數
def query_data_with_ranking(keywords):
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={keywords}&fields=title,abstract,citationCount,influentialCitationCount"
    headers = {"x-api-key": "YOUR_API_KEY"}  # 替換為您的 API 密鑰
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return []
    
    papers = response.json().get('data', [])
    results = []
    
    for paper in papers:
        title = paper.get('title')
        abstract = paper.get('abstract')
        citation_count = paper.get('citationCount', 0)
        influential_citation_count = paper.get('influentialCitationCount', 0)
        
        # 計算排名分數（可根據需求調整權重）
        ranking_score = citation_count + influential_citation_count * 2
        results.append({
            'title': title,
            'abstract': abstract,
            'ranking_score': ranking_score
        })
    
    # 根據排名分數排序
    results = sorted(results, key=lambda x: x['ranking_score'], reverse=True)
    return results
