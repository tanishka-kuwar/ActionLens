from app.services.rag_service import retrieve_relevant_chunks
from app.services.action_extraction_service import extract_actions_from_chunks


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
    source="college_notice.txt",
    top_k=3
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