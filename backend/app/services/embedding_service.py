from sentence_transformers import SentenceTransformer


# Load the embedding model once when the application starts
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text: str) -> list[float]:
    """
    Convert a single piece of text into a numerical vector.
    """

    embedding = model.encode(text)

    return embedding.tolist()


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Convert multiple text chunks into numerical vectors.
    """

    embeddings = model.encode(texts)

    return embeddings.tolist()