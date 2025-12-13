QUESTION_DESIGN_RUBRIC_TEXT = """
GLOBAL QUESTION DESIGN RUBRIC FOR EDU_DIFF_ENGINE
=================================================

Purpose:
- This rubric defines HOW questions should be designed:
  - structure of stems and options,
  - distribution across the chapter (coverage),
  - use of diagrams / data / formulas,
  - mapping to the skill vector S = (memory, reasoning, numerical, language).
- The question generator must obey BOTH:
  (1) the GLOBAL DIFFICULTY RUBRIC, and
  (2) this GLOBAL QUESTION DESIGN RUBRIC,
  while also respecting the PDF-specific DYNAMIC RUBRIC.

----------------------------------------
A. QUESTION STRUCTURE (MCQ FORMAT)
----------------------------------------

1) FORMAT:
   - Each question is a single best-answer multiple-choice question.
   - Exactly 4 options: [A, B, C, D].
   - Exactly ONE option is correct.

2) STEM QUALITY:
   - The stem must:
     - Be clear and unambiguous.
     - Contain all necessary information to answer the question.
     - Not rely on tricky wording, double negatives, or hidden assumptions.
   - Good stems often:
     - Pose a direct question,
     - Or present a short scenario or experimental setup followed by a question.

3) OPTIONS / DISTRACTORS:
   - Options must be:
     - Mutually exclusive (no overlapping meanings),
     - Collectively exhaustive for the intended reasoning space.
   - Wrong options (distractors) must:
     - Correspond to specific, plausible mistakes:
       - misapplied formula,
       - sign error,
       - confusion between similar concepts,
       - incorrect step in a pathway, etc.
     - NOT be silly or obviously impossible.
   - The correct option should not be:
     - systematically longer/shorter than others,
     - obviously more precise while others are vague.

4) EXPLANATION:
   - For each question, the explanation must:
     - Show the full reasoning path from the PDF content to the correct answer.
     - Briefly indicate why each distractor is wrong (if possible).
     - Stay faithful to the notation and conventions of the PDF.

----------------------------------------
B. COVERAGE ACROSS THE CHAPTER
----------------------------------------

Goal:
- A small set of questions (e.g., 10) should still touch the FULL chapter:
  - early/basic topics,
  - middle/intermediate topics,
  - late/advanced topics.

Segment tags:
- We conceptually divide the chapter into:
  - "early"  = first ~1/3 of the content,
  - "mid"    = middle ~1/3 of the content,
  - "late"   = last ~1/3 of the content.

Coverage rules:
- When N questions are generated in total (e.g., N = 10):
  - At least 3–4 questions should be from early topics,
  - At least 3–4 questions should be from mid topics,
  - At least 3–4 questions should be from late topics.
- Each individual API call may target a specific segment:
  - segment_tag ∈ {"early", "mid", "late"}.
  - In that case, the question generator MUST:
    - use content mainly from that segment,
    - but remain consistent with the global PDF context and DYNAMIC RUBRIC.

----------------------------------------
C. USE OF SKILL VECTOR S = (MEMORY, REASONING, NUMERICAL, LANGUAGE)
----------------------------------------

The skill vector guides HOW a question becomes hard:

- MEMORY:
  - Higher memory demand:
    - more precise definitions,
    - more components to recall (e.g., multiple steps in a process),
    - need to remember exceptions or special cases.
- REASONING:
  - Higher reasoning demand:
    - multi-step chains,
    - combining multiple ideas,
    - inferring hidden variables, causes, or consequences.
- NUMERICAL:
  - Higher numerical demand:
    - explicit calculations,
    - multi-step algebra,
    - interpreting quantitative data tables or graphs.
- LANGUAGE:
  - Higher language demand:
    - longer stems with multiple embedded clauses,
    - complex comparative or conditional statements,
    - interpretation of dense descriptions (e.g., experimental setups).

Rules:
- Difficulty should arise from cognitive/quantitative complexity, not from bad wording.
- Language complexity should never be so high that a good student fails purely due to reading difficulty.

----------------------------------------
D. SUBJECT-SPECIFIC QUESTION PATTERNS (HIGH-LEVEL)
----------------------------------------

Mathematics:
- Questions should:
  - Use symbols and formulas appearing in the PDF.
  - Require actual calculation for medium-high numerical skill targets.
  - Often be word problems at intermediate levels (2–4).
  - Incorporate subtle conceptual twists at level 5.

Physics:
- Questions should:
  - Link physical concepts with the corresponding formulas,
  - Use realistic physical scenarios,
  - Require unit consistency and dimensional intuition.

Chemistry:
- Questions should:
  - Cover reactions, mechanisms, structural features, periodic trends,
  - Use stoichiometry and equilibrium numerics when numerical skill is high,
  - Frequently involve "what happens if..." style reasoning.

Biology:
- Questions should:
  - Emphasise:
    - sequences of processes (pathways),
    - structure–function relationships,
    - regulatory and feedback mechanisms,
    - interpretation of diagrams, graphs, or tables.
  - For high reasoning levels:
    - connect molecular → cellular → tissue → organism → population.
  - For chapters like biotechnology:
    - mix:
      - process steps (PCR, cloning, transformation, selection, bioreactors),
      - experimental design logic,
      - real-world applications.

----------------------------------------
E. QUESTION PATTERN LIBRARY (DYNAMIC RUBRIC INTERFACE)
----------------------------------------

- The PDF-specific DYNAMIC RUBRIC must output a QUESTION PATTERN LIBRARY
  containing AT LEAST 40 distinct patterns.
- Each pattern is a template that a question generator can instantiate into
  one or more concrete questions.

Pattern requirements:
- Each pattern should be annotated with:
  - difficulty level L ∈ {1,2,3,4,5},
  - approximate skill ranges for (M, R, N, Lang),
  - a segment tag ∈ {"early", "mid", "late"},
  - a short natural-language description of the question family.

Example annotation format (for the DYNAMIC RUBRIC to follow):
- [L3 | skills: M=0.4–0.6, R=0.6–0.8, N=0.2–0.4, Lang=0.4–0.6 | mid]
  "Ask the student to order the main steps of PCR from the mid-chapter description,
   focusing on conceptual sequence rather than numeric detail."

The question generator MUST:
- Choose patterns consistent with:
  - the desired difficulty level,
  - the desired skill vector S,
  - and the target segment ("early"/"mid"/"late") when specified.
- Then instantiate them into fully formed MCQs that obey all the constraints above.
"""

