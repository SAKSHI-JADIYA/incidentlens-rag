
import json
from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import (
    SentenceTransformerEmbeddingFunction,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHUNKS_PATH = PROJECT_ROOT / "data" / "chunks.json"
DB_PATH = PROJECT_ROOT / "data" / "chroma_db"

COLLECTION_NAME = "incidentlens_book"
MODEL_NAME = "all-MiniLM-L6-v2"


def build_index():
    """Build a persistent vector index from the book's chunks."""
    if not CHUNKS_PATH.exists():
        raise FileNotFoundError(
            f"Chunks file not found: {CHUNKS_PATH}. "
            "Run the chunking step first."
        )

    with CHUNKS_PATH.open("r", encoding="utf-8") as file:
        chunks = json.load(file)

    if not chunks:
        raise ValueError("No chunks found in chunks.json")

    client = chromadb.PersistentClient(path=str(DB_PATH))
    embedding_function = SentenceTransformerEmbeddingFunction(
        model_name=MODEL_NAME
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function,
        metadata={"hnsw:space": "cosine"},
    )

    # Add only chunks that aren't already indexed.
    existing_ids = set()
    for start in range(0, collection.count(), 500):
        batch = collection.get(
            limit=500,
            offset=start,
            include=[],
        )
        existing_ids.update(batch["ids"])

    new_chunks = [
        chunk for chunk in chunks
        if chunk["chunk_id"] not in existing_ids
    ]

    for start in range(0, len(new_chunks), 100):
        batch = new_chunks[start:start + 100]
        collection.upsert(
            ids=[item["chunk_id"] for item in batch],
            documents=[item["text"] for item in batch],
            metadatas=[
                {"page": int(item["page"])}
                for item in batch
            ],
        )

    print(f"Total chunks in source: {len(chunks)}")
    print(f"New chunks indexed: {len(new_chunks)}")
    print(f"Total chunks in index: {collection.count()}")
    print(f"Index location: {DB_PATH}")


def search_book(question, top_k=5):
    """Return the most relevant book chunks for a question."""
    if not question or not question.strip():
        raise ValueError("Question cannot be empty")

    client = chromadb.PersistentClient(path=str(DB_PATH))
    embedding_function = SentenceTransformerEmbeddingFunction(
        model_name=MODEL_NAME
    )

    collection = client.get_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function,
    )

    if collection.count() == 0:
        return []

    results = collection.query(
        query_texts=[question],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    matches = []
    for text, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        matches.append({
            "text": text,
            "page": metadata["page"],
            "distance": distance,
        })

    return matches


if __name__ == "__main__":
    build_index()
    print("\nTest search:")
    for result in search_book(
        "How should a security team respond to an incident?"
    ):
        print(f"\nPage {result['page']} | distance={result['distance']:.3f}")
        print(result["text"][:350])
