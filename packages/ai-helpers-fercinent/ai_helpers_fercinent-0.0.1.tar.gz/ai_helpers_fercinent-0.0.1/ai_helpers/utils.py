def summarize_text(text):
    """
    Summarize text to the first 150 characters.
    """
    if len(text) > 150:
        return text[:150] + "..."
    return text


def format_response(text):
    """
    Clean text for HTML display.
    """
    return text.strip().replace("\n", "<br>")
