from app.services.document_service import extract_pdf_pages
from app.services.rag_service import retrieve_relevant_pdf_chunks


# Use the same PDF path you used in test_pdf_pages.py
pdf_path = "backend/uploads/testing1.pdf"


# 1. Extract pages
pages = extract_pdf_pages(pdf_path)


print("\n========== PDF INFORMATION ==========\n")

print(f"Total pages: {len(pages)}")


# 2. Run page-aware RAG
results = retrieve_relevant_pdf_chunks(
    pages,
    source="Email or username (2).pdf",
    top_k=2
)


print("\n========== RETRIEVED PDF CHUNKS ==========\n")


for result in results:

    print(f"Chunk ID: {result['chunk_id']}")
    print(f"Score: {result['score']:.4f}")
    print(f"Source: {result['source']}")
    print(f"Page: {result['page']}")
    print(f"Section: {result['section']}")

    print("Text:")
    print(result["text"])

    print("-" * 70)