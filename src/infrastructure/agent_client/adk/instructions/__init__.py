from typing import Dict

from src.domain.agents.core.instruction import Instruction
from src.infrastructure.agent_client.adk.instructions.helpful_agent import SYSTEM_INSTRUCTION, DESCRIPTION, VERSION

_AGENT_INSTRUCTION_MAP: Dict[str, Instruction] = {
    "helpful_agent": Instruction(name="helpful_agent", instruction=SYSTEM_INSTRUCTION, description=DESCRIPTION,
                                 version=VERSION)}


def get_adk_instruction(agent_name: str) -> Instruction:
    try:
        return _AGENT_INSTRUCTION_MAP[agent_name]
    except KeyError:
        raise ValueError(f"Unknown agent name: {agent_name}")
