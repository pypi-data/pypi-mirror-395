"""
Simple in-memory conversation history storage.
"""

from typing import List, Dict


class ConversationHistory:
    def __init__(self, max_items: int = 100):
        self.items: List[Dict[str, str]] = []
        self.max_items = max_items

    def add(self, prompt: str, response: str):
        self.items.append({"prompt": prompt, "response": response})
        if len(self.items) > self.max_items:
            self.items = self.items[-self.max_items:]

    def all(self):
        return list(self.items)

    def clear(self):
        self.items.clear()
