import json
import logging
from pathlib import Path

from src.domain.entities.instruction.instruction import Instruction
from src.domain.ports.local_instruction_port import LocalInstructionPort

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parents[2]

class FileInstructionAdapter(LocalInstructionPort):

    def __init__(self, registry_path: str = "data/instructions/instructions.json"):
        self.registry_path = BASE_DIR / registry_path

    def get(self, name: str, client: str) -> Instruction:
        logger.info(f"Getting instruction for agent '{name}' for client '{client}'")
        if not self.registry_path.exists():
            raise FileNotFoundError(f"Registry file not found at: {self.registry_path}")

        with open(self.registry_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        agent_config = next(
            (agent for agent in data.get("agents", []) if agent["name"] == name and agent.get("client") == client),
            None)

        if not agent_config:
            raise ValueError(f"Instruction not found for agent '{name}' (client: {client})")

        md_file_path = Path(agent_config["instructions"])

        if not md_file_path.exists():
            raise FileNotFoundError(f"Markdown file missing at: {md_file_path}")

        with open(md_file_path, "r", encoding="utf-8") as md_file:
            markdown_content = md_file.read()

        return Instruction(name=agent_config["name"], description=agent_config["description"],
                           instruction=markdown_content, version=agent_config["version"], client=agent_config["client"])
