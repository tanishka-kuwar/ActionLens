from pathlib import Path
import fitz
from docx import Document
from ..schemas.document_schema import DocumentPage


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file.
    """

    text = ""

    pdf_document = fitz.open(file_path)

    for page in pdf_document:
        text += page.get_text()

    pdf_document.close()

    return text


def extract_text_from_docx(file_path: str) -> str:
    """
    Extract text from a DOCX file.
    """

    document = Document(file_path)

    text = "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
    )

    return text


def extract_text_from_txt(file_path: str) -> str:
    """
    Extract text from a TXT file.
    """

    return Path(file_path).read_text(
        encoding="utf-8"
    )


def extract_text(file_path: str) -> str:
    """
    Detect file type and extract text accordingly.
    """

    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    elif extension == ".docx":
        return extract_text_from_docx(file_path)

    elif extension == ".txt":
        return extract_text_from_txt(file_path)

    else:
        raise ValueError(
            f"Unsupported file type: {extension}"
        )

def extract_pdf_pages(file_path: str) -> list[DocumentPage]:
    pages = []

    pdf_document = fitz.open(file_path)

    for page_number, page in enumerate(pdf_document, start=1):

        text = page.get_text().strip()

        if text:
            pages.append(
                DocumentPage(
                    page_number=page_number,
                    text=text
                )
            )

    pdf_document.close()

    return pages