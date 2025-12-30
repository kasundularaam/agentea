from abc import ABC, abstractmethod
from typing import Dict, Any


class DatabasePort(ABC):

    @abstractmethod
    def query(self, query: str) -> Dict[str, Any]:
        pass
