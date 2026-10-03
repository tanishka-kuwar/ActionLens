import faiss
import numpy as np


class VectorStore:

    def __init__(self, dimension: int = 384):
        self.dimension = dimension

        self.index = faiss.IndexFlatIP(dimension)

        # Store complete chunk metadata
        self.chunks = []

    def add_embeddings(self, embeddings, chunks):

        if len(embeddings) != len(chunks):
            raise ValueError(
                "Number of embeddings must match number of chunks."
            )

        vectors = np.array(
            embeddings,
            dtype="float32"
        )

        # Normalize vectors so inner product becomes cosine similarity
        faiss.normalize_L2(vectors)

        self.index.add(vectors)

        self.chunks.extend(chunks)

    def search(
        self,
        query_embedding,
        top_k: int = 3
    ):

        if len(self.chunks) == 0:
            return []

        query_vector = np.array(
            [query_embedding],
            dtype="float32"
        )

        faiss.normalize_L2(query_vector)

        scores, indices = self.index.search(
            query_vector,
            min(top_k, len(self.chunks))
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0]
        ):

            if index == -1:
                continue

            chunk = self.chunks[index]

            results.append({
                "chunk_id": chunk.chunk_id,
                "text": chunk.text,
                "score": float(score),
                "source": chunk.source,
                "page": chunk.page,
                "section": chunk.section
            })

        return results