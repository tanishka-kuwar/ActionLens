from .chunk_metadata_service import create_document_chunks
from .embedding_service import generate_embeddings
from .vector_service import VectorStore


def retrieve_relevant_chunks(
    document_text: str,
    source: str | None = None,
    top_k: int = 3
):

    # Create metadata-aware chunks
    chunks = create_document_chunks(
        document_text,
        source=source
    )

    if not chunks:
        return []

    # Extract only the text for embedding
    chunk_texts = [
        chunk.text
        for chunk in chunks
    ]

    embeddings = generate_embeddings(
        chunk_texts
    )

    vector_store = VectorStore()

    vector_store.add_embeddings(
        embeddings,
        chunks
    )

    queries = [
        "What actions or tasks must someone complete?",
        "What deadlines, dates, or times are mentioned?",
        "What documents or requirements are needed?",
        "What eligibility conditions or warnings are mentioned?"
    ]

    retrieved_results = []

    for query in queries:

        query_embedding = generate_embeddings(
            [query]
        )[0]

        results = vector_store.search(
            query_embedding,
            top_k=top_k
        )

        for result in results:

            # Avoid duplicate chunks
            already_exists = any(
                existing["chunk_id"] == result["chunk_id"]
                for existing in retrieved_results
            )

            if not already_exists:
                retrieved_results.append(result)

    retrieved_results.sort(
        key=lambda result: result["score"],
        reverse=True
    )

    return retrieved_results[:top_k]

def retrieve_relevant_pdf_chunks(
    pages,
    source: str | None = None,
    top_k: int = 3
):
    """
    Retrieve relevant chunks from a PDF while preserving
    the original PDF page number.
    """

    from .chunk_metadata_service import create_pdf_chunks
    from .embedding_service import generate_embeddings
    from .vector_service import VectorStore

    # 1. Create page-aware chunks
    chunks = create_pdf_chunks(
        pages,
        source=source
    )

    if not chunks:
        return []

    # 2. Extract chunk text for embeddings
    chunk_texts = [
        chunk.text
        for chunk in chunks
    ]

    # 3. Generate embeddings
    embeddings = generate_embeddings(
        chunk_texts
    )

    # 4. Create vector store
    vector_store = VectorStore()

    vector_store.add_embeddings(
        embeddings,
        chunks
    )

    # 5. Queries representing the information
    # ActionLens is interested in
    queries = [
        "What actions or tasks must someone complete?",
        "What deadlines, dates, or times are mentioned?",
        "What documents or requirements are needed?",
        "What problems, issues, warnings, or important information are mentioned?",
        "What categories, instructions, or procedures are described?"
    ]

    retrieved_results = []

    # 6. Retrieve relevant chunks
    for query in queries:

        query_embedding = generate_embeddings(
            [query]
        )[0]

        results = vector_store.search(
            query_embedding,
            top_k=top_k
        )

        for result in results:

            already_exists = any(
                existing["chunk_id"] == result["chunk_id"]
                for existing in retrieved_results
            )

            if not already_exists:
                retrieved_results.append(result)

    # Sort all retrieved candidates by similarity score.
    retrieved_results.sort(
        key=lambda result: result["score"],
        reverse=True
    )

    # Return only the globally highest-scoring chunks.
    return retrieved_results[:top_k]