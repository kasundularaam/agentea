import os

from google.adk.models.lite_llm import LiteLlm

from src.domain.ports.model_port import ModelPort


class LiteLLMModelAdapter(ModelPort):
    @property
    def model(self, agent_name: str | None = None):
        return LiteLlm(model=os.getenv('LLM_MODEL_NAME'), api_key=os.getenv('LLM_API_KEY'),
                       base_url=os.getenv('LLM_API_URL'), custom_llm_provider='openai')
