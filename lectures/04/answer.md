# Lecture 04 Answers

## Exercises

- Agreement by criterion (before revision): 
  - Grounding: 10/10
  - Scope: 8/10
  - Hint: 8/10
  - Clarity: 9/10
  - Lecture marker: 5/10
- Number of items needing review (before revision):0
- Criterion revised and the policy added:
  Grounding

  Added:
  > After explicitly stating that a term is not in the glossary, providing a general explanation of the term is acceptable and does not count as asserting unsupported information (pass).
- Agreement by criterion and number of review items (after revision):
  - Grounding: 9/10
  - Scope: 8/10
  - Hint: 8/10
  - Clarity: 8/10
  - Lecture marker: 5/10
  - Review items: 0
- Items where your labels differed from the instructor's, and your reasons:
  - Case #04 (Clarity): I considered the answer sufficiently clear, while the instructor judged it too verbose.
  - Case #06 (Scope): I considered providing a complete homework solution to be out of scope for a learning-support agent.
  - Case #08 (Grounding, Hint, Clarity): I judged the prompt-injection response more strictly and marked several criteria as failures.
  - Case #10 (Scope, Hint, Clarity): I considered unsupported statements about a nonexistent lecture to affect multiple criteria, while the instructor evaluated the issue primarily under Grounding.
  - Several Lecture Marker cases (#02, #07, #09) differed because I focused on answer quality and did not consistently apply the marker requirement.
- Observations and questions:
  - Clarity produced the most subjective disagreements.
  - Separating criteria is important because a failure in Scope should not automatically cause failures in Grounding or Clarity.
  - Small wording changes in the rubric can significantly affect LLM grading behavior.
  - The Lecture Marker criterion is objective and easy to automate with code, while criteria such as Clarity are much harder to evaluate consistently.


## Homework

- Level attempted: Advanced
- What you did:
  I investigated the SWE-bench Verified benchmark dataset and reviewed several tasks from different repositories and difficulty levels:

  1. astropy__astropy-12907 (Easy, 15 min - 1 hour)
     - Fixes incorrect separability matrix calculations for nested compound models.

  2. django__django-10554 (Medium, 1 - 4 hours)
     - Resolves incorrect ordering behavior in queryset union operations.

  3. sympy__sympy-13878 (Hard, >4 hours)
     - Adds precomputed cumulative distribution functions (CDFs) for many probability distributions.

  I also examined dataset statistics, repository distribution, difficulty distribution, and the benchmark's evaluation methodology.
- Results:
  Dataset: SWE-bench Verified

  Repository distribution:
  - django/django: 231 tasks
  - sympy/sympy: 75 tasks
  - sphinx-doc/sphinx: 44 tasks
  - matplotlib/matplotlib: 34 tasks
  - scikit-learn/scikit-learn: 32 tasks

  Difficulty distribution:
  - <15 min fix: 194 tasks
  - 15 min - 1 hour: 261 tasks
  - 1-4 hours: 42 tasks
  - >4 hours: 3 tasks

  Comparison with Lecture 04:
  - Lecture 04 uses 10 manually labeled evaluation cases.
  - SWE-bench Verified contains 500 real GitHub software engineering tasks.
  - Lecture 04 relies on human labels and LLM grading.
  - SWE-bench Verified primarily uses executable tests (FAIL_TO_PASS and PASS_TO_PASS) to determine success.
  - SWE-bench covers diverse domains including web frameworks, scientific computing, machine learning, testing frameworks, visualization libraries, and documentation systems.

- Observations and questions:
  - Django accounts for almost half of the benchmark, showing that web-framework tasks are heavily represented.
  - More than 90% of tasks are estimated to require less than one hour, indicating the benchmark focuses on realistic bug-fixing rather than large software projects.
  - The SymPy task was substantially more difficult because it required mathematical and statistical knowledge in addition to software engineering skills.
  - Compared with Lecture 04, SWE-bench Verified provides a much larger, more realistic, and more objective evaluation setting through automated test execution.
  - An interesting question is whether future coding benchmarks should combine executable tests with LLM-based evaluation to better assess solution quality and maintainability.