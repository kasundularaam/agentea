from abc import ABC, abstractmethod
from typing import Dict, Any


class VectorDBPort(ABC):

    @abstractmethod
    def get(self, collection_name: str, query: str, output_fields: list[str]) -> list[Dict[str, Any]]:
        pass

    @abstractmethod
    def search_similar(self, collection_name: str, embeddings: list[float], output_fields: list[str], top_k: int = 10,
                       embedding_filed: str = "embedding") -> list[Dict[str, Any]]:
        pass
