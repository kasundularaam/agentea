from src.domain.agents.core.agent import Agent
from src.domain.ports.instruction_port import InstructionPort


class HelpfulAgent(Agent):
    def __init__(self, instruction_service: InstructionPort) -> None:
        super().__init__(name="helpful_agent", instruction_service=instruction_service, )

    def add_tools(self):
        pass
