from typing import List
from dataclasses import dataclass
import os

# Both new and legacy OpenAI SDKs for maximum compatibility
try:
    from openai import OpenAI  # new SDK (>=1.0)
    _HAS_NEW_OPENAI = True
    print(f"_HAS_NEW_OPENAI :{_HAS_NEW_OPENAI}")
except Exception:
    OpenAI = None
    _HAS_NEW_OPENAI = False

try:
    import openai as openai_legacy  # legacy SDK (<1.0)
    _HAS_LEGACY_OPENAI = True
    print(f"_HAS_LEGACY_OPENAI :{_HAS_LEGACY_OPENAI}")
except Exception:
    openai_legacy = None
    _HAS_LEGACY_OPENAI = False


@dataclass
class SimpleOpenAIEmbeddings:
    api_key: str | None = None
    model: str | None = None  # Will default later if None

    def __post_init__(self):
        if self.api_key is None:
            self.api_key = os.environ.get("OPENAI_API_KEY")
        if self.model is None:
            self.model = os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

        if _HAS_NEW_OPENAI:
            self._client = OpenAI(api_key=self.api_key)
        elif _HAS_LEGACY_OPENAI:
            openai_legacy.api_key = self.api_key
            self._client = None
        else:
            raise RuntimeError("The 'openai' Python package is required but not installed. Please 'pip install openai'.")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        if _HAS_NEW_OPENAI:
            resp = self._client.embeddings.create(model=self.model, input=texts)
            # Ensure order matches inputs
            # The new SDK returns .data as a list of objects with .embedding
            return [item.embedding for item in resp.data]
        else:
            # Legacy SDK
            resp = openai_legacy.Embedding.create(model=self.model, input=texts)
            # resp['data'] is a list of dicts with 'embedding'
            # The order follows the input list
            return [item["embedding"] for item in resp["data"]]

    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text])[0]