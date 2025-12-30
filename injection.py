from dependency_injector import containers, providers

from src.application.reply_message import ReplyMessage
from src.domain.agents.agents_chain import AgentsChain
from src.domain.agents.helpful_agent.agent import HelpfulAgent
from src.domain.entities.user.user_facade import UserFacade
from src.domain.ports.database_port import DatabasePort
from src.domain.ports.embedding_port import EmbeddingPort
from src.domain.ports.instruction_port import InstructionPort
from src.domain.ports.vector_db_port import VectorDBPort
from src.infrastructure.agent_client.adk.adk_agents_chain import ADKAgentsChain
from src.infrastructure.repositories.user_repo import UserRepo
from src.infrastructure.services.gemini_embeding_service import GeminiEmbeddingService
from src.infrastructure.services.milvus_vector_db_service import MilvusVectorDBService
from src.infrastructure.services.opik_instruction_service import OpikInstructionService
from src.infrastructure.services.trino_db_service import TrinoDatabaseService
from src.infrastructure.services.vertex_config import setup_vertex_env


class BaseContainer(containers.DeclarativeContainer):
    # Services
    vector_service = providers.Dependency(VectorDBPort)
    database_service = providers.Dependency(DatabasePort)
    embedding_service = providers.Dependency(EmbeddingPort)
    instruction_service = providers.Dependency(InstructionPort)

    # Repositories
    user_repo = providers.Dependency(UserFacade)

    # Agents
    helpful_agent = providers.Dependency(HelpfulAgent)

    # Chains
    agents_chain = providers.Dependency(AgentsChain)


class DevContainer(BaseContainer):
    # Wiring Packages
    wiring_config = containers.WiringConfiguration(packages=["src.routers"])

    # Resource Setup
    vertex_setup = providers.Resource(setup_vertex_env)

    # Services
    vector_service = providers.Singleton(MilvusVectorDBService)
    database_service = providers.Singleton(TrinoDatabaseService)
    embedding_service = providers.Singleton(GeminiEmbeddingService)
    instruction_service = providers.Singleton(OpikInstructionService)

    # Repositories
    user_repo = providers.Singleton(UserRepo)

    # Agents
    helpful_agent = providers.Singleton(HelpfulAgent, instruction_service=instruction_service)

    # Chains
    agents_chain = providers.Factory(ADKAgentsChain, helpful_agent=helpful_agent, user_repo=user_repo)

    reply_usecase = providers.Factory(ReplyMessage, chain=agents_chain)
