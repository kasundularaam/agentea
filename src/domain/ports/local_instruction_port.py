from abc import ABC, abstractmethod

from src.application.agents.core.instruction import Instruction


class LocalInstructionPort(ABC):
    @abstractmethod
    def get(self, name: str, client:str) -> Instruction:
        pass
