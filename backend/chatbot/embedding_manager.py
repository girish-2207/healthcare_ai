# embedding_manager.py

import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


class EmbeddingManager:
    # Change this line in EmbeddingManager __init__
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        print(f"[EmbeddingManager] Loading model: {model_name}")
        self.model = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={"device": "cpu"},
        )
        self.index = None

    def build_index(self, chunks, save_path: str = "vector_store/faiss_index"):
        print("[EmbeddingManager] Building FAISS index...")
        self.index = FAISS.from_documents(chunks, self.model)
        os.makedirs(save_path, exist_ok=True)
        self.index.save_local(save_path)
        print(f"[EmbeddingManager] Saved to {save_path}")

    def load_index(self, load_path: str = "vector_store/faiss_index"):
        print(f"[EmbeddingManager] Loading index from {load_path}")
        self.index = FAISS.load_local(
            load_path,
            self.model,
            allow_dangerous_deserialization=True,
        )
        print("[EmbeddingManager] Index loaded")

    def get_index(self):
        if self.index is None:
            raise ValueError("FAISS index not loaded yet.")
        return self.index