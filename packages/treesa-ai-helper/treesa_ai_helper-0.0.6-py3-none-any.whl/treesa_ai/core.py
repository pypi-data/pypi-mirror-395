"""
core.py
AI helper functions for response generation using Groq (Llama-3 models).

Usage Example:
--------------
from treesa_ai import get_response

answer = get_response("Tell me a joke")
print(answer)
"""

import os
from dotenv import load_dotenv
from groq import Groq

# Load variables from .env (must contain GROQ_API_KEY)
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found. Set it in your .env file.")

# Initialize Groq client
client = Groq(api_key=api_key)

def get_response(prompt: str) -> str:
    """
    Generate an AI response using Groq Llama 3.1.

    Parameters
    ----------
    prompt : str
        User input text.

    Returns
    -------
    str
        The generated AI response.
    """

    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    chat_completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",   # fast & free model
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return chat_completion.choices[0].message["content"]
