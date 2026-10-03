from app.services.rag_service import retrieve_relevant_chunks


document = """
Placement Registration Notice

All students must register by 20 September 2026.

Students must upload their updated resume.

Students must carry two printed copies of their resume and college ID.

Students must report at 9:00 AM in Seminar Hall 2.

Only students with an aggregate CGPA above 7.0 are eligible.
"""


results = retrieve_relevant_chunks(
    document,
    source="college_notice.txt"
)


print("\n========== RETRIEVED CHUNKS ==========\n")

for result in results:

    print(f"Chunk ID: {result['chunk_id']}")
    print(f"Score: {result['score']:.4f}")
    print(f"Source: {result['source']}")
    print(f"Page: {result['page']}")
    print(f"Section: {result['section']}")
    print("Text:")
    print(result["text"])

    print("-" * 60)