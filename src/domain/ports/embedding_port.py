from abc import ABC, abstractmethod


class EmbeddingPort(ABC):
    @abstractmethod
    def create_embedding(self, text: str) -> list[float]:
        pass