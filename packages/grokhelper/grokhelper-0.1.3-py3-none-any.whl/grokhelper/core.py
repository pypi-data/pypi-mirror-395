import os
import requests
from typing import Optional

class GrokHelper:
    """
    A simple wrapper to interact with Grok API by xAI.
    You can also extend this to support OpenAI, Gemini, etc.
    """

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GROK_API_KEY")
        if not self.api_key:
            raise ValueError("GROK_API_KEY not found. Set it as env var or pass directly.")
        self.base_url = "https://api.x.ai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def get_response(self, prompt: str, model: str = "grok-beta") -> str:
        """
        Send a prompt to Grok and return the response.

        Args:
            prompt (str): User query
            model (str): Model name (default: grok-beta)

        Returns:
            str: AI-generated response
        """
        if not prompt.strip():
            return "Please enter a valid question."

        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }

        try:
            response = requests.post(self.base_url, json=payload, headers=self.headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        except requests.exceptions.RequestException as e:
            return f"Error communicating with AI: {str(e)}"
        except KeyError:
            return "Unexpected response from AI service."

    def summarize_text(self, text: str) -> str:
        """Summarize long text using Grok"""
        prompt = f"Summarize the following text in 3-4 sentences:\n\n{text}"
        return self.get_response(prompt)

    def format_response(self, text: str) -> str:
        """Clean up AI response (remove extra spaces, etc.)"""
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return "\n".join(lines)