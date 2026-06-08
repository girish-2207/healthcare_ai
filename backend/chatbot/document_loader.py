import os
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    CSVLoader,
    UnstructuredWordDocumentLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentLoader:
    LOADER_MAP = {
        ".txt":  TextLoader,
        ".pdf":  PyPDFLoader,
        ".csv":  CSVLoader,
        ".docx": UnstructuredWordDocumentLoader,
    }

    def __init__(self, directory: str):
        self.directory = directory

    def load(self):
        documents = []
        for filename in os.listdir(self.directory):
            ext = os.path.splitext(filename)[1].lower()
            if ext in self.LOADER_MAP:
                filepath = os.path.join(self.directory, filename)
                try:
                    loader = self.LOADER_MAP[ext](filepath)
                    docs = loader.load()
                    for doc in docs:
                        doc.metadata["source"] = filename
                        doc.metadata["category"] = self._infer_category(filename)
                    documents.extend(docs)
                    print(f"[DocumentLoader] Loaded: {filename}")
                except Exception as e:
                    print(f"[DocumentLoader] Failed {filename}: {e}")
        print(f"[DocumentLoader] Total loaded: {len(documents)}")
        return documents

    def _infer_category(self, filename: str) -> str:
        name = filename.lower()
        if any(k in name for k in ["drug", "medicine", "pharma"]):
            return "drug"
        elif any(k in name for k in ["symptom", "disease", "condition"]):
            return "disease"
        elif any(k in name for k in ["diet", "food", "nutrition"]):
            return "diet"
        return "general"

    def chunk(self, documents):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", ".", " "],
        )
        chunks = splitter.split_documents(documents)
        print(f"[DocumentLoader] Total chunks: {len(chunks)}")
        return chunks