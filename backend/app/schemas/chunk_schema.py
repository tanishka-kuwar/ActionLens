from pydantic import BaseModel

class DocumentChunk(BaseModel):
    chunk_id: int
    text: str
    source: str | None = None
    page: int | None = None
    section: str | None = None