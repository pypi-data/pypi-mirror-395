from __future__ import annotations
from pathlib import Path
import pdfplumber


class PDFProcessor:
    """
    Simple PDF text extractor using pdfplumber.

    This is intentionally minimal: we just want a clean text string
    for the rubric and question LLMs to work with.
    """

    def extract_text(self, pdf_path: str | Path) -> str:
        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        pages_text: list[str] = []

        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text() or ""
                    pages_text.append(text)
        except Exception as exc:
            raise RuntimeError(f"Failed to read PDF {pdf_path}: {exc}") from exc

        full_text = "\n\n".join(pages_text).strip()
        if not full_text:
            raise ValueError(f"No text could be extracted from PDF: {pdf_path}")

        return full_text

