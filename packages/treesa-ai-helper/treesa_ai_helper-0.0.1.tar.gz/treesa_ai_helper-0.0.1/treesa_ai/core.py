"""
core.py
This module provides AI helper functions such as get_response().

Usage Example:
--------------
from treesa_ai import get_response

answer = get_response("Tell me a joke")
print(answer)
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Load API key from .env file

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_response(prompt: str) -> str:
    """
    Generate a response using OpenAI's chat model.

    Parameters
    ----------
    prompt : str
        The user's text query.

    Returns
    -------
    str
        The AI-generated response.

    Raises
    ------
    ValueError
        If the prompt is empty.
    """

    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message["content"].strip()
