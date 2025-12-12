import os
from dataclasses import dataclass
from typing import Optional

try:
    from openai import OpenAI  # new SDK (>=1.0)
    _HAS_NEW_OPENAI = True
except Exception:
    OpenAI = None
    _HAS_NEW_OPENAI = False

try:
    import openai as openai_legacy  # legacy SDK (<1.0)
    _HAS_LEGACY_OPENAI = True
except Exception:
    openai_legacy = None
    _HAS_LEGACY_OPENAI = False


@dataclass
class LLMResponse:
    content: str


class SimpleChatOpenAI:
    def __init__(self, model: str, temperature: float = 0.7, api_key: Optional[str] = None):
        self.model = model
        self.temperature = float(temperature)
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")

        if _HAS_NEW_OPENAI:
            self._client = OpenAI(api_key=self.api_key)
        elif _HAS_LEGACY_OPENAI:
            openai_legacy.api_key = self.api_key
            self._client = None
        else:
            raise RuntimeError("The 'openai' Python package is required but not installed. Please 'pip install openai'.")

    def invoke(self, prompt: str) -> LLMResponse:
        messages = [{"role": "user", "content": prompt}]
        if _HAS_NEW_OPENAI:
            resp = self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
            )
            content = resp.choices[0].message.content
        else:
            resp = openai_legacy.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
            )
            content = resp["choices"][0]["message"]["content"]
        return LLMResponse(content=content)