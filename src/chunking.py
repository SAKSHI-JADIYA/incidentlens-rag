
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_PATH = PROJECT_ROOT / "data" / "extracted_pages.json"
OUTPUT_PATH = PROJECT_ROOT / "data" / "chunks.json"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


def split_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be between 0 and chunk_size")

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))

        # Prefer ending at a word boundary.
        if end < len(text):
            boundary = text.rfind(" ", start, end)
            if boundary > start:
                end = boundary

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = max(end - overlap, start + 1)

    return chunks


def create_chunks():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Extracted pages not found: {INPUT_PATH}"
        )

    pages = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
    all_chunks = []

    for page in pages:
        for index, text in enumerate(split_text(page["text"])):
            all_chunks.append({
                "chunk_id": f"page-{page['page']}-chunk-{index}",
                "page": page["page"],
                "text": text
            })

    OUTPUT_PATH.write_text(
        json.dumps(all_chunks, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"Pages processed: {len(pages)}")
    print(f"Chunks created: {len(all_chunks)}")
    print(f"Saved chunks to: {OUTPUT_PATH}")

    if all_chunks:
        print("\nExample chunk:")
        print(all_chunks[0]["text"][:300])


if __name__ == "__main__":
    create_chunks()
