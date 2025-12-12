def format_response(data):
    """Return a nicely formatted string from API response"""
    try:
        return data["choices"][0]["message"]["content"]
    except Exception:
        return str(data)

def summarize_text(text, max_words=50):
    """Simple summary by truncating words"""
    words = text.split()
    return " ".join(words[:max_words]) + ("..." if len(words) > max_words else "")
