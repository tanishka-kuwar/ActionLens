from app.services.action_extraction_service import extract_actions


document = """
Placement Registration Notice

All students must register by 20 September 2026.

Students must upload their updated resume.

Students must carry two printed copies of their resume and college ID.

Students must report at 9:00 AM in Seminar Hall 2.

Only students with an aggregate CGPA above 7.0 are eligible.
"""


result = extract_actions(document)

print("\n========== ACTIONLENS RESULT ==========\n")
print(result.model_dump_json(indent=4))