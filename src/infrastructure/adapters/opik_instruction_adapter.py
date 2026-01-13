import logging
from datetime import datetime
from typing import Optional

from opik import Opik, Prompt

from src.application.agents.core.instruction import Instruction
from src.domain.ports.remote_instruction_port import RemoteInstructionPort
from src.domain.status.service_status import ServiceStatus

logger = logging.getLogger(__name__)


class OpikInstructionAdapter(RemoteInstructionPort):
    def __init__(self):
        self.service_name = "OpikInstructionService"
        self._is_enabled: bool = True
        self._last_error: Optional[str] = None
        self._disabled_at: Optional[datetime] = None
        self.client = Opik()

    # --- Circuit Breaker & Health ---
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
        return ServiceStatus(
            service_name=self.service_name,
            is_enabled=self._is_enabled,
            is_healthy=self._last_error is None,
            status_message="ENABLED" if self._is_enabled else "DISABLED",
            last_error=self._last_error,
            disabled_at=self._disabled_at
        )

    def _trigger_circuit_breaker(self, error: Exception):
        self._is_enabled = False
        self._last_error = str(error)
        self._disabled_at = datetime.now()
        logger.error(f"⚠️ {self.service_name} failed. Auto-disabling. Error: {error}")


    def get_instruction(self, name: str) -> Optional[Instruction]:
        """
        Safely attempts to fetch an instruction from Opik.
        Returns None if disabled, not found, or if an error occurs.
        """
        logger.info(f"Fetching instruction '{name}' from Opik.")
        if not self._is_enabled:
            return None

        try:
            opik_prompt = self.client.get_prompt(name)

            if opik_prompt is None:
                return None

            metadata = opik_prompt.metadata or {}
            description = metadata.get("description")
            version = metadata.get("version")
            client = metadata.get("client")

            if description is None or version is None:
                logger.warning(f"Opik prompt '{name}' found but missing metadata (desc/ver). skipping.")
                return None

            return Instruction(
                name=opik_prompt.name,
                instruction=opik_prompt.prompt,
                description=description,
                version=version,
                client=client
            )

        except Exception as e:
            self._trigger_circuit_breaker(e)
            return None

    def save_instruction(self, instruction: Instruction) -> None:
        """
        Safely attempts to save an instruction to Opik.
        """
        logger.info(f"Saving instruction '{instruction.name}' to Opik.")
        if not self._is_enabled:
            return

        try:
            metadata = {
                "description": instruction.description,
                "version": instruction.version,
                "provider": instruction.provider
            }
            Prompt(
                name=instruction.name,
                prompt=instruction.instruction,
                metadata=metadata
            )
            logger.info(f"Synced instruction '{instruction.name}' (v{instruction.version}) to Opik.")

        except Exception as e:
            self._trigger_circuit_breaker(e)