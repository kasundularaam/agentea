from abc import ABC, abstractmethod

from src.domain.entities.instruction.instruction import Instruction


class LocalInstructionPort(ABC):
    @abstractmethod
    def get(self, name: str, client: str) -> Instruction:
        pass
