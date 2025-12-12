"""
ai_helpers.core

This module provides helper functions that simulate AI-powered
text generation and summarization without using external APIs.
It is designed for student projects, Flask apps, and educational use.
"""

def get_response(prompt: str) -> str:
    """
    Generate a simulated AI-style response for a given prompt.

    Parameters
    ----------
    prompt : str
        The user's input message or question.

    Returns
    -------
    str
        A fake AI-generated answer created using rule-based logic.
    """
    prompt = prompt.strip()

    if not prompt:
        return "Please enter a valid prompt."

    # Simple rule-based "AI" engine
    if "what" in prompt.lower():
        return f"Here is what I found about: {prompt}"
    elif "how" in prompt.lower():
        return f"Here is how you can understand: {prompt}"
    elif "why" in prompt.lower():
        return f"This is why: {prompt}"
    else:
        # Generic fallback response
        return f"You said: {prompt}. I think this means you need more details."


def summarize_text(text: str) -> str:
    """
    Summarize long text using a rule-based method
    (first sentence + short snippet).

    Parameters
    ----------
    text : str
        The long input text that needs to be summarized.

    Returns
    -------
    str
        A short summary created by simple logic.
    """
    text = text.strip()

    if len(text.split()) < 10:
        return "Text too short to summarize."

    sentences = text.split(".")
    first_sentence = sentences[0].strip()

    # Create a snippet of about 12 words
    words = text.split()
    short_snippet = " ".join(words[:12]) + "..."

    return f"Summary: {first_sentence}. {short_snippet}"


def format_response(text: str) -> str:
    """
    Clean the AI output text.

    Parameters
    ----------
    text : str
        Any raw text.

    Returns
    -------
    str
        Cleaned text with whitespace trimmed.
    """
    return text.strip()
