from abc import ABC, abstractmethod


class ModelPort(ABC):
    @property
    @abstractmethod
    def model(self, agent_name: str | None = None):
        pass
