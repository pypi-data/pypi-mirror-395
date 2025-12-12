"""
ai_queryhelper.core

Gemini-powered AI query helper functions.
"""

import os
import textwrap
from typing import Optional
import google.generativeai as genai


_client_configured = False


def _configure_client() -> None:
    """
    Configure Gemini client using environment variable GEMINI_API_KEY.
    Called lazily on first request.
    """
    global _client_configured

    if _client_configured:
        return

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY environment variable is not set.\n"
            "Get a key from https://aistudio.google.com/apikey"
        )

    genai.configure(api_key=api_key)
    _client_configured = True


def get_response(prompt: str, model: str = "gemini-2.5-flash") -> str:
    """
    Send a user query to Gemini and return a response.

    Args:
        prompt (str): User input string.

    Returns:
        str: AI-generated response text.
    """
    if not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    _configure_client()

    try:
        response = genai.GenerativeModel(model).generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        raise RuntimeError(f"Gemini API error: {e}") from e


def summarize_text(text: str, model: str = "gemini-2.5-flash") -> str:
    """
    Summarize content using AI.

    Args:
        text (str): Input content.

    Returns:
        str: Bullet point summary.
    """
    prompt = (
        "Summarize the following content into 4-5 bullet points:\n\n"
        f"{text}"
    )
    return get_response(prompt, model)


def format_response(text: str, width: int = 80) -> str:
    """
    Format AI output for display (line wrapping, cleaning).

    Args:
        text (str): AI output text.
        width (int): line wrap width.

    Returns:
        str: formatted text.
    """
    cleaned = text.strip()
    return textwrap.fill(cleaned, width)
