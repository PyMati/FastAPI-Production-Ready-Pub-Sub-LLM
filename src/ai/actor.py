from typing import Generator

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage


class Actor:
    def stream(self, message_content: str) -> Generator[str, None, None]:
        agent = create_agent("gpt-3.5-turbo")
        messages = {"messages": [HumanMessage(content=message_content)]}
        for chunk in agent.stream(messages, stream_mode="messages", version="v2"):
            yield chunk
