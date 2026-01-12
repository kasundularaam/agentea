from abc import ABC, abstractmethod

from src.domain.status.service_status import ServiceStatus


class ObserverPort(ABC):

    @abstractmethod
    def observe_agent(self, root_agent) -> None:
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
