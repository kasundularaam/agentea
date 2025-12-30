import os

from google.adk.agents import LlmAgent

from src.domain.agents.core.agent import Agent
from src.infrastructure.agent_client.adk.instructions import get_adk_instruction


class ADKCompatibleAgent:
    def __init__(self, agent: Agent):
        self.agent = agent
        self.adk_agent = LlmAgent(model=os.getenv("MODEL_NAME"), name=agent.name, tools=agent.tools,
                                  output_key=agent.output_key)
        self.__set_instruction()

    def __set_instruction(self):
        adk_instruction = get_adk_instruction(agent_name=self.agent.name)
        instruction = self.agent.sync_instruction(default=adk_instruction)
        self.adk_agent.instruction = instruction.instruction
        self.adk_agent.description = instruction.description
