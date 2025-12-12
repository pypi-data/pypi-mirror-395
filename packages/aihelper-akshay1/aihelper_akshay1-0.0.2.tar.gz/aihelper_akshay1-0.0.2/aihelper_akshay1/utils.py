def format_response(text: str) -> str:
    """Clean extra spaces and formatting from AI output."""
    return text.strip().replace("\n\n", "\n")
