
import os

from dotenv import load_dotenv
from google import genai

from src.retrieval import search_book

# Load the API key from the project's .env file
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Add it to your .env file."
    )

client = genai.Client(api_key=API_KEY)
# client = genai.Client(
#     api_key=API_KEY,
#     http_options={"timeout": 60000},
# )

# def answer_question(question: str, top_k: int = 5) -> dict:
def answer_question(question: str, top_k: int = 3) -> dict:
    """Answer a question using relevant passages from the book."""

    # Step 1: Retrieve relevant book passages
    # passages = search_book(question, top_k=top_k)
    import time

    start = time.time()
    print("1. Searching book...", flush=True)

    passages = search_book(question, top_k=top_k)

    print(
        f"2. Retrieval finished in {time.time() - start:.1f}s",
        flush=True,
    )

        if not passages:
            return {
                "answer": "I couldn't find relevant passages in the book.",
                "sources": [],
            }

    # Step 2: Prepare the source text for Gemini
    context = "\n\n".join(
        f"[Book page {item['page']}]\n{item['text']}"
        for item in passages
    )

    # Step 3: Tell Gemini to answer using the book evidence
    prompt = f"""
You are IncidentLens, a book-grounded incident response assistant.

Answer the user's question using ONLY the source passages below.

Rules:
- Use clear, beginner-friendly language.
- Cite supporting passages using [p. NUMBER].
- Do not invent facts or page numbers.
- If the passages don't contain enough information, say so.
- Do not claim the book supports something it doesn't say.

SOURCE PASSAGES:
{context}

USER QUESTION:
{question}
"""

    # Step 4: Generate the answer with Gemini
    # response = client.interactions.create(
    #     model="gemini-3.8-flash",
    #     input=prompt,
    # )
    response = client.interactions.create(
    model="gemini-3.8-flash",
    input=prompt,
    timeout=60000,
)

    # Step 5: Return the answer and source passages
    return {
        "answer": (
            response.output_text
            or "No answer was generated."
        ),
        "sources": [
            {
                "page": item["page"],
                "text": item["text"],
            }
            for item in passages
        ],
    }


if __name__ == "__main__":
    question = input("Ask IncidentLens: ").strip()

    if question:
        try:
            result = answer_question(question)

            print("\n--- INCIDENTLENS ANSWER ---\n")
            print(result["answer"])

            print("\n--- SOURCE PAGES ---")
            for source in result["sources"]:
                print(f"\nPage {source['page']}")
                print(source["text"][:250])

        except Exception as error:
            print(f"\nIncidentLens encountered an error: {error}")
