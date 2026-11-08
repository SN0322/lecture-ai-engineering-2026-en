# Lecture 03 Answers

## Exercises

- Differences between the Lecture 01 (bare LLM) and agent answers:
    - For *"What are the 3 levels in the AIE2026 course homework?"*, the bare LLM usually said it had no course information or gave a generic guess. The agent used `search_glossary`, found the **3 homework levels** entry, and answered correctly: **Basic**, **Implementation**, and **Advanced**. It also added course-specific details and ended with a lecture reference as required by `INSTRUCTIONS`.
- Tool calls shown by `--trace` (tool names and arguments):
  - *"What is the difference between LoRA and QLoRA?"*
    - `search_glossary({'query': 'LoRA'})`
    - `search_glossary({'query': 'QLoRA'})`
  - *"What will we learn in Lecture 03?"*
    - `get_lecture_summary({'lecture': 3})`
  - *"Give me a review question for Lecture 2"*
    - `make_quiz({'lecture': 2})`
  - *"What is RAG?"*
    - `search_glossary({'query': 'RAG'})`
    - `search_glossary({'query': 'Retrieval-Augmented Generation'})`
- Number of LLM calls for one question (`requests`):
  - Most questions: `requests=2`, `tool_calls=1`
  - LoRA vs QLoRA: `requests=2`, `tool_calls=2`
  - RAG: `requests=3`, `tool_calls=2`

- Tool added and the description in its docstring:
  - Added:

    ```python
    make_quiz(lecture: int)
    ```

  - Registered with:

    ```python
    agent.tool_plain(tools.make_quiz)
    ```

  - Purpose: generate a review question from a glossary term covered in a selected lecture.
  - `--list-tools` shows the new tool and its integer argument.
  - `--trace "Give me a review question for Lecture 2"` showed:
    - `make_quiz({'lecture': 2})`
    - Returned an Overfitting question.
  - The model turned the returned JSON into a learner-facing quiz question and did not reveal the answer immediately.

## Homework

- Level attempted: Advanced (a) - rebuild the agent with Google ADK
- What you did: 
  - Created an ADK version of the glossary agent using:
    - `search_glossary`
    - `get_lecture_summary`
    - `make_quiz`
  - Reused the same `INSTRUCTIONS` and tools without modification.
  - Ran the ADK agent with:

    ```bash
    PYTHONPATH=. uv run --with google-adk adk run adk_agent/glossary_agent
    ```

  - Asked both agents the same questions:
    - What is LoRA?
    - Tell me about fine-tuning
    - What are the 3 levels?
    - What will we learn in Lecture 03?
    - Give me a review question for Lecture 2
    - What is the difference between LoRA and QLoRA?
    - What is RAG?
    - What is a token?
    - Explain MCP server
    - Define AI engineering

- Results:

| Feature | Pydantic AI | ADK |
|----------|----------|----------|
| Instructions | `Agent(instructions=...)` | `Agent(instruction=...)` |
| Tool registration | `agent.tool_plain(fn)` | `tools=[...]` |
| Tool descriptions | Function docstrings | Same docstrings |
| Trace support | `--trace` | Not shown by default |
| Output quality | Correct glossary-based answers | Correct glossary-based answers |

| Question | Pydantic AI | ADK |
|----------|----------|----------|
| What is LoRA? | Correct glossary definition | Correct glossary definition |
| 3 homework levels | Correct | Correct |
| Lecture 03 summary | Used `get_lecture_summary(3)` | Similar answer |
| Review question | Overfitting quiz | Pretraining quiz |
| LoRA vs QLoRA | Correct | Correct |
| Token | Correct | Correct |
| RAG | "Not in glossary" + explanation | "Not in glossary" only |

- Observations and questions:
  - Both frameworks produced very similar answers. The tools and instructions appeared more important than the framework itself.
  - `make_quiz` was selected correctly whenever a review question was requested.
  - `search_glossary("RAG")` unexpectedly matched the Token entry because `"rag"` occurs inside `"fragments"` in a glossary definition. Both agents inherit this behavior because they share the same `tools.py`.
  - Pydantic AI exposed tool activity clearly through `--trace`.
  - ADK's standard CLI only displayed final answers. The log files under `/tmp/agents_log/` did not expose tool calls in a way comparable to Pydantic AI, so tool usage was inferred from the generated answers.
  - Gemini frequently returned **503 (model busy)** errors during testing. Re-running the same query usually succeeded.
  - On the RAG question, Pydantic AI said "It is not in the glossary" but then explained RAG anyway. ADK stopped after the refusal. With only a few runs, I cannot determine whether this difference is systematic or caused by normal model variation.

- **Conclusion:**
  - The experiment supports the lecture's claim that an agent is primarily **model + tools + instructions**.
  - Rebuilding the agent using ADK required only minor code changes.
  - With the same instructions and tools, both frameworks behaved similarly.
  - The main practical difference was observability: Pydantic AI made tool use easy to inspect with `--trace`, while ADK's default CLI exposed only final responses.