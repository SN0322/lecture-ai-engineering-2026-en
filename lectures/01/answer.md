# Lecture 01 Answers

## Exercises

- Model's answer to the course-specific question (the 3 homework levels; a summary is fine):gemini-3.5-flash-lite said it has no access to real-time information, specific course syllabi, or internal details regarding the "AIE2026 course." Therefore, it cannot provide the 3 homework levels for this specific program.
- What you noticed when comparing it with the correct meaning in the glossary: The glossary defines three levels: Basic (review lecture content), Implementation (write your own code), Advanced (research and experimentation); completing any one completes the homework. The bare model could not know this, and in this run it declined rather than guessing.
For the general question "What is LoRA?" the answers were broadly correct, but two runs listed Stable Diffusion as an LLM, which is an error stated with full confidence.
- Token counts you displayed (input / output): 18 / 45 (homework question, gemini-3.5-flash-lite); 6 / 720 for "What is LoRA?".

## Homework

- Level attempted:  Advanced
- What you did: 
  - Implemented the TODO in `app/ask.py` using `response.usage_metadata`.
  - Added token-count reporting (input, output, and total tokens).
  - Added response-time measurement.
  - Created a benchmark script (`benchmarks/bench.py`) to automate repeated experiments.
  - Compared two models:
    - `gemini-3.5-flash-lite`
    - `gemini-3.8-flash`
  - Compared two questions:
    - "What is LoRA?"
    - "What are the 3 homework levels in the AIE2026 course?"
  - Collected multiple benchmark runs across several days and analyzed latency, token usage, hallucinations, and API errors.
- Results:

### Benchmark Summary

| Model | Question | Successful Runs | Avg Time (s) | Avg Output Tokens | Avg Thinking Tokens |
|---------|----------|---------:|---------:|---------:|---------:|
| gemini-3.5-flash-lite | LoRA | 5 | 3.24 | 735 | 0 |
| gemini-3.5-flash-lite | Homework levels | 5 | 1.08 | 133 | 0 |
| gemini-3.8-flash | LoRA | 5 | 96.35 | 803 | 908 |
| gemini-3.8-flash | Homework levels | 5 | 103.74 | 350 | 1533 |

### Reliability

| Model | Successes | Failures |
|---------|---------:|---------:|
| gemini-3.5-flash-lite | 10 | 0 |
| gemini-3.8-flash | 10 | 6 |

Observed errors for `gemini-3.8-flash`:
- ReadTimeout
- HTTP 503 (high demand)
- HTTP 504 (deadline exceeded)

### Ground Truth Comparison

The correct homework levels from `data/glossary.json` are:

1. Basic (review lecture content)
2. Implementation (write your own code)
3. Advanced (research and experimentation)

For the course-specific question, neither model consistently produced the correct answer without access to the glossary.

- Results from `gemini-3.5-flash-lite`:
  - Usually replied that it did not know the answer.
  - Occasionally generated plausible but incorrect homework levels.

- Results from `gemini-3.8-flash`:
  - Consistently generated detailed and plausible course structures.
  - None matched the actual glossary definition.

- Observations and questions:
  - `gemini-3.5-flash-lite` was much faster and more reliable than `gemini-3.8-flash`.
  - The stronger model used substantially more reasoning tokens, especially for the course-specific question.
  - More reasoning did not improve correctness when the required information was missing.
  - For unknown course information, `gemini-3.5-flash-lite` often admitted uncertainty, whereas `gemini-3.8-flash` tended to generate detailed but incorrect answers.
  - Free-tier limitations are influenced not only by request count but also by model demand and response complexity. The stronger model showed timeout and service-availability issues during benchmarking.
  - These results demonstrate why later lectures introduce tools and retrieval mechanisms instead of relying solely on a bare LLM.