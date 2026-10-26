
from pathlib import Path
import json
from pypdf import PdfReader

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = PROJECT_ROOT / "data" / "book.pdf"
OUTPUT_PATH = PROJECT_ROOT / "data" / "extracted_pages.json"


def extract_pages():
    if not PDF_PATH.exists():
        raise FileNotFoundError(
            f"Book PDF not found at: {PDF_PATH}"
        )

    reader = PdfReader(str(PDF_PATH))
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()

        if text:
            pages.append({
                "page": page_number,
                "text": text
            })

    OUTPUT_PATH.write_text(
        json.dumps(pages, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"Total PDF pages: {len(reader.pages)}")
    print(f"Pages with extracted text: {len(pages)}")
    print(f"Saved extracted text to: {OUTPUT_PATH}")


if __name__ == "__main__":
    extract_pages()
