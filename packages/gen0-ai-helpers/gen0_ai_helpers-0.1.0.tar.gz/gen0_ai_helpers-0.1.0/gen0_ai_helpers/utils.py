from .core import get_response

def summarize_text(text: str) -> str:
    """
    Summarizes text using Gemini API.
    """
    prompt = f"Summarize the following text:\n\n{text}"
    return get_response(prompt)

def format_response(text: str) -> str:
    """
    Formats text for HTML output.
    """
    return text.replace("\n", "<br>").strip()
