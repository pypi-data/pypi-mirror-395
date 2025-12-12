"""
Core AI helper functions using Groq's Llama 3.1 model.

Functions:
- get_response(prompt): chat reply from AI
- summarize_text(text): summary of AI or user text
- format_response(text): clean & wrap output for display
"""

import os
import textwrap
from groq import Groq


def _get_client() -> Groq:
    """
    Internal helper to create a Groq client.

    Raises
    ------
    RuntimeError
        If the GROQ_API_KEY environment variable is not set.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Please set it as an environment variable."
        )
    return Groq(api_key=api_key)


def get_response(prompt: str) -> str:
    """
    Send a prompt to the AI model and return the response text.

    Parameters
    ----------
    prompt : str
        The user input or question.

    Returns
    -------
    str
        The AI-generated response text.
    """
    if not prompt.strip():
        return "Please enter a non-empty prompt."

    client = _get_client()

    chat_completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful web assistant."},
            {"role": "user", "content": prompt},
        ],
    )

    return chat_completion.choices[0].message.content.strip()


def summarize_text(text: str) -> str:
    """
    Summarize a long piece of text using the AI model.

    Parameters
    ----------
    text : str
        The text to summarize.

    Returns
    -------
    str
        A short summary of the text.
    """
    if not text.strip():
        return "No text provided to summarize."

    if len(text.split()) < 15:
        return "Response is short; no summary needed."

    prompt = (
        "Summarize the following text in 3–4 bullet points using simple language:\n\n"
        f"{text}"
    )

    return get_response(prompt)


def format_response(text: str, width: int = 80) -> str:
    """
    Clean and format the AI output nicely before displaying.

    Parameters
    ----------
    text : str
        The raw AI output text.
    width : int, optional
        Maximum line width for wrapping (default 80).

    Returns
    -------
    str
        A cleaned, nicely wrapped version of the text.
    """
    if not text:
        return ""

    cleaned = text.strip()
    wrapped = textwrap.fill(cleaned, width=width)
    return wrapped
