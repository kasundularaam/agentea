import os
from datetime import datetime
from typing import AsyncGenerator

from google.adk import Runner
from google.adk.agents import BaseAgent, RunConfig
from google.adk.agents.run_config import StreamingMode
from google.adk.events import Event
from google.adk.sessions import InMemorySessionService, Session
from google.genai import types
from opik.integrations.adk import track_adk_agent_recursive, OpikTracer

from src.domain.agents.agents_chain import AgentsChain
from src.domain.agents.helpful_agent.agent import HelpfulAgent
from src.domain.entities.user.user_facade import UserFacade
from src.infrastructure.agent_client.adk.core.adk_competible_agent import ADKCompatibleAgent


class ADKAgentsChain(AgentsChain[BaseAgent]):

    def __init__(self, helpful_agent: HelpfulAgent, user_repo: UserFacade):
        super().__init__(helpful_agent=helpful_agent, user_repo=user_repo)

    def get_root_agent(self) -> BaseAgent:
        helpful_agent = ADKCompatibleAgent(self.helpful_agent).adk_agent

        # TODO: Add abstract observer to track all agents
        track_adk_agent_recursive(helpful_agent, OpikTracer(project_name=os.getenv("PROJECT_NAME_OPIK")))

        return helpful_agent

    @staticmethod
    def __get_runner(root_agent: BaseAgent) -> Runner:
        runner = Runner(app_name=os.getenv("APP_NAME"), agent=root_agent, session_service=InMemorySessionService())
        return runner

    def __get_user_id(self) -> str:
        return str(self.user_repo.get_current().id)

    @staticmethod
    def __get_session_id():
        return f"session-{datetime.now().isoformat()}"

    @staticmethod
    async def __create_session(runner: Runner, user_id: str, session_id: str) -> Session:
        session = await runner.session_service.create_session(app_name=os.getenv("APP_NAME"), user_id=str(user_id),
                                                              session_id=session_id)
        return session

    @staticmethod
    def __get_new_message(conversation) -> types.Content:
        return types.Content(role="user", parts=[types.Part(text=conversation)])

    async def __run_agent(self, message: str, streaming: bool = False) -> AsyncGenerator[Event, None]:

        root_agent = self.get_root_agent()
        runner = self.__get_runner(root_agent=root_agent)
        session_id = self.__get_session_id()
        new_message = self.__get_new_message(conversation=message)
        user_id = self.__get_user_id()

        await self.__create_session(runner, user_id=user_id, session_id=session_id)

        run_config = RunConfig(streaming_mode=StreamingMode.SSE if streaming else StreamingMode.NONE)

        events = runner.run_async(user_id=user_id, session_id=session_id, new_message=new_message,
                                  run_config=run_config)

        async for event in events:
            yield event

    async def invoke(self, message: str) -> str:
        events = self.__run_agent(message=message)

        last_event = None

        async for event in events:
            last_event = event

        if last_event:
            if last_event.content and last_event.content.parts:
                part = last_event.content.parts[0]
                if part.text:
                    return part.text
                return ""  # Part exists but text is empty

            return "Final event has no content parts."

        return "No events were generated."

    async def stream(self, message: str) -> AsyncGenerator[str, None]:
        events = self.__run_agent(message=message, streaming=True)

        async for event in events:
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        yield part.text
