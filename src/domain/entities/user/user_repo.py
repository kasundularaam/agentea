from abc import ABC, abstractmethod

from src.domain.entities.user.user import User


class UserRepo(ABC):

    @property
    @abstractmethod
    def user(self) -> User:
        pass
