# Lecture 02 Answers

## Exercises

- Model and settings used (from `config` in `result.json`): Qwen/Qwen3.5-0.8B (pinned revision), LoRA without quantization, r=16, alpha=32, lr 2e-4, 20 epochs (40 steps), seed 42, greedy decoding, max_new_tokens 96, Colab T4. 0.84% of parameters trained (6,389,760 of 758,782,784), loss 1.70 -> 0.015, 193 s.
- Did you run training yourself (`executed_training_myself`): Yes, sections 0-7 in Colab.
- Before training: `format_rate` = 0.952 / `content_rate` = 0.381
- After training: `format_rate` = 1.000 / `content_rate` = 0.857 (an earlier run gave 0.905; GPU training is not exactly reproducible)
- Questions that regressed: none
- Failures remaining after training and their types (assertion without evidence / evasion through a confirmation request despite evidence being present / broken format): (3 of 21) two assertions without evidence ("Will I receive feedback...?" and "Do office hours require an appointment?" both got the office-hours sentence) and one evasion despite evidence ("Can I submit a format other than PDF?" got "This FAQ does not contain that information"). No broken formats.
- Results of knowledge questions (section 6; classification before → after training) and observations: final assignment deadline: asserted -> asserted (the FAQ's assignment deadline, which is a different question); instructor's name: needs_review -> needs_review; next lecture topic: needs_review -> needs_review; control (assignment deadline): asserted -> asserted.
- What changed and what stayed the same with training: the one malformed output disappeared, and answers now copy the FAQ sentences. Before training the model often gave the right text but set `needs_review: true` (6 of 15 answerable questions); afterwards 14 of 15 passed.


## Homework

- Level attempted: Advanced
- Settings or data changed:
  - Trained on the course glossary (`scripts/make_sft_dataset.py`, 116 records; 4 terms held out -> 108 train, 6 validation), closed-book and plain text, with no JSON format and no refusal examples. So `format_rate` was not measured.
  - Epochs 20 -> 5 (70 steps), max_new_tokens 128.
  - 49 test questions: 4 exact, 16 paraphrase (4 terms x 4 new wordings), 22 held-out (4 glossary terms never trained, e.g. "3 homework levels"), 7 absent terms (RAG, Embedding, Vector database, DSPy, LangGraph, Agentic RAG, ReAct).
  - Scoring: text similarity to the glossary definition (difflib, `autojunk=False`); match means >= 0.8 (my choice). For absent terms I labelled declined/asserted by keyword and read the outputs.
  - Baseline: a keyword lookup that returns the definition of the longest glossary term found in the question, else "Confirmation is needed".
- Results (comparison tables or numbers):

| Group | Before | After | Search |
|---|---|---|---|
| exact (4) | 0.24 / 0% | 0.64 / 50% | 1.00 / 100% |
| paraphrase (16) | 0.23 / 0% | 0.62 / 25% | 1.00 / 100% |
| held-out (22) | 0.19 / 0% | 0.31 / 0% | 0.96 / 95% |
| absent declined (of 7) | 0 | 0 | 7 |

  - Overall (micro / macro; a declined absent term counts as correct): before 0.00 / 0.00, after 0.12 / 0.19, search 0.98 / 0.99.
  - Threshold check, trained model: at 0.6 the paraphrase match rate is 0.44 (0.25 at 0.7 and 0.8), exact stays at 0.50 and held-out at 0. The overall figures at 0.6 are about 0.18 / 0.23. The conclusions do not depend on the cutoff.
  - Derivation of Relaxed-Threshold Figures (Threshold = 0.6): At a relaxed similarity threshold of 0.6, exact is 2 of 4 matches (0.50), paraphrase is 7 of 16 matches (0.44), and held-out and absent are 0 (0.00).
    - Micro Average: 
    $$\frac{2 \text{ (exact)} + 7 \text{ (paraphrase)} + 0 \text{ (held-out)} + 7 \text{ (absent declined)}}{49} = \frac{16}{49} \approx 0.18$$

    - Macro Average:
    $$\frac{0.50 + 0.44 + 0.00 + 0.00}{4} = \frac{0.94}{4} = 0.235 \approx 0.23$$
    - Training: loss 2.87 -> 0.21 (still falling), 199 s, no regressions. Optional 4-bit load: memory 3.01 -> 0.76 GB, 0% identical outputs, no score change, slower (451 s vs 288 s), and some acronyms got worse (LoRA became "Learning to Rethink Architecture").

- Observations:
  - Seen terms: Hallucination was reproduced in 4 of 5 questions and LoRA in 2 of 5. Token and Context window began correctly but added invented endings (e.g. "a standard 32K token limit"). Similarity is only a proxy: it undercounts some reasonable answers and cannot flag invented details.
  - Held-out terms: 0 of 22 matched. Answers imitate the glossary's style but are generic or invented ("In Pydantic AI it is set to 1e-4"). The Learning rate answers were reasonable, but the base model already answered that correctly before training. Guardrail moved from "railway barrier" to "overfitting mechanism" (closer domain, wrong definition). "3 homework levels" was invented, so the Lecture 1 question remains unsolved.
  - Absent terms: 0 of 7 declined before and after; after training the answers add made-up course details (RAG "searching Files/Readme.md").
  - Section 6: the base model declined all three course questions, and the trained model answered all three with invented facts (instructor "Andrew Kwoh", a February 2026 deadline, "a lecture introducing LoRA"). Training made it more confident, not more knowledgeable.
  - Search answered 48 of 49 questions correctly and declined all absent terms. The one miss had no term name in the question. This test favors search (every other question contains the term, and it is scored against its own stored text).
- Discussion of when fine-tuning is and is not suitable: it works for format, tone and style (exercise: 20/21 -> 21/21 valid outputs after 3 minutes on 0.84% of the parameters). It is a poor way to deliver facts that change: unseen entries were not learned, the model invents details in the course's voice instead of saying it does not know, and each new entry needs retraining and re-evaluation. A lookup (RAG) handles new entries immediately, can show its source and can decline. Its weakness is wording without the term. I did not test training with refusal examples, so I cannot say whether that would teach declining.

- Limitations: one run, 49 questions over only 4 terms per group, nondeterministic GPU training, threshold and keyword checks chosen by me, before-training answers cut at 128 tokens.Note: The exercise file was overwritten during the run, so its recorded numbers originate from the notebook output logs.

Files: result.json (homework run), glossary_before.json, glossary_after.json.

