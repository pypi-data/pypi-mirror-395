from openai import OpenAI
import os
from .exceptions import APIKeyMissing, APIError

class ChatGPTClient:
    def __init__(self, api_key: str = None, model: str = "gpt-4o-mini"):
        key = api_key or os.getenv("OPENAI_API_KEY")

        if not key:
            raise APIKeyMissing(
                "No API key provided. Set OPENAI_API_KEY in environment."
            )

        self.client = OpenAI(api_key=key)
        self.model = model

    def get_response(self, prompt: str, max_tokens: int = 200):
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens
            )
            return completion.choices[0].message.content.strip()

        except Exception as e:
            raise APIError(f"ChatGPT request failed: {e}")
