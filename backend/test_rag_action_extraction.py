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


print("\n========== STEP 1: RETRIEVING RELEVANT CHUNKS ==========\n")

chunks = retrieve_relevant_chunks(document)

for i, chunk in enumerate(chunks, start=1):
    print(f"--- Retrieved Chunk {i} ---")
    print(chunk)
    print()


print("\n========== STEP 2: EXTRACTING ACTIONS ==========\n")

result = extract_actions_from_chunks(chunks)

print(result.model_dump_json(indent=4))