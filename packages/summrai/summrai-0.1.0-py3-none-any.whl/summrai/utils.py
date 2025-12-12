def summarize_text(text, client):
    """
    Summarize text using the provided AIClient instance.
    """
    prompt = f"Summarize this:\n{text}"
    return client.get_response(prompt)


def format_response(text):
    """
    Basic cleanup for AI output.
    """
    return text.strip()
