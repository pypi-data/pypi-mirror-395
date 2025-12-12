from .core import get_response

def summarize_text(text):
    prompt = "Summarize this: " + text
    return get_response(prompt)

def format_response(text):
    return text.strip()
