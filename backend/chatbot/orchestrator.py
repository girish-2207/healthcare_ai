import os
from typing import Optional

from .document_loader   import DocumentLoader
from .embedding_manager import EmbeddingManager
from .retriever         import Retriever
from .intent_classifier import IntentClassifier
from .prompt_builder    import PromptBuilder
from .llm_client        import LLMClient
from .safety_guard      import SafetyGuard
from .chat_history      import ChatHistoryManager


class MedicalChatbot:
    def __init__(
        self,
        docs_dir: str    = "medical_docs",
        index_path: str  = "vector_store/faiss_index",
        db_path: str     = "database/medical.db",
        llm_model: str   = "llama-3.1-8b-instant",
        openai_api_key: str = "",
        rebuild_index: bool = False,
    ):
        self.index_path = index_path

        self.loader    = DocumentLoader(docs_dir)
        self.embedder  = EmbeddingManager()
        self.retriever = Retriever(self.embedder)
        self.intent    = IntentClassifier()
        self.prompt    = PromptBuilder()
        self.llm       = LLMClient(model=llm_model, api_key=openai_api_key)
        self.safety    = SafetyGuard()
        self.history   = ChatHistoryManager(db_path=db_path)

        self._setup_index(rebuild_index)

    def _setup_index(self, rebuild: bool):
        index_exists = os.path.exists(self.index_path)
        if rebuild or not index_exists:
            print("[MedicalChatbot] Building FAISS index...")
            documents = self.loader.load()
            chunks    = self.loader.chunk(documents)
            self.embedder.build_index(chunks, save_path=self.index_path)
        else:
            self.embedder.load_index(load_path=self.index_path)

    def chat(self, user_id, query, external_context=None):
        if self.safety.is_emergency(query):
            return {
                "response": self.safety.emergency_response(),
                "sources": [],
                "intent": "emergency",
            }

        intent   = self.intent.classify(query)
        history  = self.history.get(user_id, last_n=5)
        chunks   = self.retriever.search(query, intent, top_k=4)
        messages = self.prompt.build(query, chunks, history, external_context)
        response = self.llm.generate(messages)
        response = self.safety.add_disclaimer(response)

        self.history.save(user_id, query, response)
        sources = list(set([c.metadata.get("source", "unknown") for c in chunks]))

        return {
            "response": response,
            "sources":  sources,
            "intent":   intent,
        }

    def reset(self, user_id: str):
        self.history.clear(user_id)
        return {"message": f"Cleared history for {user_id}"}