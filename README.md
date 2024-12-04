# Research Idea Generator 
# 研究想法產生器

Generate research ideas using LLMs.
使用法學碩士產生研究想法。


API Usage Example
Input:
curl -X POST -H "Content-Type: application/json" -d '{"keywords": "AI in medical imaging"}' http://127.0.0.1:5000/idea_generator
Output:
{
    "keywords": "AI in medical imaging",
    "ideas": "Develop a deep learning model to enhance cardiovascular disease imaging accuracy. Explore GANs for rare disease image synthesis."
}

系統架構運作流程
System Architecture Workflow

1.User Input: 用戶輸入的關鍵字通過 /idea_generator API 傳送。
User Input: Users provide keywords through the /idea_generator API.

2.Data Querying: 調用 query_data 函式，檢索學術資料（如 ArXiv）。
Data Querying: The query_data function retrieves academic data (e.g., from ArXiv).

3.Summarization: 使用 generate_summary 函式生成簡明扼要的研究建議。
Summarization: The generate_summary function generates concise research suggestions.

4.Output: 返回用戶經處理的研究想法清單。
Output: Processed research idea lists are returned to the user.
