# src/agents/summarization_agent.py

class SummarizationAgent:
    def summarize_papers(self, papers):
        """
        Summarizes a list of research papers.
        
        Args:
            papers (list): A list of paper metadata (e.g., titles, abstracts).
        
        Returns:
            list: Summarized insights from the papers.
        """
        summaries = []
        for paper in papers:
            summary = f"Title: {paper['title']}\nSummary: {paper['abstract'][:200]}..."  # Example
            summaries.append(summary)
        return summaries
