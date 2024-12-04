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



System Flow
具體做法：
1.設計系統架構：
    使用工具：使用 Visio、Lucidchart 或 Figma 繪製流程圖。
    流程概述：
    1.用戶輸入：提供關鍵字、研究主題或領域。
    2.資料查詢模組：觸發查詢模組檢索學術文章或相關數據。
    3.AI生成模組：使用生成式AI模型（例如 GPT 系列）創建多個初步想法。
    4.摘要模組：整理並篩選生成的內容，輸出簡單明瞭的摘要。
    5.用戶反饋：允許用戶選擇或進一步調整生成的研究題目。
2.具體技術：
    後端框架：Django、Flask（Python），或 Node.js。
    前端框架：React、Vue.js，設計簡單用戶界面。
    整合工具：REST API 連接數據查詢、生成和摘要模組。

System Flow
Implementation Details:
1.Design System Architecture:
    Tools: Use tools like Visio, Lucidchart, or Figma to create flowcharts.
    Process Overview:
    1.User Input: Users provide keywords, research topics, or fields.
    2.Data Querying Module: Triggers the querying module to retrieve academic articles or related data.
    3.AI Generation Module: Uses generative AI models (e.g., GPT series) to create multiple initial ideas.
    4.Summarizer Module: Refines and filters the generated content, outputting actionable research topics.
    5.User Feedback: Allows users to select or further refine the generated topics.
2.Technical Implementation:
    Backend Framework: Use Django, Flask (Python), or Node.js.
    Frontend Framework: Use React or Vue.js to design a simple user interface.
    Integration Tools: Use REST API to connect the querying, generation, and summarization modules.
