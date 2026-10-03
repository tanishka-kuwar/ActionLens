from app.services.document_service import extract_pdf_pages
from app.services.rag_service import retrieve_relevant_pdf_chunks
from app.services.action_extraction_service import extract_actions_from_chunks


pdf_path = "backend/uploads/testing1.pdf"

pages = extract_pdf_pages(pdf_path)

results = retrieve_relevant_pdf_chunks(
    pages,
    source="tesing1.pdf",
    top_k=2
)

print("\n========== RETRIEVED EVIDENCE ==========\n")

for result in results:
    print(f"Page: {result['page']}")
    print(f"Source: {result['source']}")
    print(f"Score: {result['score']:.4f}")
    print(result["text"])
    print("-" * 60)


print("\n========== ACTIONLENS RESULT ==========\n")

result = extract_actions_from_chunks(results)

print(result.model_dump_json(indent=4))