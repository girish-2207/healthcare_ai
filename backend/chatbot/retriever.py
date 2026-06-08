from .embedding_manager import EmbeddingManager


class Retriever:
    def __init__(self, embedder: EmbeddingManager):
        self.embedder = embedder

    def search(self, query: str, intent: str, top_k: int = 4):
        index = self.embedder.get_index()

        if intent in ["drug", "disease", "diet"]:
            results = index.similarity_search_with_score(
                query,
                k=top_k,
                filter={"category": intent},
            )
            if not results:
                print(f"[Retriever] No filtered results, falling back to unfiltered")
                results = index.similarity_search_with_score(query, k=top_k)
        else:
            results = index.similarity_search_with_score(query, k=top_k)

        # filter out low relevance chunks — lower score = more similar
        relevant = [doc for doc, score in results if score < 1.0]

        if not relevant:
            print(f"[Retriever] No relevant chunks found for query")
            return []

        print(f"[Retriever] Found {len(relevant)} relevant chunks for intent '{intent}'")
        return relevant