# ActionLens

### Turn complicated documents into clear, actionable next steps.

ActionLens is an AI-powered document intelligence platform that transforms unstructured documents into structured, actionable information.

Instead of simply summarizing a document, ActionLens identifies:

- Actions a user needs to perform
- Deadlines and important dates
- Responsible parties
- Required documents
- Eligibility conditions
- Warnings and consequences
- Evidence supporting each extracted action
- Source document and page information

ActionLens uses Retrieval-Augmented Generation (RAG) to retrieve the most relevant parts of a document before sending them to an LLM for structured action extraction.

---

## Problem

Important instructions are often buried inside long and complicated documents such as:

- College notices
- Placement announcements
- Internship documents
- Government notices
- HR policies
- Agreements
- Forms
- Application instructions
- Business documents

A simple summary does not answer the questions users actually care about:

> What do I need to do?

> By when?

> What documents do I need?

> Who is responsible?

> What are the eligibility conditions?

> Where exactly does the document say this?

ActionLens is designed to answer these questions in a structured way.

---

## Key Features

### 1. Multi-format Document Processing

Currently supports:

- PDF
- DOCX
- TXT

PDF documents are processed page-by-page so extracted information can retain page-level evidence.

---

### 2. Document Cleaning and Chunking

Extracted document text is cleaned and divided into manageable chunks.

The chunking process uses paragraph-aware splitting and overlap to preserve useful context for semantic retrieval.

---

### 3. Semantic Search with Embeddings

ActionLens uses:

- Sentence Transformers
- `all-MiniLM-L6-v2`

to convert document chunks and retrieval queries into vector representations.

---

### 4. FAISS Vector Search

FAISS is used for efficient semantic similarity search.

The current implementation uses:

- FAISS `IndexFlatIP`
- L2-normalized vectors
- Cosine similarity through inner-product search

Retrieved chunks are deduplicated and globally ranked by similarity score.

---

### 5. Retrieval-Augmented Generation

Instead of sending an entire document directly to the LLM, ActionLens:

1. Processes the document
2. Creates chunks
3. Generates embeddings
4. Retrieves relevant chunks
5. Ranks the retrieved content
6. Sends the relevant evidence to the LLM
7. Produces structured output

This reduces irrelevant context and focuses extraction on information related to actions, deadlines, requirements, eligibility, and warnings.

---

### 6. Structured Action Extraction

The LLM extracts information into a structured schema containing:

- Action
- Deadline
- Responsible party
- Required documents
- Consequence
- Evidence
- Eligibility conditions
- Warnings

Example:

```json
{
  "actions": [
    {
      "action": "Register",
      "deadline": "20 September 2026",
      "responsible_party": "All students",
      "required_documents": [],
      "consequence": null,
      "evidence": {
        "text": "All students must register by 20 September 2026.",
        "source": "Placement Registration Notice.pdf",
        "page": 1
      }
    }
  ],
  "eligibility_conditions": [
    "Only students with an aggregate CGPA above 7.0 are eligible."
  ],
  "warnings": []
}

```
---
### 7. Evidence Grounding

ActionLens is designed to ground extracted actions in the original document.

Each extracted action can include:

Evidence text
Source document
Page number for PDF documents

The system also instructs the LLM to use only the supplied evidence and avoid inventing deadlines, page numbers, or other information.

---

### 8. UI-Aware Action Detection

ActionLens does not automatically treat every imperative-looking word as a real user obligation.

For example, interface labels such as:

LOGIN
SUBMIT
COMMENT
RATE
LOGOUT

are not automatically extracted as actions.

The system attempts to identify meaningful instructions and obligations from surrounding context.

---

### System Architecture
                    ┌─────────────────────┐
                    │   Document Upload   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Document Extraction │
                    │   PDF / DOCX / TXT  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Text Cleaning     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Chunk Generation    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Embeddings       │
                    │ Sentence Transformer│
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   FAISS Vector      │
                    │       Search        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Semantic Retrieval  │
                    │ + Global Ranking    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Gemini LLM       │
                    │ Structured Extraction│
                    └──────────┬──────────┘
                               │
                               ▼
              ┌─────────────────────────────────┐
              │       ActionLens Output         │
              ├─────────────────────────────────┤
              │ Actions                          │
              │ Deadlines                        │
              │ Requirements                     │
              │ Eligibility                      │
              │ Warnings                         │
              │ Evidence                         │
              │ Source + Page                    │
              └─────────────────────────────────┘

---

### Tech Stack
Backend
Python
FastAPI
Pydantic
AI / NLP
Google Gemini API
Sentence Transformers
all-MiniLM-L6-v2
Retrieval
FAISS
Semantic similarity search
Retrieval-Augmented Generation (RAG)
Document Processing
PyMuPDF
python-docx
Development
VS Code
Git
GitHub
Python virtual environment
Project Structure
ActionLens/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── action_schema.py
│   │   │   ├── chunk_schema.py
│   │   │   └── document_schema.py
│   │   │
│   │   └── services/
│   │       ├── action_extraction_service.py
│   │       ├── chunk_metadata_service.py
│   │       ├── chunk_service.py
│   │       ├── document_service.py
│   │       ├── embedding_service.py
│   │       ├── llm_service.py
│   │       ├── rag_service.py
│   │       ├── text_service.py
│   │       └── vector_service.py
│   │
│   ├── requirements.txt
│   │
│   └── test_*.py
│
├── frontend/
│
├── data/
│
├── tests/
│
├── .gitignore
├── README.md
└── venv/

---

### API

The backend currently exposes FastAPI endpoints for document processing and action extraction.

Interactive API documentation is available through Swagger UI when the application is running:

http://127.0.0.1:8000/docs
Main Action Extraction Endpoint
POST /extract-actions

This endpoint accepts a supported document and returns structured action information.

----

### Running Locally
1. Clone the repository
git clone https://github.com/tanishka-kuwar/ActionLens.git
cd ActionLens
2. Create a virtual environment
python -m venv venv
3. Activate the virtual environment

Windows PowerShell:
venv\Scripts\Activate.ps1
4. Install dependencies
pip install -r backend/requirements.txt
5. Configure environment variables

Create:
backend/.env

Add your Gemini API key:
GEMINI_API_KEY=your_api_key_here
Do not commit .env to GitHub.

6. Start the FastAPI server
python -m uvicorn backend.app.main:app --reload

Open:
http://127.0.0.1:8000/docs
