import os
from groq import Groq
from typing import Optional

class IAIHelper:
    """
    IAI Helper – Super-fast AI interface using Groq
    Published on PyPI as iai-helper
    """
    def __init__(self, api_key: Optional[str] = None, model: str = "llama-3.3-70b-versatile"):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found! Get free key at https://console.groq.com/keys")
        self.client = Groq(api_key=self.api_key)
        self.model = model

    def ask(self, prompt: str, temperature: float = 0.7) -> str:
        """Get AI response for any question"""
        try:
            completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=temperature,
                max_tokens=2048,
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: {str(e)}"