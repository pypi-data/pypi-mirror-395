STATIC_RUBRIC_TEXT = """
GLOBAL STATIC RUBRIC FOR EDU_DIFF_ENGINE
========================================

Purpose:
- This rubric defines what difficulty levels 1–5 mean ACROSS ALL SUBJECTS.
- The dynamic rubric for a specific PDF MUST be a deformation of this global rubric, NOT a new scale.
- All local (PDF-specific) difficulty decisions must remain consistent with this global structure.

----------------------------------------
A. GLOBAL DIFFICULTY LEVELS (1–5)
----------------------------------------

For ALL subjects, difficulty level is defined by a combination of:
- Cognitive demand (recall vs multi-step reasoning)
- Number of concepts combined
- Required numerical / symbolic manipulation
- Subtlety of distractors
- Required skill vector S = (memory, reasoning, numerical, language) in [0,1]

Level 1 (FOUNDATION / RECALL)
- Cognitive type:
  - Pure recall or single definition / fact.
  - Direct reading from PDF; almost no transformation.
- Concepts:
  - Exactly 1 simple concept.
- Reasoning chain:
  - 0–1 reasoning steps (read → answer).
- Numerical / symbolic:
  - None or trivial substitution (e.g., "2 + 3", "mass = 5 kg").
- Distractors:
  - 1 clearly correct option,
  - 1–2 obviously wrong options,
  - Only 1 mildly plausible distractor.
- Typical skill vector range:
  - memory:   0.6–0.9  (dominating)
  - reasoning:0.1–0.3
  - numerical:0.0–0.2
  - language: 0.2–0.4

Level 2 (BASIC UNDERSTANDING / DIRECT APPLICATION)
- Cognitive type:
  - Understanding of a definition / formula,
  - Direct application to a simple example.
- Concepts:
  - 1–2 closely related concepts.
- Reasoning chain:
  - 1–2 steps ("identify correct formula → plug → get result").
- Numerical / symbolic:
  - Simple arithmetic or single-step algebra.
- Distractors:
  - All options are plausible at first glance,
  - Wrong options correspond to simple misunderstandings or arithmetic slips.
- Typical skill vector range:
  - memory:   0.5–0.7
  - reasoning:0.3–0.5
  - numerical:0.2–0.4
  - language: 0.3–0.5

Level 3 (STANDARD APPLICATION / SHORT MULTI-STEP)
- Cognitive type:
  - Applying known ideas to new but standard situations.
  - Requires combining 2–3 ideas from the PDF.
- Concepts:
  - 2–3 concepts, or 1 concept used in a non-trivial way.
- Reasoning chain:
  - 2–4 steps (interpret → select formula/concept → transform → evaluate).
- Numerical / symbolic:
  - Multi-step calculations with clean numbers,
  - Algebraic manipulations that are standard for the grade level.
- Distractors:
  - Each option maps to a specific partial reasoning path or common mistake.
- Typical skill vector range:
  - memory:   0.4–0.6
  - reasoning:0.5–0.7
  - numerical:0.4–0.6
  - language: 0.4–0.6

Level 4 (ADVANCED MULTI-CONCEPT / SUBTLE REASONING)
- Cognitive type:
  - Multi-step reasoning with branching paths,
  - Discrimination between similar concepts,
  - Interpretation of unfamiliar but derivable situations.
- Concepts:
  - 3+ concepts interacting.
- Reasoning chain:
  - 4–6 steps; often requires "planning" the solution.
- Numerical / symbolic:
  - Longer derivations, messy numbers (decimals, fractions, exponents, logs),
  - Combined units or multi-equation systems.
- Distractors:
  - All options look very plausible; each wrong option corresponds to a specific, realistic misconception.
- Typical skill vector range:
  - memory:   0.3–0.5
  - reasoning:0.7–0.85
  - numerical:0.6–0.8
  - language: 0.5–0.7

Level 5 (MAXIMUM DIFFICULTY WITHIN THIS PDF)
- Cognitive type:
  - Deep synthesis, edge cases, or non-obvious connections,
  - Reverse reasoning (e.g., infer cause from observed effect),
  - "What-if" variants that stretch the ideas in the PDF to the limit.
- Concepts:
  - 3–5 concepts with non-obvious links.
- Reasoning chain:
  - 5–8 steps; may involve nested reasoning or approximate arguments.
- Numerical / symbolic:
  - Extended calculations, chained formulas, careful handling of approximations or limits.
- Distractors:
  - Each option is deeply plausible; correct answer requires full, precise reasoning.
- Typical skill vector range:
  - memory:   0.3–0.5
  - reasoning:0.85–0.95
  - numerical:0.7–0.9
  - language: 0.6–0.8

NOTE:
- These skill vector ranges are priors. The dynamic rubric can deform them (e.g., theory-heavy chapter → lower numerical).

------------------------------------------------
B. SUBJECT-SPECIFIC INTERPRETATION GUIDELINES
------------------------------------------------

The same level (e.g., 3) looks DIFFERENT in different subjects.

Mathematics:
- Level 1:
  - Direct formula name, symbol meaning, simple identities.
- Level 3:
  - Standard word problems with 2–3 operations, solving linear equations, basic inequalities, geometry with 1–2 steps.
- Level 5:
  - Multi-step problems involving simultaneous equations, non-trivial transformations, composition of functions, or tricky geometrical reasoning.
- Numerical emphasis:
  - All levels except 1 usually contain numbers or algebraic symbols that must be manipulated.

Physics:
- Level 1:
  - Names of quantities, units, ONE simple law or definition.
- Level 3:
  - Single-principle numerical problems (e.g., use Newton’s second law once, or one kinematics equation).
- Level 5:
  - Multi-principle, multi-step problems (e.g., combine energy + momentum + kinematics, or electrical + thermal effects).
- Numerical emphasis:
  - Most questions (≥ 60% at levels 3–5) should involve explicit calculation.

Chemistry:
- Level 1:
  - Definitions, periodic trends, names of compounds, basic reaction categories.
- Level 3:
  - Stoichiometric calculations with 1–2 steps, limiting reagent in simple reactions, basic pH problems.
- Level 5:
  - Complex equilibrium or multi-reaction stoichiometry; combined conceptual + numeric reasoning; thermochemistry chains.
- Reaction emphasis:
  - At most levels, many questions can be conceptual (mechanism, trends),
  - But when numerical skill is high, a significant fraction should be quantitative.

Biology:
- Level 1:
  - Names of structures (organelles, tissues, organs),
  - Simple one-line definitions (e.g., osmosis, diffusion),
  - Straight recall of labeled diagrams (without reasoning).
- Level 2:
  - Understanding basic processes with one cause-effect link (e.g., "What happens if stomata close?"),
  - Matching structure to function.
- Level 3:
  - Multi-step processes (e.g., photosynthesis stages, cellular respiration stages, immune response sequence),
  - Questions requiring tracking a sequence or comparing two processes.
- Level 4:
  - Integration across scales (e.g., how a cellular defect leads to organ-level symptoms),
  - Multi-factor cause-effect chains, interpreting data tables or graphs from experiments.
- Level 5:
  - Deep, multi-level reasoning (gene → protein → pathway → phenotype → population),
  - Interpretation of experimental setups, controls, and outcomes; subtle questions about regulatory mechanisms.
- Numerical aspect in Biology:
  - Usually low to moderate; main difficulty comes from:
    - reasoning about pathways,
    - cause–effect chains,
    - interpreting graphs / data tables,
    - distinguishing similar-sounding processes.
- Language emphasis:
  - Biology often carries higher language load (dense text, many terms),
  - But difficulty must not come only from jargon; conceptual reasoning should dominate at higher levels.

Theory-heavy subjects (History, Civics, etc.):
- Difficulty relies more on:
  - Depth of understanding,
  - Ability to connect causes → consequences over time,
  - Ability to discriminate between similar formulations or interpretations.
- Numerical skill often stays low; reasoning and language dominate.

------------------------------------------------
C. SKILL VECTOR S = (MEMORY, REASONING, NUMERICAL, LANGUAGE)
------------------------------------------------

Definitions:
- MEMORY:
  - Reliance on recall of exact facts, definitions, names, or formulas.
- REASONING:
  - Need to connect ideas, infer, generalize, or follow multi-step logic.
- NUMERICAL:
  - Amount and complexity of arithmetic, algebra, or quantitative reasoning.
- LANGUAGE:
  - Complexity of reading, parsing, and understanding written text (including long stems, indirect wording).

Global tendencies:
- As difficulty increases from 1 → 5:
  - REASONING almost always increases.
  - MEMORY may decrease slightly (less pure recall, more inference).
  - NUMERICAL increases strongly in quantitative subjects (math/physics/quant-chem).
  - LANGUAGE may increase, but must never be so complex that language alone makes a question hard.

Dynamic rubric MUST:
- Start from the global ranges given above,
- Then adjust them based on:
  - How quantitative the specific PDF is,
  - How dense the text is,
  - Whether the chapter is primarily conceptual or computational.

------------------------------------------------
D. GLOBAL CONSTRAINTS ON GOOD QUESTIONS
------------------------------------------------

1) SOURCE FIDELITY:
   - All questions MUST be answerable using the PDF alone (plus standard prior knowledge for that grade).
   - Do NOT invent facts or formulas not implied or clearly consistent with the PDF.

2) FAIRNESS:
   - Difficulty must come from reasoning and/or content complexity, NOT from trick wording.
   - Avoid ambiguous stems, double negatives, and purely language-based traps.

3) OPTIONS / DISTRACTORS:
   - Always 4 options.
   - Each wrong option should correspond to a specific misunderstanding, calculation error, or partial reasoning path.
   - Avoid "silly" distractors that no serious student would pick.

4) ALIGNMENT TO LEVEL:
   - At level 1, a well-prepared student should answer almost instantly after recognizing the fact.
   - At level 5, even a strong student should need to think carefully and possibly work through multiple sub-steps.

5) SKILL CONSISTENCY:
   - The dynamic rubric must explicitly state, for each level in THIS PDF:
     - Approximate skill ranges (min–max) for memory, reasoning, numerical, language.
     - Typical question templates (e.g., "compute X from Y and Z using formula F", "identify correct graph", "infer cause from data").
   - When generating questions, the LLM should try to match BOTH:
     - the target difficulty level, and
     - the target skill vector S within those ranges.

This STATIC RUBRIC is the non-negotiable baseline. The dynamic rubric may specialize it to a specific chapter, but must not contradict these global principles.
"""

