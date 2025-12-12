import re

def clean_response(text: str) -> str:
    """Remove extra newlines and clean AI output"""
    text = re.sub(r'\n{3,', '\n\n', text)
    return text.strip()

def summarize_text(text: str, ai_client) -> str:
    prompt = f"Summarize the following in 3-4 sentences:\n\n{text[:4000]}"
    return ai_client.ask(prompt)