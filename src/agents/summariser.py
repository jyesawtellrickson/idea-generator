# src/agents/summarization_agent.py

from transformers import pipeline

class SummarizationAgent:
    def __init__(self):
        # Load a pre-trained summarization model (e.g., T5 or BART)
        self.summarizer = pipeline('summarization', model='t5-small')

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

    def generate_summary(self, data):
        # Combine all summaries from queried data
        combined_text = ' '.join([item['summary'] for item in data])
    
        # Generate summarized text
        summary = self.summarizer(combined_text, max_length=100, min_length=30, do_sample=False)
        return summary[0]['summary_text']
