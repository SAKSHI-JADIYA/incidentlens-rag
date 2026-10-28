# 🛡️ IncidentLens — Book-Grounded Incident Response Assistant

IncidentLens is a Retrieval-Augmented Generation (RAG) application that helps users explore cybersecurity incident response concepts through a book-grounded AI assistant.

Instead of relying only on an LLM's general knowledge, IncidentLens retrieves relevant passages from *Dynamic Incident Response: A Framework for Security Teams* by Joshua Wright and uses them to generate answers with page citations.

## Why I Built This

Recent cyber incidents have highlighted how important it is for organizations to respond to security threats effectively. Detecting a threat is only one part of the challenge; teams also need structured incident response processes, clear communication, coordination, and proper documentation.

I chose *Dynamic Incident Response: A Framework for Security Teams* because I wanted to understand how incident response works beyond theory and explore how established cybersecurity knowledge can be made easier to access.

This project combines that learning goal with practical AI implementation: **using RAG to turn a cybersecurity reference book into an interactive, source-grounded learning tool.**

## ✨ Features

- **Book-based question answering:** Ask questions about incident response concepts covered in the reference book.
- **Semantic retrieval:** Uses sentence embeddings to find passages relevant to a user's question.
- **Grounded AI responses:** Uses Google's Gemini model to generate answers based on retrieved passages.
- **Page citations:** Answers can cite relevant book pages, making it easier to verify the information.
- **Source inspection:** Expand the source sections in the interface to read the passages used to generate an answer.
- **Persistent vector index:** Stores book embeddings in ChromaDB so the index does not need to be rebuilt for every question.
- **Interactive interface:** A Streamlit web app for submitting questions and reviewing answers.

## 🧠 How It Works

IncidentLens follows a Retrieval-Augmented Generation pipeline.

```text
                  Reference Book (PDF)
                           |
                           v
                    Text Extraction
                           |
                           v
                      Text Chunking
                           |
                           v
                 Sentence Embeddings
                           |
                           v
                  ChromaDB Vector Index
                           |
                           v
                     User Question
                           |
                           v
                  Semantic Retrieval
                           |
                           v
                 Relevant Source Passages
                           |
                           v
                    Gemini LLM
                           |
                           v
                 Answer + Page Citations
                           |
                           v
                    Streamlit UI
```

### Pipeline Overview

1. **Text extraction:** Extracts readable text from the PDF using PyPDF.
2. **Chunking:** Splits the extracted text into smaller overlapping passages to support retrieval.
3. **Embedding generation:** Converts passages into numerical representations using the `all-MiniLM-L6-v2` sentence-transformer model.
4. **Vector storage:** Stores passage embeddings and page metadata in ChromaDB.
5. **Semantic retrieval:** Searches for passages relevant to the user's question.
6. **Answer generation:** Sends the retrieved passages and question to Gemini with instructions to stay grounded in the provided context.
7. **Source verification:** Displays the generated answer alongside the retrieved book passages and their page numbers.

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Language | Python |
| User interface | Streamlit |
| PDF text extraction | PyPDF |
| Embeddings | Sentence Transformers |
| Vector database | ChromaDB |
| LLM | Google Gemini via `google-genai` |
| Configuration | `python-dotenv` |

## 📚 Reference Book

**Title:** *Dynamic Incident Response: A Framework for Security Teams*  
**Author:** Joshua Wright

The book was selected to explore incident response practices, including how security teams approach incidents, coordinate their work, communicate effectively, and document response activities.

The application is intended as a learning and information-retrieval aid, not a replacement for professional incident response procedures.

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or a compatible Python version
- Git
- A Google Gemini API key
- The reference PDF, which is not included in this repository

### 1. Clone the Repository

```bash
git clone https://github.com/SAKSHI-JADIYA/incidentlens-rag.git
cd incidentlens-rag
```

### 2. Create and Activate a Virtual Environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use the Python executable inside the environment directly or adjust your local execution policy as appropriate.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API Key

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_api_key_here
```

Replace the placeholder with your own key. Keep `.env` private and never commit it to GitHub.

### 5. Add the Reference PDF

Place your legally obtained copy of the reference book at:

```text
data/book.pdf
```

The PDF is kept outside the repository to avoid distributing copyrighted material.

### 6. Prepare the Book Index

Run the project's existing PDF extraction and chunking scripts in the order defined by their filenames or instructions. These steps produce the extracted text and chunk data used by retrieval.

Once `data/chunks.json` has been generated, build the vector index:

```powershell
.\.venv\Scripts\python.exe -m src.retrieval
```

The vector index is stored locally under `data/chroma_db`.

### 7. Launch the Application

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open the local URL shown in the terminal by Streamlit.

> **Note:** The setup assumes the extraction and chunking scripts in the repository generate the expected files. If you use a differently named virtual environment, replace `.venv` in the commands with its path.

## 💬 Example Questions

Try asking:

- How should a security team respond to an incident?
- What are the main responsibilities of an incident response team?
- Why is documentation important during incident response?
- How should responders communicate with management during an incident?
- What is the role of management during an incident?

You can also ask questions outside the book's scope to evaluate whether the application appropriately acknowledges when the retrieved evidence is insufficient.

## 📁 Project Structure

```text
incidentlens-rag/
├── app.py                  # Streamlit application
├── src/
│   ├── retrieval.py        # Vector index and semantic search
│   └── answer.py           # RAG pipeline and answer generation
├── data/
│   ├── book.pdf            # Local reference PDF (not committed)
│   ├── chunks.json         # Extracted text chunks (not committed)
│   └── chroma_db/          # Persistent vector index (not committed)
├── requirements.txt        # Python dependencies
├── .gitignore
└── README.md
```

The exact extraction and chunking filenames may vary depending on the current implementation.

## 🔒 Limitations

- Answers depend on the quality and relevance of the retrieved passages.
- Page citations and source passages should be checked before relying on an answer.
- The system may produce incomplete or inaccurate answers despite its grounding instructions.
- The application is limited to the content available in the indexed book; it does not independently verify live cyber incident reports.
- Gemini API access requires a valid API key and network connectivity.
- IncidentLens is an educational prototype, not an operational incident response or security monitoring system.

## 🔮 Potential Improvements

- Add automated evaluation for retrieval relevance and answer faithfulness.
- Improve handling of questions that cannot be answered from the book.
- Add source-relevance scores and more transparent retrieval diagnostics.
- Support multiple cybersecurity reference documents.
- Add automated tests for retrieval, source attribution, and answer generation.

## 🎯 What I Learned

Building IncidentLens gave me practical experience with:

- Implementing a RAG pipeline from document ingestion to answer generation.
- Extracting, chunking, and indexing PDF content.
- Using embeddings and vector search for semantic retrieval.
- Integrating a hosted LLM API into a Python application.
- Displaying source passages to make AI-generated answers easier to verify.
- Structuring a small Python project and building a user-facing interface with Streamlit.

---

**IncidentLens — Making cybersecurity knowledge easier to explore, one source-grounded answer at a time.**
