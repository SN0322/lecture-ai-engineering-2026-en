# Lecture 01 Answers

## Exercises

- Model's answer to the course-specific question (the 3 homework levels; a summary is fine):gemini-3.5-flash-lite said it has no access to real-time information, specific course syllabi, or internal details regarding the "AIE2026 course." Therefore, it cannot provide the 3 homework levels for this specific program.
- What you noticed when comparing it with the correct meaning in the glossary: The glossary defines three levels: Basic (review lecture content), Implementation (write your own code), Advanced (research and experimentation); completing any one completes the homework. The bare model could not know this, and in this run it declined rather than guessing.
For the general question "What is LoRA?" the answers were broadly correct, but two runs listed Stable Diffusion as an LLM, which is an error stated with full confidence.
- Token counts you displayed (input / output): 18 / 45 (homework question, gemini-3.5-flash-lite); 6 / 720 for "What is LoRA?".

## Homework

- Level attempted:  Advanced
- What you did: Added timing and token reporting (input, output, thinking, total) to Added timing and token reporting (input, output, thinking, total) to gemini-3.5-flash via AIE_MODEL, with a short pause between calls. Time is measured end to end (network + generation), not time to first token.
- Results (means; flash n=2 per question because of failed calls):
| Model | Question | Runs | Time (s) | Input | Output | Thinking | Total |
|---|---|---|---|---|---|---|---|
| flash-lite | LoRA | 3 | 4.2 | 6 | 726 | 0 | 732 |
| flash-lite | Homework | 3 | 8.8 | 18 | 49 | 0 | 67 |
| flash | LoRA | 2 | 24.3 | 6 | 849 | 1047 | 1902 |
| flash | Homework | 2 | 15.6 | 18 | 398 | 1091 | 1507 |
Failures: gemini-3.5-flash returned 503 (model busy) on retries of two runs; the other missing runs were not recorded because my first loop hid error messages. No 429 (rate limit) errors were observed.
- Observations and questions:
- flash used about 1,000-1,100 thinking tokens per call even for a short question, while flash-lite used none. Total tokens were roughly 22x higher for flash on the homework question, and latency was 2-7x higher.
- Latency did not track output length: flash-lite took 6-11 s for ~50 tokens in the loop but 1.9 s for the same question in a later run, so timing is noisy (n=3).
- Rate limits: [fill in from AI Studio: RPM / TPM / RPD for each model]. If thinking tokens count toward token quotas, flash would consume them much faster than flash-lite. The 503s are server-side overload, not my quota.
- Question: do thinking tokens count toward the free-tier token limits?