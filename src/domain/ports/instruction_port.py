from abc import ABC, abstractmethod

from src.domain.agents.core.instruction import Instruction


class InstructionPort(ABC):

    @abstractmethod
    def sync(self, default: Instruction) -> Instruction:
        pass
