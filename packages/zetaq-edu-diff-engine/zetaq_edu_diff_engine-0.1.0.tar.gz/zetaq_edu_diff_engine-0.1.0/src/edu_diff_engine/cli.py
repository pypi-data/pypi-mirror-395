from __future__ import annotations
from getpass import getpass
from typing import Optional

from .engine import DifficultyEngine, EngineConfig
from .skill_vector import SkillVector


def _ask_float_0_1(prompt: str) -> Optional[float]:
    """
    Ask for a float in [0,1]. If user hits Enter, returns None (auto).
    """
    while True:
        raw = input(prompt).strip()
        if raw == "":
            return None
        try:
            val = float(raw)
        except ValueError:
            print("Please enter a number between 0 and 1, or leave blank for auto.")
            continue
        if 0.0 <= val <= 1.0:
            return val
        print("Value must be between 0 and 1, or blank for auto.")


def _ask_int_1_5(prompt: str) -> int:
    """
    Ask for an integer in [1,5].
    """
    while True:
        raw = input(prompt).strip()
        try:
            val = int(raw)
        except ValueError:
            print("Please enter an integer between 1 and 5.")
            continue
        if 1 <= val <= 5:
            return val
        print("Value must be between 1 and 5.")


def _ask_subject_hint() -> str:
    """
    Ask the user which subject this PDF belongs to.
    This controls bias: math/physics → numerical, chemistry → reactions + numericals.
    """
    print("\nSubject of this PDF?")
    print("  1) Mathematics")
    print("  2) Physics")
    print("  3) Chemistry")
    print("  4) Other / Mixed")

    mapping = {
        "1": "Mathematics",
        "2": "Physics",
        "3": "Chemistry",
        "4": "Other",
    }

    while True:
        choice = input("Choose 1–4 (default = Other): ").strip()
        if choice == "":
            return "Other"
        if choice in mapping:
            return mapping[choice]
        print("Please enter 1, 2, 3, or 4.")


def main() -> None:
    print("\n=== edu_diff_engine – PDF Difficulty & Skill Aware Question Generator ===\n")

    # 1) PDF path
    pdf_path = input("PDF file path: ").strip()
    if not pdf_path:
        print("PDF path is required. Exiting.")
        return

    # 2) Subject hint (Math / Physics / Chemistry / Other)
    subject_hint = _ask_subject_hint()

    # 3) API keys
    print("\nEnter API keys (they are NOT stored anywhere):")
    rubric_api_key = getpass("  Groq API key (for dynamic rubric): ").strip()
    question_api_key = getpass("  OpenAI (or compatible) API key (for questions): ").strip()

    if not rubric_api_key or not question_api_key:
        print("Both API keys are required. Exiting.")
        return

    # 4) Difficulty
    print("\nDifficulty settings:")
    difficulty_level = _ask_int_1_5("  Target difficulty level (1–5, local to PDF): ")

    # 5) Skill sliders
    print("\nSkill profile (0–1). Leave blank for auto in that dimension.")
    memory = _ask_float_0_1("  Memory (0–1, blank = auto): ")
    reasoning = _ask_float_0_1("  Reasoning (0–1, blank = auto): ")
    numerical = _ask_float_0_1("  Numerical (0–1, blank = auto): ")
    language = _ask_float_0_1("  Language (0–1, blank = auto): ")

    skill_vector = SkillVector(
        memory=memory,
        reasoning=reasoning,
        numerical=numerical,
        language=language,
    )

    # 6) Build engine with subject hint
    config = EngineConfig(subject_hint=subject_hint)
    engine = DifficultyEngine(config=config)

    print("\nGenerating questions... this will call the rubric LLM and question LLM.\n")

    try:
        questions = engine.generate_questions(
            pdf_path=pdf_path,
            rubric_api_key=rubric_api_key,
            question_api_key=question_api_key,
            difficulty_level=difficulty_level,
            skill_vector=skill_vector,
        )
    except Exception as exc:
        print(f"\n[ERROR] Failed to generate questions: {exc}")
        return

    print(f"\nGenerated {len(questions)} questions:\n")
    for i, q in enumerate(questions, start=1):
        print(f"Q{i}. {q.text}\n")
        for idx, opt in enumerate(q.options):
            label = chr(ord("A") + idx)
            print(f"   {label}) {opt}")
        print(f"\n   Correct option index (0-based): {q.correct_index}")
        print(f"   Explanation: {q.explanation}\n")
        print("-" * 80)


if __name__ == "__main__":
    main()

