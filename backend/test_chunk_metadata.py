from app.services.chunk_metadata_service import create_document_chunks


document = """
Placement Registration Notice

All students must register by 20 September 2026.

Students must upload their updated resume.

Students must carry two printed copies of their resume and college ID.

Students must report at 9:00 AM in Seminar Hall 2.

Only students with an aggregate CGPA above 7.0 are eligible.
"""


chunks = create_document_chunks(
    document,
    source="college_notice.txt"
)


print("\n========== DOCUMENT CHUNKS ==========\n")

for chunk in chunks:

    print(f"Chunk ID: {chunk.chunk_id}")
    print(f"Source: {chunk.source}")
    print(f"Page: {chunk.page}")
    print(f"Section: {chunk.section}")
    print("Text:")
    print(chunk.text)
    print("-" * 50)