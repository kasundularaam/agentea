from abc import ABC, abstractmethod
from typing import TypeVar, Generic, AsyncGenerator

from src.domain.agents.helpful_agent.agent import HelpfulAgent
from src.domain.entities.user.user_facade import UserFacade

R = TypeVar("R")


class AgentsChain(Generic[R], ABC):
    def __init__(self, helpful_agent: HelpfulAgent, user_repo: UserFacade) -> None:
        self.helpful_agent = helpful_agent
        self.user_repo = user_repo

    @abstractmethod
    async def invoke(self, message: str) -> str:
        pass

    @abstractmethod
    async def stream(self, message: str) -> AsyncGenerator[str, None]:
        pass

    @abstractmethod
    def get_root_agent(self) -> R:
        pass
