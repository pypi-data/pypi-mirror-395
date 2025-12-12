"""
ai.py – AI helper functions.
"""

import re

def get_response(prompt: str) -> str:
    """
    Generate a mock AI response.

    Args:
        prompt (str): The user prompt.

    Returns:
        str: A simple AI-generated response (placeholder).
    """
    return f"AI Response: {prompt[::-1]}"  # Temporary dummy logic


def summarize_text(text: str, sentences: int = 2) -> str:
    """
    Summarize text by returning the first few sentences.

    Args:
        text (str): The long text to summarize.
        sentences (int): Number of sentences to return.

    Returns:
        str: Summarized text.
    """
    parts = re.split(r"(?<=[.!?]) +", text)
    return " ".join(parts[:sentences]) if parts else text
