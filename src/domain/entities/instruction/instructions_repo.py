from abc import ABC

from src.domain.entities.instruction.instruction import Instruction
from src.domain.ports.local_instruction_port import LocalInstructionPort
from src.domain.ports.remote_instruction_port import RemoteInstructionPort


class InstructionsRepo(ABC):
    def __init__(self, remote_instruction_adapter: RemoteInstructionPort,
                 local_instruction_adapter: LocalInstructionPort):
        self.remote = remote_instruction_adapter
        self.local = local_instruction_adapter

    def get(self, name: str) -> Instruction:
        pass
