from abc import ABC, abstractmethod
from typing import AsyncGenerator

from src.application.agents.sub_agents.helpful_agent import HelpfulAgent
from src.domain.entities.user.user_repo import UserRepo
from src.domain.ports.observer_port import ObserverPort


class AgentsChain(ABC):
    def __init__(self, helpful_agent: HelpfulAgent, user_repo: UserRepo, observer_adapter:ObserverPort) -> None:
        self.helpful_agent = helpful_agent
        self.user_repo = user_repo
        self.observer_adapter = observer_adapter

    @abstractmethod
    async def invoke(self, message: str) -> str:
        pass

    @abstractmethod
    async def stream(self, message: str) -> AsyncGenerator[str, None]:
        pass

    @property
    @abstractmethod
    def root_agent(self):
        pass
