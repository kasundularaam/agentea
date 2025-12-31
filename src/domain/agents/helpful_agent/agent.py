from src.domain.agents.core.agent import Agent
from src.domain.ports.instruction_port import InstructionPort


class HelpfulAgent(Agent):
    def __init__(self, instruction_adapter: InstructionPort) -> None:
        super().__init__(name="helpful_agent", instruction_adapter=instruction_adapter)

    def add_tools(self):
        pass
