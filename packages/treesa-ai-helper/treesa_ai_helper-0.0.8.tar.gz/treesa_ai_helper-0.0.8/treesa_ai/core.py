"""
core.py
AI helper functions for response generation using Groq (Llama-3 models).

Usage Example:
--------------
from treesa_ai import get_response

answer = get_response("Tell me a joke")
print(answer)
"""

"""
core.py - GROQ version
"""

import os
from dotenv import load_dotenv
from groq import Groq

# Load .env variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found. Set it in your .env file.")

# Create Groq client
client = Groq(api_key=api_key)

def get_response(prompt: str) -> str:
    """Generate AI response using GROQ."""
    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
    )

    # FIX is here ↓↓↓
    return response.choices[0].message.content
