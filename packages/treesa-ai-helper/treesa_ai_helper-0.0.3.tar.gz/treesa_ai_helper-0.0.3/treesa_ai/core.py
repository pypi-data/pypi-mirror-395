"""
core.py
AI helper functions for response generation using Google Gemini.

Usage Example:
--------------
from treesa_ai import get_response

answer = get_response("Tell me a joke")
print(answer)
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables (.env must contain GEMINI_API_KEY)
load_dotenv()

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Set it in your .env file.")

genai.configure(api_key=api_key)

def get_response(prompt: str) -> str:
    """
    Generate an AI response using Google Gemini.

    Parameters
    ----------
    prompt : str
        User query text.

    Returns
    -------
    str
        AI-generated response.

    Raises
    ------
    ValueError
        If prompt is empty or invalid.
    """

    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return response.text
