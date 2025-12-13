# edu_diff_engine

Interactive CLI tool + library to generate difficulty- and skill-controlled questions from PDFs using LLMs.

Usage (from project root, venv active):

    python -m edu_diff_engine

You will be prompted for:
- PDF path
- Groq API key (dynamic rubric)
- OpenAI API key (questions)
- Difficulty level (1–5)
- 4 skill sliders: memory, reasoning, numerical, language (0–1, blank = auto)

