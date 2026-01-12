from typing import AsyncGenerator

from src.application.agents.agents_chain import AgentsChain


class ReplyMessage:
    def __init__(self, chain: AgentsChain):
        self.chain = chain

    async def generate(self, new_message: str) -> str:
        return await self.chain.invoke(message=new_message)

    async def stream(self, new_message: str) -> AsyncGenerator[str, None]:
        source_stream = self.chain.stream(message=new_message)
        async for token in source_stream:  # type: ignore
            yield token
