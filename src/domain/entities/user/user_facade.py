from abc import ABC, abstractmethod

from src.domain.entities.user.user import User


class UserFacade(ABC):
    @abstractmethod
    def get_current(self) -> User:
        pass
