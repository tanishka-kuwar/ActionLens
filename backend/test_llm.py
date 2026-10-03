from app.services.llm_service import generate_response


prompt = """
Explain in one sentence what a document action extraction system does.
"""

response = generate_response(prompt)

print(response)