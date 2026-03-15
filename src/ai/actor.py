from langchain_openai import ChatOpenAI


class Actor:
    def stream(self, message_content: str):
        llm = ChatOpenAI(model="gpt-3.5-turbo", streaming=True)
        for chunk in llm.stream(message_content):
            yield chunk
