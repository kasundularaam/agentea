from abc import abstractmethod, ABC

from src.domain.agents.core.instruction import Instruction
from src.domain.ports.instruction_port import InstructionPort


class Agent(ABC):
    def __init__(self, name: str, instruction_adapter: InstructionPort, output_key: str | None = None):
        self.name = name
        self.instruction_adapter = instruction_adapter
        self.output_key = output_key
        self.tools = []
        self.add_tools()

    @abstractmethod
    def add_tools(self):
        pass

    def sync_instruction(self, default: Instruction) -> Instruction:
        return self.instruction_adapter.sync(default=default)
