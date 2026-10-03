from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
import shutil

from backend.app.services.document_service import extract_text
from backend.app.services.text_service import clean_text
from backend.app.services.chunk_service import split_text_into_chunks
from backend.app.services.embedding_service import generate_embeddings
from backend.app.services.vector_service import VectorStore
from backend.app.services.action_extraction_service import extract_actions

from .services.rag_service import (
    retrieve_relevant_chunks,
    retrieve_relevant_pdf_chunks
)

from .services.document_service import (
    extract_text,
    extract_pdf_pages
)

from .services.text_service import clean_text
from .services.action_extraction_service import extract_actions_from_chunks

vector_store = VectorStore()

app = FastAPI(
    title="ActionLens API",
    description="AI-powered document action intelligence platform",
    version="1.0.0"
)

UPLOAD_DIR = Path("backend/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}


@app.get("/")
def home():
    return {
        "message": "Welcome to ActionLens API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOCX, and TXT files are allowed."
        )

    file_path = UPLOAD_DIR / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "Document uploaded successfully",
        "filename": file.filename,
        "file_path": str(file_path)
    }

@app.post("/extract-text")
async def extract_document_text(file: UploadFile = File(...)):
    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOCX, and TXT files are allowed."
        )

    file_path = UPLOAD_DIR / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        extracted_text = extract_text(str(file_path))

        return {
            "message": "Text extracted successfully",
            "filename": file.filename,
            "text": extracted_text
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Text extraction failed: {str(error)}"
        )

@app.post("/clean-text")
async def clean_document_text(file: UploadFile = File(...)):
    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOCX, and TXT files are allowed."
        )

    file_path = UPLOAD_DIR / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        extracted_text = extract_text(str(file_path))
        cleaned_text = clean_text(extracted_text)

        return {
            "message": "Text cleaned successfully",
            "filename": file.filename,
            "cleaned_text": cleaned_text
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Text cleaning failed: {str(error)}"
        )

@app.post("/chunk-text")
async def chunk_document_text(file: UploadFile = File(...)):
    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOCX, and TXT files are allowed."
        )

    file_path = UPLOAD_DIR / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        extracted_text = extract_text(str(file_path))
        cleaned_text = clean_text(extracted_text)
        chunks = split_text_into_chunks(cleaned_text)

        return {
            "message": "Text chunked successfully",
            "filename": file.filename,
            "total_chunks": len(chunks),
            "chunks": chunks
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Text chunking failed: {str(error)}"
        )

@app.post("/semantic-search")
async def semantic_search(file: UploadFile = File(...), query: str = ""):
    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOCX, and TXT files are allowed."
        )

    file_path = UPLOAD_DIR / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # 1. Extract text
        extracted_text = extract_text(str(file_path))

        # 2. Clean text
        cleaned_text = clean_text(extracted_text)

        # 3. Split into chunks
        chunks = split_text_into_chunks(cleaned_text)

        # 4. Generate embeddings for chunks
        embeddings = generate_embeddings(chunks)

        # 5. Store embeddings in FAISS
        vector_store.add_embeddings(
            embeddings,
            chunks
        )

        # 6. Generate embedding for user's query
        query_embedding = generate_embeddings([query])[0]

        # 7. Search for similar chunks
        results = vector_store.search(
            query_embedding,
            top_k=3
        )

        return {
            "query": query,
            "results": results
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Semantic search failed: {str(error)}"
        )

@app.post("/extract-actions")
async def extract_document_actions(file: UploadFile = File(...)):
    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file_extension}"
        )

    file_path = UPLOAD_DIR / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # --------------------------------------------------
        # PDF DOCUMENT
        # --------------------------------------------------
        if file_extension == ".pdf":

            pages = extract_pdf_pages(str(file_path))

            if not pages:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "The PDF contains no extractable text. "
                        "It may be a scanned/image-based PDF. "
                        "OCR support will be added later."
                    )
                )

            retrieved_chunks = retrieve_relevant_pdf_chunks(
                pages,
                source=file.filename,
                top_k=5
            )

        # --------------------------------------------------
        # TXT / DOCX DOCUMENT
        # --------------------------------------------------
        else:

            extracted_text = extract_text(str(file_path))
            cleaned_text = clean_text(extracted_text)

            if not cleaned_text:
                raise HTTPException(
                    status_code=400,
                    detail="The document contains no extractable text."
                )

            retrieved_chunks = retrieve_relevant_chunks(
                cleaned_text,
                source=file.filename,
                top_k=5
            )

        # --------------------------------------------------
        # ACTION EXTRACTION FROM RETRIEVED RAG CHUNKS
        # --------------------------------------------------

        if not retrieved_chunks:
            raise HTTPException(
                status_code=400,
                detail="No relevant content could be retrieved from the document."
            )

        result = extract_actions_from_chunks(retrieved_chunks)

        return result.model_dump()

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Action extraction failed: {str(error)}"
        )

