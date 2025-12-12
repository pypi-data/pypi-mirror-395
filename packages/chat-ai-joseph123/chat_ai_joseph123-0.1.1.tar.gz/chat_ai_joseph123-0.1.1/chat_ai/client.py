"""
CHAT_AI.client
Clean and safe client for querying OpenAI-like APIs.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
API_URL = "https://api.openai.com/v1/chat/completions"

def get_response(prompt: str):
    """
    Universal safe response wrapper.
    Always returns a dict containing:
    { "choices": [ { "message": { "content": "..." } } ] }
    """

    if not API_KEY:
        return {
            "choices": [
                {"message": {
                    "content": "ERROR: Missing API key. Set OPENAI_API_KEY in .env"
                }}
            ]
        }

    if not prompt or not prompt.strip():
        return {
            "choices": [
                {"message": {
                    "content": "ERROR: Prompt cannot be empty."
                }}
            ]
        }

    try:
        response = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=(5, 20)  # connect timeout, read timeout
        )

        # Handle HTTP errors before parsing JSON
        if response.status_code != 200:
            return {
                "choices": [
                    {"message": {
                        "content": f"HTTP Error {response.status_code}: {response.text}"
                    }}
                ]
            }

        data = response.json()

        # Handle API format errors
        if "choices" not in data:
            return {
                "choices": [
                    {"message": {
                        "content": f"API Error: {data}"
                    }}
                ]
            }

        return data

    except requests.exceptions.Timeout:
        return {
            "choices": [
                {"message": {
                    "content": "Network Error: Request timed out."
                }}
            ]
        }

    except Exception as e:
        return {
            "choices": [
                {"message": {"content": f"Network Error: {str(e)}"}}
            ]
        }
