# Lecture 05 Answers

## Exercises

- Answering model (`[model]` shown during execution):gemini-3.5-flash-lite
- Comparison question: In Lecture 02, what does LoRA freeze and train? What does QLoRA add?
- Target materials (also record the difference in scope between full context and the other methods): Full Context covered all 9 documents, while Vector, Tree and Graph targeted Lectures 01–03 (214 pages).

### Results by Method

| Method | Answer and correctness | Cited pages | Time (s) | Input/output tokens | Responses | Cost (USD) |
|---|---|---|---:|---:|---:|---:|
| Full Context | Correct | Lec 2, pp.51–52 | 4.61 | 95,824/289 | 1 | 0.029470 |
| Vector | Correct | Lec 2, pp.51–52 | 12.70 | 2,759/213 | 2 | 0.001360 |
| Tree | Correct | Lec 2, p.52 | 17.48 | 9,442/359 | 5 | 0.003730 |
| Graph (original) | Correct | Lec 2, p.52 | 3.43 | 5,190/242 | 2 | 0.002162 |

- **Pages found:**
  - **Vector:** Retrieved five pages; Lecture 02 p.52 directly explained LoRA/QLoRA, while p.51 provided background.
  - **Tree:** Located Lecture 02 p.52 through the document hierarchy.
  - **Graph:** Retrieved Lecture 02 p.52 as a seed page.
  - **Multi-page test:** Lecture 03 pp.39–40 provided evidence about compaction, cross-session memory and daily-note filtering.

- **Tool calls (`--trace`):**
  - **Vector:** `search_materials()`
  - **Tree:** `browse_tree()` — followed `lec02-main` → `lec02-main-s045` → `lec02-main-p052`.
  - **Graph:** `search_graph()`
  - **Basic RAG:** Called `search_materials()` twice for the multi-page question.
  - Graph traces showed abbreviated results, so complete expanded page lists could not be verified.

- **Limitations observed:**
  - Some Vector results were related but did not directly explain QLoRA.
  - Tree included an unnecessary follow-up question.
  - For the unanswerable question, all methods correctly identified that the requested RAG performance measurements were unavailable. Lecture 02 p.13 provided related background, not the requested measurements.

- **Method selection:**
  - **Vector search** is suitable for specific factual questions, with relatively low token usage and cost.
  - **Graph** may help retrieve evidence across related pages, while **Tree** is useful when document hierarchy matters.
  - Graph did not consistently outperform Basic RAG in these tests.

- **Overall observations:**
  - All methods answered the tested answerable questions correctly and handled the unanswerable question appropriately.
  - Full Context had the highest input-token usage in the initial comparison.
  - Modified Graph reduced input tokens and cost in the unanswerable test but took longer.



## Homework


- Level attempted: Advanced
- What you did (files, settings, or processing changed, or retrieval method designed): Modified `app/retrieval.py` to restrict Graph expansion to adjacent pages.
  Original:
  ```python
  if edge["relation"] in ("next_page", "mentions") and a in nodes and b in nodes:
  ```

  Modified:
  ```python
  if edge["relation"] == "next_page" and a in nodes and b in nodes:
  ```
- Comparison question and conditions held fixed (model, target materials, etc.):
  - Model: `gemini-3.5-flash-lite`
  - Target materials: Lectures 01–03.
  - Compared Basic RAG, Original Graph and Modified Graph using the same questions.
  - Tested single-page, multi-page and unanswerable questions.
- Results (answers and evidence before/after, `--trace` output, time, token counts, estimated generation API cost, etc.):
  **1. Single-page question (LoRA/QLoRA)**

  | Metric | Original Graph | Modified Graph |
  |---|---:|---:|
  | Correct | Yes | Yes |
  | Cited page | 52 | 52 |
  | Time (s) | 3.43 | 4.03 |
  | Input/output tokens | 5,190/242 | 5,260/211 |
  | Responses | 2 | 2 |
  | Cost (USD) | 0.002162 | 0.002106 |

  **2. Multi-page question (compaction and memory)**

  | Metric | Basic RAG | Original Graph | Modified Graph |
  |---|---:|---:|---:|
  | Correct | Yes | Yes | Yes |
  | Cited pages | 39–40, 65 | 39–40 | 39–40 |
  | Time (s) | 20.13 | 20.47 | 7.12 |
  | Input/output tokens | 6,061/285 | 4,876/228 | 4,943/263 |
  | Responses | 3 | 2 | 2 |
  | Cost (USD) | 0.002531 | 0.002033 | 0.002140 |

  **3. Unanswerable question (RAG performance metrics)**

  | Metric | Basic RAG | Original Graph | Modified Graph |
  |---|---:|---:|---:|
  | Correctly identified missing information | Yes | Yes | Yes |
  | Time (s) | 30.34 | 31.86 | 35.23 |
  | Input/output tokens | 7,459/189 | 24,656/285 | 12,828/271 |
  | Responses | 3 | 4 | 3 |
  | Cost (USD) | 0.002710 | 0.005362 | 0.003428 |

  All three methods answered the answerable questions correctly and recognised that the requested measurements were absent in the unanswerable question.
- Examples of improvements and remaining failures or limitations:
  - Modified Graph reduced input tokens and cost compared with Original Graph in the unanswerable test.
  - It was faster in the multi-page test but slower in the other two tests.
  - Removing `mentions` may exclude useful related pages.
  - Only one run per configuration was conducted, so performance differences are not conclusive.
- Observations and questions:
  - Modified Graph did not consistently outperform Original Graph or Basic RAG.
  - Basic RAG was cost-efficient, while Graph may help retrieve related information across pages.
  - Further testing with repeated runs and different hop limits is needed to evaluate the modification reliably.