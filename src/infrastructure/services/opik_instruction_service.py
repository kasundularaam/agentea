from opik import Opik, Prompt

from src.domain.agents.core.instruction import Instruction
from src.domain.ports.instruction_port import InstructionPort


class OpikInstructionService(InstructionPort):
    @staticmethod
    def __from_opik(name: str) -> Instruction | None:
        opik_prompt = Opik().get_prompt(name)

        if opik_prompt is None:
            return None

        metadata = opik_prompt.metadata

        if metadata is None:
            raise ValueError("Metadata not found")

        description = opik_prompt.metadata.get("description")
        if description is None:
            raise ValueError("Description not found")

        version = opik_prompt.metadata.get("version")

        if version is None:
            raise ValueError("Version not found")

        return Instruction(name=opik_prompt.name, instruction=opik_prompt.prompt, description=description,
                           version=version)

    def __register_opik_instruction(self, instruction: Instruction) -> Instruction:
        metadata = {"description": instruction.description, "version": instruction.version}
        Prompt(name=instruction.name, prompt=instruction.instruction, metadata=metadata)
        return self.__from_opik(name=instruction.name)

    def sync(self, default: Instruction) -> Instruction:
        opik_instruction = self.__from_opik(default.name)
        if opik_instruction:
            if opik_instruction.version >= default.version:
                return opik_instruction
        return self.__register_opik_instruction(instruction=default)
