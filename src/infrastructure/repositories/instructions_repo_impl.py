import logging
import os

from src.domain.entities.instruction.instruction import Instruction
from src.domain.entities.instruction.instructions_repo import InstructionsRepo

logger = logging.getLogger(__name__)


class InstructionsRepoImpl(InstructionsRepo):
    def get(self, name: str) -> Instruction:
        local_instr = self.local.get(name=name, client=os.getenv("AGENT_CLIENT"))

        remote_instr = self.remote.get_instruction(name=local_instr.name)

        if remote_instr:
            if remote_instr.version > local_instr.version:
                logger.info(f"Using Remote instruction for '{name}' (v{remote_instr.version} > v{local_instr.version})")
                return remote_instr

            elif local_instr.version > remote_instr.version:
                logger.info(f"Local instruction for '{name}' is newer (v{local_instr.version}). Updating Remote...")
                self.remote.save_instruction(local_instr)
                return local_instr
            else:
                return remote_instr

        if self.remote.health_check().is_healthy:
            logger.info(f"Instruction '{name}' not found on Remote. Uploading Local version.")
            self.remote.save_instruction(local_instr)

        logger.info(f"Using Local instruction for '{name}' (Fallback or Remote Init)")
        return local_instr
