"""
ai.py – AI helper functions.
"""

import re

import google.generativeai as genai

def get_response(prompt, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")

    response = model.generate_content(prompt)
    return response.text



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
