from ..schemas.chunk_schema import DocumentChunk
from ..schemas.document_schema import DocumentPage
from .chunk_service import split_text_into_chunks


def create_document_chunks(
    text: str,
    source: str | None = None
) -> list[DocumentChunk]:

    chunks = split_text_into_chunks(text)

    document_chunks = []

    for index, chunk in enumerate(chunks):

        document_chunks.append(
            DocumentChunk(
                chunk_id=index,
                text=chunk,
                source=source
            )
        )

    return document_chunks


def create_pdf_chunks(
    pages: list[DocumentPage],
    source: str | None = None
) -> list[DocumentChunk]:

    document_chunks = []

    chunk_id = 0

    for page in pages:

        chunks = split_text_into_chunks(page.text)

        for chunk in chunks:

            document_chunks.append(
                DocumentChunk(
                    chunk_id=chunk_id,
                    text=chunk,
                    source=source,
                    page=page.page_number
                )
            )

            chunk_id += 1

    return document_chunks