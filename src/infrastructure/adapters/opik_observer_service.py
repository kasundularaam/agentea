import logging
import os
from datetime import datetime
from typing import Optional

from opik.integrations.adk import track_adk_agent_recursive, OpikTracer

from src.domain.ports.observer_port import ObserverPort
from src.domain.status.service_status import ServiceStatus

logger = logging.getLogger(__name__)


class OpikObserverAdapter(ObserverPort):
    def __init__(self):
        self.service_name = "OpikObserverService"
        self.app_name = os.getenv('APP_NAME')

        self._is_enabled: bool = True
        self._last_error: Optional[str] = None
        self._disabled_at: Optional[datetime] = None

    def enable(self) -> None:
        self._is_enabled = True
        self._last_error = None
        self._disabled_at = None
        logger.info(f"{self.service_name} manually ENABLED.")

    def disable(self) -> None:
        self._is_enabled = False
        self._disabled_at = datetime.now()
        logger.info(f"{self.service_name} manually DISABLED.")

    def health_check(self) -> ServiceStatus:
        return ServiceStatus(service_name=self.service_name, is_enabled=self._is_enabled,
                             is_healthy=self._last_error is None,
                             status_message="ENABLED" if self._is_enabled else "DISABLED", last_error=self._last_error,
                             disabled_at=self._disabled_at)

    def _trigger_circuit_breaker(self, error: Exception):
        self._is_enabled = False
        self._last_error = str(error)
        self._disabled_at = datetime.now()
        logger.error(f"⚠️ {self.service_name} failed. Auto-disabling. Error: {error}")

    def observe_agent(self, root_agent) -> None:
        logger.info(f"Observing agent '{root_agent.name}' to Opik.")
        if not self._is_enabled:
            logger.warning(f"Skipping Opik observation because {self.service_name} is DISABLED. "
                           f"(Reason: {self._last_error or 'Manual Action'})")
            return None

        try:
            tracer = OpikTracer(self.app_name)
            track_adk_agent_recursive(root_agent, tracer)

        except Exception as e:
            self._trigger_circuit_breaker(e)
            return None
