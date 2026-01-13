from abc import ABC, abstractmethod

from src.domain.entities.instruction.instruction import Instruction
from src.domain.status.service_status import ServiceStatus


class RemoteInstructionPort(ABC):

    @abstractmethod
    def get_instruction(self, name: str) -> Instruction:
        pass

    @abstractmethod
    def save_instruction(self, instruction: Instruction):
        pass

    @abstractmethod
    def disable(self):
        pass

    @abstractmethod
    def enable(self):
        pass

    @abstractmethod
    def health_check(self) -> ServiceStatus:
        pass
