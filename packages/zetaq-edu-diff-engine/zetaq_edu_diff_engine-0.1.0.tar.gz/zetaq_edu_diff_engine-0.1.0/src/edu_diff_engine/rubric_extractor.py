from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from .static_rubric import STATIC_RUBRIC_TEXT
from .static_question_rubric import QUESTION_DESIGN_RUBRIC_TEXT


@dataclass
class DynamicRubric:
    """
    Holds the dynamic, PDF-specific rubric text returned by the Groq model.
    """
    raw_text: str


def _build_coverage_snippet(pdf_text: str, max_chars: int = 24000, segments: int = 3) -> str:
    """
    Build a coverage-aware snippet that samples from early, middle, and late
    parts of the PDF text, so the model sees the whole chapter structure.
    """
    text = pdf_text
    length = len(text)
    if length <= max_chars:
        # Whole text fits, just return it
        return text

    # Split into 'segments' conceptual zones (early/mid/late)
    snippet_parts = []
    # How many chars per sampled segment
    per_seg_chars = max_chars // segments

    for i in range(segments):
        # Conceptual segment position in the original
        start_global = (length * i) // segments
        end_global = min(length, start_global + per_seg_chars)
        seg_label = ["EARLY", "MID", "LATE"][i] if segments == 3 else f"SEGMENT_{i+1}"
        seg_text = text[start_global:end_global]
        snippet_parts.append(f"[{seg_label} SEGMENT]\n{seg_text}")

    return "\n\n".join(snippet_parts)


class RubricExtractor:
    """
    Uses a Groq model (or compatible chat model) to build a PDF-specific dynamic rubric.

    It takes the global STATIC_RUBRIC_TEXT as a baseline and adapts it
    to the actual content of the PDF.
    """

    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        self.api_key = api_key
        self.model = model

    def build_dynamic_rubric(self, pdf_text: str, subject_hint: Optional[str] = None) -> DynamicRubric:
        """
        Returns a DynamicRubric object that describes:
        - key concepts,
        - concept difficulty ordering,
        - examples of level 1..5 questions for THIS PDF,
        - how skills (memory, reasoning, numerical, language) should be adjusted,
        - a QUESTION PATTERN LIBRARY with at least 40 patterns.
        """
        try:
            from groq import Groq
        except ImportError as exc:
            raise RuntimeError(
                "groq package not installed. Run `pip install groq` inside your venv."
            ) from exc

        client = Groq(api_key=self.api_key)

        subject_text = subject_hint or "Unknown / mixed"

        system_msg = (
            "You are an educational measurement expert. "
            "You design difficulty rubrics and question pattern libraries for exam questions from textbooks and PDFs.\n\n"
            "IMPORTANT:\n"
            "- You MUST treat the provided GLOBAL DIFFICULTY RUBRIC as the definition of difficulty levels 1–5.\n"
            "- You MUST treat the GLOBAL QUESTION DESIGN RUBRIC as the definition of good MCQ design and coverage.\n"
            "- Your job is to ADAPT these global rubrics to THIS specific PDF, not to invent a new scale.\n"
        )

        pdf_snippet = _build_coverage_snippet(pdf_text, max_chars=24000, segments=3)

        user_msg = (
            f"SUBJECT HINT: {subject_text}\n\n"
            "GLOBAL DIFFICULTY RUBRIC (STATIC):\n"
            f"{STATIC_RUBRIC_TEXT}\n\n"
            "GLOBAL QUESTION DESIGN RUBRIC (STATIC):\n"
            f"{QUESTION_DESIGN_RUBRIC_TEXT}\n\n"
            "PDF CONTENT (COVERAGE-AWARE SNIPPET; includes EARLY/MID/LATE segments):\n"
            f"{pdf_snippet}\n\n"
            "TASK:\n"
            "1. Identify key concepts, definitions, formulas, reactions, worked examples, and typical problem types in this PDF.\n"
            "   - Explicitly note which topics belong to EARLY, MID, and LATE parts of the chapter.\n"
            "2. Order concepts from easiest/basic to hardest/advanced.\n"
            "3. Using the GLOBAL DIFFICULTY RUBRIC as the master scale, define LOCAL difficulty bands for levels 1–5 for THIS PDF only.\n"
            "   - Level 1 = easiest meaningful questions from this PDF.\n"
            "   - Level 5 = hardest plausible questions from this PDF.\n"
            "4. For each level (1–5), specify clearly:\n"
            "   - Types of questions (conceptual, numeric, data-interpretation, mechanism/pathway, diagram-based, etc.).\n"
            "   - Typical reasoning depth (number of steps).\n"
            "   - How numerical complexity should scale when the subject allows it.\n"
            "   - How the 4 skills (memory, reasoning, numerical, language) bias compared to the global priors.\n"
            "5. QUESTION PATTERN LIBRARY (MANDATORY):\n"
            "   - Provide AT LEAST 40 distinct question patterns (40 or more bullet points).\n"
            "   - Each pattern MUST be annotated as:\n"
            "       [Lk | skills: M=a..b, R=c..d, N=e..f, Lang=g..h | segment]\n"
            "     where:\n"
            "       - k ∈ {1,2,3,4,5} is the difficulty level,\n"
            "       - a..b etc. are approximate skill ranges in [0,1],\n"
            "       - segment ∈ {early, mid, late}.\n"
            "   - The textual description of each pattern should describe a family of questions which a generator can instantiate.\n"
            "   - Patterns MUST cover topics from EARLY, MID, and LATE parts of the chapter.\n"
            "6. OUTPUT STRUCTURE (HEADINGS):\n"
            "   - Key Concepts by Segment (early/mid/late)\n"
            "   - Difficulty Ladder (how difficulty grows)\n"
            "   - Level Profiles 1–5 (local to this PDF)\n"
            "   - Skill Bias Notes\n"
            "   - Question Pattern Library (≥ 40 patterns as specified above)\n"
            "7. The resulting dynamic rubric must be self-contained and detailed enough that a separate MCQ generator can:\n"
            "   - pick a level and segment,\n"
            "   - pick a target skill vector,\n"
            "   - and instantiate valid MCQs directly from your pattern descriptions.\n"
        )

        chat_completion = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg},
            ],
        )

        content = chat_completion.choices[0].message.content
        return DynamicRubric(raw_text=content)

