from dependency_injector import containers, providers

from src.application.reply_message import ReplyMessage
from src.application.agents.agents_chain import AgentsChain
from src.application.agents.sub_agents.helpful_agent import HelpfulAgent
from src.domain.ports.remote_instruction_port import InstructionPort
from src.domain.ports.model_port import ModelPort
from src.domain.ports.observer_port import ObserverPort
from src.infrastructure.adapters.litellm_model_adapter import LiteLLMModelAdapter
from src.infrastructure.adapters.opik_instruction_adapter import OpikInstructionAdapter
from src.infrastructure.adapters.opik_observer_service import OpikObserverAdapter
from src.infrastructure.adapters.vertex_config import setup_vertex_env
from src.infrastructure.chain.adk.adk_agents_chain import ADKAgentsChain
from src.infrastructure.repositories.local_user_repo_impl import UserRepo


class BaseContainer(containers.DeclarativeContainer):
    # Adapters
    model_adapter = providers.Dependency(ModelPort)
    instruction_adapter = providers.Dependency(InstructionPort)
    observer_adapter = providers.Dependency(ObserverPort)

    # Repositories
    user_repo = providers.Dependency(UserRepo)

    # Agents
    helpful_agent = providers.Dependency(HelpfulAgent)

    # Chains
    agents_chain = providers.Dependency(AgentsChain)


class DevContainer(BaseContainer):
    # Wiring Packages
    wiring_config = containers.WiringConfiguration(packages=["src.routers"])

    # Resource Setup
    vertex_setup = providers.Resource(setup_vertex_env)

    # Adapters
    model_adapter = providers.Dependency(LiteLLMModelAdapter)
    observer_adapter = providers.Dependency(OpikObserverAdapter)
    instruction_adapter = providers.Singleton(OpikInstructionAdapter)

    # Repositories
    user_repo = providers.Singleton(UserRepo)

    # Agents
    helpful_agent = providers.Singleton(HelpfulAgent, instruction_adapter=instruction_adapter)

    # Chains
    agents_chain = providers.Factory(ADKAgentsChain, helpful_agent=helpful_agent, user_repo=user_repo)

    reply_usecase = providers.Factory(ReplyMessage, chain=agents_chain)
