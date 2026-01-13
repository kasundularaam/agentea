from abc import ABC
from dataclasses import dataclass

from src.domain.entities.instruction.instruction import Instruction
from src.domain.entities.instruction.instructions_repo import InstructionsRepo


@dataclass(frozen=True)
class AgentContext:
    instructions_repo: InstructionsRepo


class Agent(ABC):
    def __init__(self, ctx: AgentContext):
        self.ctx = ctx

    NAME: str
    TOOLS: tuple = ()

    @property
    def name(self) -> str:
        return self.NAME

    @property
    def tools(self) -> list:
        return list(self.TOOLS)

    @property
    def instruction(self) -> Instruction:
        return self.ctx.instructions_repo.get(name=self.name)
