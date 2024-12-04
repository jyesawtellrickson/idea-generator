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

Data Querying
具體做法：
1.設置數據來源：
    對接 API：
        Google Scholar：使用 SerpAPI，實現學術內容的檢索。
        ArXiv：直接調用其開放的 API，檢索特定主題的學術論文。
        專利資料庫：調用 Lens.org 或 WIPO API，查詢技術專利。
    網絡爬蟲（備選）：如無 API，可通過 Python 的 BeautifulSoup 或 Scrapy 撰寫自動化數據爬取程式。
2.查詢處理：
    用戶輸入清理：
        使用 NLP 工具（如 spaCy 或 NLTK）解析輸入的關鍵詞並生成查詢語句。
    語意分析：
        部署 BERT 模型，確保用戶的輸入能轉化為有效的查詢參數。
    過濾與排序：
        使用 Elasticsearch 或 SQL 數據庫進行快速查詢。
        加入相關性排序算法，例如基於 TF-IDF 或 BM25 的方法。
3.數據格式化：
    將結果轉換為 JSON 格式，方便後續模組處理。

Data Querying
Implementation Details:
1.Set Data Sources:
    API Integration:
        Google Scholar: Use SerpAPI to retrieve academic content.
        ArXiv: Directly use its open API to query academic papers on specific topics.
        Patent Databases: Utilize APIs from Lens.org or WIPO to search for patents.
    Web Scraping (Optional): If APIs are unavailable, use Python libraries like BeautifulSoup or Scrapy for automated data crawling.
2.Query Processing:
    Input Cleaning:
        Use NLP tools like spaCy or NLTK to parse keywords and generate query statements.
    Semantic Analysis:
        Deploy a BERT model to ensure user inputs are translated into effective query parameters.
    Filtering and Ranking:
        Use Elasticsearch or SQL databases for fast query processing.
        Implement ranking algorithms like TF-IDF or BM25 for relevance scoring.
3.Data Formatting:
    Convert results into JSON format for seamless processing by subsequent modules.

Summariser
具體做法：
1.摘要模型選擇：
    零基礎實現：
        使用 Hugging Face 提供的 transformers 模組，部署訓練好的 BERT 或 T5 模型。
    工具調用：
        GPT 模型（OpenAI API）：直接利用其強大的摘要生成能力。
        提供參數：控制摘要長度和語言風格（專業、簡潔、學術性）。
2.摘要生成邏輯：
    從數據查詢模組的結果中提取關鍵段落。
    使用 NLP 技術分析關鍵詞和句子關係，濃縮關鍵訊息。
3.摘要優化：
    設定輸出層級：
        簡要版：生成3-5條核心想法。
        詳細版：生成含背景與可能研究方向的完整摘要。
    允許用戶進一步調整摘要風格或重點。
4.整合測試：
    測試用例：輸入不同領域的關鍵字（例如「氣候變遷+能源效率」），檢查摘要的準確性和實用性。

Summariser
Implementation Details:
1.Choose a Summarization Model:
    Custom Implementation:
        Use pre-trained models from Hugging Face’s transformers library, such as BERT or T5.
    API Integration:
        Use GPT models (e.g., OpenAI API) for powerful summarization capabilities.
        Provide parameters to control the summary length and style (e.g., professional, concise, academic).
2.Summarization Logic:
    Combine all summaries from the queried data.
    Use NLP techniques to analyze keywords and sentence relationships, condensing key information.
3.Optimize Summarization:
    Define output levels:
        Brief Version: Generate 3-5 core ideas.
        Detailed Version: Generate summaries with background information and potential research directions.
    Allow users to further adjust the summary style or focus.
4.Integration Testing:
    Test cases: Input keywords from various fields (e.g., "climate change + energy efficiency") and check the accuracy and usability of the generated summaries.
