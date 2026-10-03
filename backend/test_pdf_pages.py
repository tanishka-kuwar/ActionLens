from app.services.document_service import extract_pdf_pages


pdf_path = "backend/uploads/testing1.pdf"

pages = extract_pdf_pages(pdf_path)


print("\n========== PDF PAGES ==========\n")

for page in pages:

    print(f"Page: {page.page_number}")
    print(page.text[:500])
    print("-" * 60)