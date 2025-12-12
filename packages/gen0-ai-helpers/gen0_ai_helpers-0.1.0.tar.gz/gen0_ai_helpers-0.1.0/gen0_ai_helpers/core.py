import os
import requests

def get_response(prompt: str) -> str:
    """
    Sends a prompt to the Gemini REST API and returns generated content.
    Handles API errors gracefully.
    """

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "❌ Error: GEMINI_API_KEY environment variable not set."

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash-latest:generateContent?key={api_key}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        res = requests.post(url, json=payload)
        data = res.json()

        # Common success case
        if "candidates" in data:
            return data["candidates"][0]["content"]["parts"][0]["text"]

        # Fallback error formatting
        return f"❌ API Error: {data}"

    except Exception as e:
        return f"❌ Request Failed: {str(e)}"
