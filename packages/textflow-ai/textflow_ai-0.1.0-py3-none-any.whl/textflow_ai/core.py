"""
textflow_ai.core
----------------
A simple helper library for AI operations such as generating responses,
summaries, or formatting text.

Functions:
    get_response(prompt)
    summarize_text(text)
    format_response(text)
"""

def get_response(prompt: str) -> str:
    """
    Generates a simple AI-like response.
    (You may later replace this with a real AI API call.)
    """
    return f"AI Response: You asked → {prompt}"


def summarize_text(text: str) -> str:
    """
    Returns a short summary of the input text.
    """
    if len(text) < 50:
        return "Text is too short to summarize."
    return text[:50] + "... (summary)"


def format_response(text: str) -> str:
    """
    Cleans extra spaces and capitalizes the output.
    """
    return text.strip().capitalize()
