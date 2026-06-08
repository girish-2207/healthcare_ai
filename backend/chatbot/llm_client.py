import os
from langchain_groq import ChatGroq


class LLMClient:
    def __init__(self, model: str = "llama-3.1-8b-instant", api_key: str = ""):
        self.llm = ChatGroq(
            model=model,
            groq_api_key=api_key or os.getenv("GROQ_API_KEY"),
            temperature=0.3,
            max_tokens=512,
        )
        print(f"[LLMClient] Model: {model}")

    def generate(self, messages: list) -> str:
        response = self.llm.invoke(messages)
        return response.content