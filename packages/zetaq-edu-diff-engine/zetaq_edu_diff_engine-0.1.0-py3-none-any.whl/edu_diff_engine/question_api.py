from __future__ import annotations
import json
from dataclasses import dataclass
from typing import List, Optional

from .skill_vector import SkillVector
from .static_rubric import STATIC_RUBRIC_TEXT
from .static_question_rubric import QUESTION_DESIGN_RUBRIC_TEXT
from .rubric_extractor import DynamicRubric


@dataclass
class QuestionRequest:
    """
    Parameters that control question generation from the PDF.
    """
    difficulty_level: int          # 1–5, local to this PDF
    skill_vector: SkillVector      # (memory, reasoning, numerical, language)
    num_questions: int = 10        # number of MCQs to generate


@dataclass
class GeneratedQuestion:
    """
    Final question structure used by the engine and CLI.
    """
    text: str
    options: list[str]
    correct_index: int
    explanation: str


class OpenAIQuestionAPI:
    """
    Uses the OpenAI Python client (v2.x) to generate MCQs as JSON.
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o-mini",
        subject_hint: Optional[str] = None,
    ):
        self.api_key = api_key
        self.model = model
        self.subject_hint = subject_hint or "Other"

    # ------------------------
    # Helper: subject bias
    # ------------------------
    def _subject_bias_text(self) -> str:
        """
        Subject-specific high-level instructions.
        """
        if self.subject_hint in ("Mathematics", "Physics"):
            return """
SUBJECT BIAS:
- Treat this as a Mathematics/Physics exam chapter when the content and formulas support it.
- Prioritise questions that USE formulas, equations, and explicit numerical values from the PDF.
"""
        if self.subject_hint == "Chemistry":
            return """
SUBJECT BIAS:
- Treat this as a Chemistry chapter.
- Emphasise questions about:
  - reactions and balanced equations,
  - mechanisms,
  - stoichiometry,
  - trends in the periodic table and bonding.
"""
        if self.subject_hint == "Biology":
            return """
SUBJECT BIAS:
- Treat this as a Biology chapter.
- Emphasise:
  - pathways and multi-step processes,
  - structure–function relationships,
  - regulatory mechanisms and feedback,
  - interpretation of diagrams, graphs, and experimental setups.
"""
        return """
SUBJECT BIAS:
- Infer from the PDF whether the content is more quantitative or qualitative.
"""

    # ------------------------
    # Helper: skill constraints
    # ------------------------
    def _skill_constraints_text(self, sv: SkillVector) -> str:
        """
        Convert the numeric skill vector into explicit structural rules
        the LLM must obey when constructing questions.
        """

        # Reasoning complexity rule
        r = sv.reasoning or 0.0
        if r >= 0.8:
            reasoning_rule = (
                "Use HIGH reasoning complexity: the solution path must have at least 3–4 "
                "distinct reasoning steps or combine 3+ concepts."
            )
        elif r >= 0.5:
            reasoning_rule = (
                "Use MEDIUM reasoning complexity: the solution path must have about 2 "
                "clear reasoning steps or combine 2 related concepts."
            )
        else:
            reasoning_rule = (
                "Use LOW reasoning complexity: at most 1 simple reasoning step; mainly "
                "direct recognition or straightforward interpretation."
            )

        # Numerical complexity rule
        n = sv.numerical or 0.0
        if n >= 0.8:
            numeric_rule = (
                "Use HIGH numerical complexity WHEN the subject permits: questions must "
                "require multi-step calculation or algebra, involving at least two different "
                "numbers (including decimals or fractions) or symbolic manipulations."
            )
        elif n >= 0.5:
            numeric_rule = (
                "Use MEDIUM numerical complexity WHEN the subject permits: questions must "
                "require at least one explicit calculation using 1–2 numbers with simple "
                "arithmetic or a single application of a formula."
            )
        else:
            numeric_rule = (
                "Use LOW numerical complexity: avoid any non-trivial calculation. Numbers, "
                "if present, must not require more than trivial comparison or recognition."
            )

        # Language complexity rule
        l = sv.language or 0.0
        if l >= 0.8:
            language_rule = (
                "Use HIGH language complexity: stems may be long, with compound or conditional "
                "sentences and realistic scenarios, but must remain grammatically clear."
            )
        elif l >= 0.5:
            language_rule = (
                "Use MEDIUM language complexity: stems of moderate length with standard exam-style "
                "wording, possibly including one or two clauses."
            )
        else:
            language_rule = (
                "Use LOW language complexity: stems must be short, direct, and simple, with as few "
                "clauses as possible."
            )

        # Memory demand rule
        m = sv.memory or 0.0
        if m >= 0.8:
            memory_rule = (
                "Use HIGH memory demand: questions should require recall of precise terms, sequences, "
                "conditions, or exceptions (e.g., full steps of a process, specific values or labels)."
            )
        elif m >= 0.5:
            memory_rule = (
                "Use MEDIUM memory demand: questions should require recall of key terms or main steps, "
                "but not rare exceptions or very fine details."
            )
        else:
            memory_rule = (
                "Use LOW memory demand: questions should rely more on interpreting information provided "
                "in the stem or general understanding, with minimal pure recall."
            )

        return f"""
MANDATORY SKILL CONSTRAINTS (derived from target skill vector):
- Reasoning (target ≈ {r:.2f}):
  {reasoning_rule}

- Numerical (target ≈ {n:.2f}):
  {numeric_rule}

- Language (target ≈ {l:.2f}):
  {language_rule}

- Memory (target ≈ {m:.2f}):
  {memory_rule}

You MUST obey these constraints strictly when designing each question and its explanation.
If any draft question violates these constraints, you must internally correct and adjust it
BEFORE returning the final JSON.
"""

    # ------------------------
    # Helper: build prompt
    # ------------------------
    def _build_prompt(
        self,
        segment_text: str,
        dynamic_rubric: DynamicRubric,
        request: QuestionRequest,
        segment_tag: str,
    ) -> str:
        subject_bias = self._subject_bias_text()
        numeric_target = request.skill_vector.numerical or 0.0

        hard_numeric_math_phys = (
            self.subject_hint in ("Mathematics", "Physics") and numeric_target >= 0.7
        )
        hard_numeric_chem = (
            self.subject_hint == "Chemistry" and numeric_target >= 0.6
        )

        if hard_numeric_math_phys:
            mode_text = f"""
HARD NUMERIC MODE (Mathematics/Physics):

- numerical skill target ≈ {numeric_target:.2f} (high).
- ALL questions MUST require explicit numerical calculation or algebraic manipulation.
- Every question stem MUST contain at least one explicit numerical value (e.g., 2, 3.5, 10^3, etc.)
  or a parameter that is given a specific value.
- It must NOT be possible to answer correctly using pure conceptual recall; the student MUST compute something.
- Questions should use formulas/equations that are actually present in the PDF (or clearly implied examples).
"""
        elif hard_numeric_chem:
            mode_text = f"""
NUMERIC-RICH CHEMISTRY MODE:

- numerical skill target ≈ {numeric_target:.2f} (moderately/high).
- At least HALF of the questions MUST require explicit quantitative reasoning in chemistry, such as:
  - moles, molar mass, stoichiometric ratios,
  - concentrations, equilibrium constants, pH/pOH, etc.
- The remaining questions can focus on reactions, mechanisms, and conceptual trends.
- Any numeric question must use reaction data, constants, or patterns that are consistent with the PDF.
"""
        else:
            mode_text = f"""
BALANCED MODE:

- numerical skill target ≈ {numeric_target:.2f}.
- Use the numeric skill level as a soft guide:
  - If numerical is high (>= 0.5), include a good fraction of questions that require calculation or data interpretation (when the subject permits).
  - If numerical is low (< 0.3), use mostly conceptual questions with only light use of numbers.
"""

        # Skill enforcement rules
        skill_constraints = self._skill_constraints_text(request.skill_vector)

        # For this segment, we can still truncate a bit for safety
        segment_snippet = segment_text[:8000]

        return f"""
You are an expert exam designer.

You must generate multiple-choice questions from a SPECIFIC SEGMENT of a chapter PDF.

GLOBAL DIFFICULTY RUBRIC:
{STATIC_RUBRIC_TEXT}

GLOBAL QUESTION DESIGN RUBRIC:
{QUESTION_DESIGN_RUBRIC_TEXT}

DYNAMIC RUBRIC FOR THIS PDF (includes question pattern library):
{dynamic_rubric.raw_text}

SUBJECT BIAS:
{subject_bias}

TARGET SEGMENT FOR THIS CALL:
- segment_tag = "{segment_tag}"
- This means:
  - You should primarily use topics, examples, and explanations that occur in the {segment_tag} part of the chapter.
  - However, you must remain consistent with the overall chapter structure and dynamic rubric.

TARGET DIFFICULTY:
- LOCAL difficulty level = {request.difficulty_level} (1 = easiest for this PDF, 5 = hardest for this PDF).

TARGET SKILL PROFILE:
- {request.skill_vector.to_prompt_fragment()}

{mode_text}

{skill_constraints}

COVERAGE ROLE OF THIS CALL:
- The engine will combine results from multiple segments (early/mid/late) to cover the entire chapter.
- This call is responsible for producing questions that represent the {segment_tag} region.
- Do NOT reuse the exact same micro-topic for every question; within this segment, cover multiple important subtopics.

CONTENT SOURCE FOR THIS SEGMENT (TRUNCATED SNIPPET):
{segment_snippet}

TASK:
- Generate exactly {request.num_questions} multiple-choice questions FROM THIS SEGMENT of the chapter.

QUESTIONS MUST:
- Obey the GLOBAL DIFFICULTY RUBRIC,
- Obey the GLOBAL QUESTION DESIGN RUBRIC,
- Be consistent with the PDF-specific DYNAMIC RUBRIC,
- Match the requested skill profile as closely as possible,
- Be based on this segment's content, while staying faithful to the chapter,
- Respect ALL MANDATORY SKILL CONSTRAINTS above.

VALIDATION REQUIREMENT FOR EACH QUESTION:
- At the END of each explanation, append a short meta-line like:
  'Skill-check: reasoning_steps = X, numeric_steps = Y, language_complexity = low/medium/high, memory_items = Z.'
- Use this meta-line to self-verify that the question satisfies the skill constraints.
- This meta-line is part of the explanation string and is visible to the user.

OUTPUT FORMAT (strict JSON, no comments, no markdown):

{{
  "questions": [
    {{
      "text": "...",
      "options": ["...", "...", "...", "..."],
      "correct_index": 0,
      "explanation": "...",
      "skill_vector": {{
        "memory": 0.0,
        "reasoning": 0.0,
        "numerical": 0.0,
        "language": 0.0
      }}
    }},
    ...
  ]
}}

Constraints:
- Exactly 4 options per question.
- correct_index is 0-based index in the options list.
- Explanation should show the reasoning and why other options are wrong, and end with the 'Skill-check' meta-line.
- skill_vector fields in the output should be in [0, 1] and approximate the true cognitive load.
"""

    # ------------------------
    # Main: call OpenAI and parse
    # ------------------------
    def generate_questions_for_segment(
        self,
        segment_text: str,
        dynamic_rubric: DynamicRubric,
        request: QuestionRequest,
        segment_tag: str,
    ) -> List[GeneratedQuestion]:
        """
        Call OpenAI chat.completions API for a specific PDF segment
        and convert JSON into a list of GeneratedQuestion.
        """
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError(
                "openai package not installed. Run `pip install openai` inside your venv."
            ) from exc

        client = OpenAI(api_key=self.api_key)

        prompt = self._build_prompt(segment_text, dynamic_rubric, request, segment_tag)

        completion = client.chat.completions.create(
            model=self.model,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert exam designer who returns ONLY valid JSON.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        try:
            raw_text = completion.choices[0].message.content
        except Exception as exc:
            raise RuntimeError(
                f"Failed to extract text from OpenAI chat completion: {exc}"
            ) from exc

        try:
            payload = json.loads(raw_text)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "Failed to parse model output as JSON. "
                f"Raw text was:\n{raw_text}"
            ) from exc

        questions_raw = payload.get("questions", [])
        result: List[GeneratedQuestion] = []

        for q in questions_raw:
            text = (q.get("text") or "").strip()
            options = q.get("options") or []
            correct_index = int(q.get("correct_index", 0))
            explanation = (q.get("explanation") or "").strip()

            if not text or len(options) != 4:
                continue

            result.append(
                GeneratedQuestion(
                    text=text,
                    options=list(options),
                    correct_index=correct_index,
                    explanation=explanation,
                )
            )

        if not result:
            raise RuntimeError(
                f"LLM returned no valid questions for segment '{segment_tag}'. Raw JSON:\n{payload}"
            )

        return result

