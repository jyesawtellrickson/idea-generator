from transformers import pipeline

# Load a pre-trained summarization model (e.g., T5 or BART)
summarizer = pipeline('summarization', model='t5-small')

def generate_summary(data):
    # Combine all summaries from queried data
    combined_text = ' '.join([item['summary'] for item in data])
    
    # Generate summarized text
    summary = summarizer(combined_text, max_length=100, min_length=30, do_sample=False)
    return summary[0]['summary_text']
