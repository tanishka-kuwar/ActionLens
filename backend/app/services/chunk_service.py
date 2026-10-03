import re


def split_text_into_chunks(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50
) -> list[str]:

    if not text.strip():
        return []

    if overlap >= chunk_size:
        raise ValueError("Overlap must be smaller than chunk size.")

    # Normalize line endings
    text = text.replace("\r\n", "\n")

    # Split using blank lines as paragraph boundaries
    paragraphs = [
        paragraph.strip()
        for paragraph in re.split(r"\n\s*\n", text)
        if paragraph.strip()
    ]

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:

        # If adding the paragraph stays within the limit
        if len(current_chunk) + len(paragraph) + 1 <= chunk_size:

            if current_chunk:
                current_chunk += "\n\n"

            current_chunk += paragraph

        else:

            if current_chunk:
                chunks.append(current_chunk.strip())

            # If a single paragraph is too large,
            # split it into smaller pieces.
            if len(paragraph) > chunk_size:

                start = 0

                while start < len(paragraph):

                    end = start + chunk_size
                    piece = paragraph[start:end].strip()

                    if piece:
                        chunks.append(piece)

                    start = end - overlap

                current_chunk = ""

            else:
                current_chunk = paragraph

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks