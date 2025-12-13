from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional

from .pdf_processor import PDFProcessor
from .rubric_extractor import RubricExtractor, DynamicRubric
from .question_api import OpenAIQuestionAPI, QuestionRequest, GeneratedQuestion
from .skill_vector import SkillVector


@dataclass
class EngineConfig:
    """
    Configuration for the DifficultyEngine.
    """
    rubric_model: str = "llama-3.3-70b-versatile"   # Groq model for dynamic rubric
    question_model: str = "gpt-4o-mini"             # OpenAI model for questions
    num_questions_total: int = 10                   # total questions across chapter
    num_segments: int = 3                           # early/mid/late conceptual segments
    subject_hint: Optional[str] = None              # e.g., "Mathematics", "Physics", "Chemistry", "Biology"


class DifficultyEngine:
    """
    High-level orchestrator:
    - reads PDF,
    - builds dynamic rubric using Groq (global + question design rubrics),
    - splits PDF into conceptual segments (early/mid/late),
    - generates questions per segment using OpenAI (or compatible),
    - returns a merged list of questions that cover the entire chapter.
    """

    def __init__(self, config: Optional[EngineConfig] = None):
        self.config = config or EngineConfig()
        self.pdf_processor = PDFProcessor()

    # -----------------------------
    # Internal: segmenting the PDF
    # -----------------------------
    def _segment_pdf(self, text: str, num_segments: int) -> List[str]:
        """
        Split the full PDF text into `num_segments` contiguous segments.
        These roughly correspond to early/mid/late parts of the chapter.
        """
        length = len(text)
        if length == 0 or num_segments <= 1:
            return [text]

        seg_size = max(1, length // num_segments)
        segments = []
        for i in range(num_segments):
            start = i * seg_size
            end = length if i == num_segments - 1 else (i + 1) * seg_size
            segments.append(text[start:end])
        return segments

    def _segment_tags(self, num_segments: int) -> List[str]:
        """
        Return human-readable tags for segments.
        For 3 segments: ['early', 'mid', 'late'].
        Otherwise: ['segment_1', 'segment_2', ...].
        """
        if num_segments == 3:
            return ["early", "mid", "late"]
        return [f"segment_{i+1}" for i in range(num_segments)]

    def _question_distribution(self, total: int, num_segments: int) -> List[int]:
        """
        Split 'total' questions as evenly as possible across segments.
        Example: total=10, num_segments=3 -> [4,3,3] or [3,3,4] etc.
        """
        base = total // num_segments
        rem = total % num_segments
        counts = []
        for i in range(num_segments):
            extra = 1 if i < rem else 0
            counts.append(base + extra)
        return counts

    # -----------------------------
    # Public API
    # -----------------------------
    def generate_questions(
        self,
        pdf_path: str,
        rubric_api_key: str,
        question_api_key: str,
        difficulty_level: int,
        skill_vector: SkillVector,
    ) -> List[GeneratedQuestion]:
        """
        Main entry point:
        - builds dynamic rubric for the entire PDF,
        - splits PDF into segments,
        - generates questions for each segment,
        - merges them into a single list.
        """

        if not (1 <= difficulty_level <= 5):
            raise ValueError("difficulty_level must be between 1 and 5.")

        # 1) Extract full text from PDF
        pdf_text = self.pdf_processor.extract_text(pdf_path)

        # 2) Build dynamic rubric using Groq, based on full chapter
        rubric_extractor = RubricExtractor(
            api_key=rubric_api_key,
            model=self.config.rubric_model,
        )
        dynamic_rubric: DynamicRubric = rubric_extractor.build_dynamic_rubric(
            pdf_text,
            subject_hint=self.config.subject_hint,
        )

        # 3) Split PDF into segments (early/mid/late)
        segments = self._segment_pdf(pdf_text, self.config.num_segments)
        segment_tags = self._segment_tags(self.config.num_segments)
        per_segment_counts = self._question_distribution(
            self.config.num_questions_total,
            self.config.num_segments,
        )

        # 4) Prepare request template
        base_request = QuestionRequest(
            difficulty_level=difficulty_level,
            skill_vector=skill_vector,
            num_questions=0,  # will set per segment
        )

        # 5) Question API client
        question_api = OpenAIQuestionAPI(
            api_key=question_api_key,
            model=self.config.question_model,
            subject_hint=self.config.subject_hint,
        )

        all_questions: List[GeneratedQuestion] = []

        # 6) Generate questions per segment
        for segment_text, seg_tag, n_q in zip(segments, segment_tags, per_segment_counts):
            if n_q <= 0:
                continue

            req = QuestionRequest(
                difficulty_level=base_request.difficulty_level,
                skill_vector=base_request.skill_vector,
                num_questions=n_q,
            )

            segment_questions = question_api.generate_questions_for_segment(
                segment_text=segment_text,
                dynamic_rubric=dynamic_rubric,
                request=req,
                segment_tag=seg_tag,
            )
            all_questions.extend(segment_questions)

        return all_questions

