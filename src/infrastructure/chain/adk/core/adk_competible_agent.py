import os

from google.adk.agents import LlmAgent

from src.application.agents.core.agent import Agent


class ADKCompatibleAgent:
    def __init__(self, agent: Agent):
        self.agent = agent

    @property
    def adk_agent(self) -> LlmAgent:
        instruction = self.agent.instruction
        return LlmAgent(model=os.getenv("MODEL_NAME"), name=self.agent.name, tools=self.agent.tools,
                        instruction=instruction.instruction, description=instruction.description)
