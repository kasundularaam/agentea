import os
from typing import List

from google import genai

from src.domain.ports.embedding_port import EmbeddingPort


class GeminiEmbeddingService(EmbeddingPort):
    def __init__(self) -> None:
        self.model = self._get_env("EMBEDDING_MODEL_NAME")
        self.client = self._init_client()

    @staticmethod
    def _get_env(name: str, default: str | None = None) -> str:
        value = os.getenv(name, default)
        if not value:
            raise ValueError(f"{name} is not set")
        return value

    @staticmethod
    def _init_client() -> genai.Client:
        return genai.Client()

    def create_embedding(self, text: str) -> List[float]:
        if not text or not text.strip():
            raise ValueError("Text must not be empty")
        response = self.client.models.embed_content(model=self.model, contents=text)

        return response.embeddings[0].values
