import json
import os
import sys
import time

sys.path.insert(0, os.getcwd())

from google import genai
from google.genai import errors, types

from app.config import get_api_key

if len(sys.argv) < 3:
    raise SystemExit(
        "usage: bench.py <model> <runs> [max_attempts] [question_key ...]"
    )

MODEL = sys.argv[1]
RUNS = int(sys.argv[2])

arg3 = sys.argv[3:] if len(sys.argv) > 3 else []

if arg3 and arg3[0].isdigit():
    MAX_ATTEMPTS = int(arg3[0])
    QUESTION_KEYS = arg3[1:]
else:
    MAX_ATTEMPTS = 3
    QUESTION_KEYS = arg3

ALL_QUESTIONS = {
    "lora": "What is LoRA?",
    "levels": "What are the 3 homework levels in the AIE2026 course?",
}

QUESTION_KEYS = QUESTION_KEYS or list(ALL_QUESTIONS)

unknown = [k for k in QUESTION_KEYS if k not in ALL_QUESTIONS]
if unknown:
    raise SystemExit(
        f"Unknown question keys: {', '.join(unknown)}"
    )

QUESTIONS = {
    k: ALL_QUESTIONS[k]
    for k in QUESTION_KEYS
}

PAUSE = 5
TIMEOUT_MS = 240_000
RETRY_CODES = (429, 503)

OUTPUT_PATH = (
    f"/tmp/bench_{MODEL}_{'-'.join(QUESTION_KEYS)}.json"
)

client = genai.Client(
    api_key=get_api_key(),
    http_options=types.HttpOptions(
        timeout=TIMEOUT_MS
    ),
)

results = []


def save_results():
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(
            results,
            f,
            indent=2,
            ensure_ascii=False,
        )


for qname, question in QUESTIONS.items():

    for run in range(1, RUNS + 1):

        print(
            f"\nSTART model={MODEL} "
            f"question={qname} "
            f"run={run}",
            flush=True,
        )

        record = {
            "model": MODEL,
            "question": qname,
            "run": run,
            "timestamp": time.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        }

        for attempt in range(1, MAX_ATTEMPTS + 1):

            start = time.perf_counter()

            try:

                response = client.models.generate_content(
                    model=MODEL,
                    contents=question,
                )

                usage = response.usage_metadata

                record.update(
                    secs=round(
                        time.perf_counter() - start,
                        2,
                    ),
                    input_tokens=(
                        usage.prompt_token_count or 0
                    ),
                    output_tokens=(
                        usage.candidates_token_count or 0
                    ),
                    thinking_tokens=(
                        getattr(
                            usage,
                            "thoughts_token_count",
                            0,
                        )
                        or 0
                    ),
                    total_tokens=(
                        usage.total_token_count or 0
                    ),
                    status="ok",
                    attempts=attempt,
                    answer=response.text,
                )

                break

            except errors.APIError as e:

                record.update(
                    secs=round(
                        time.perf_counter() - start,
                        2,
                    ),
                    status=f"error {e.code}",
                    error=e.message,
                    attempts=attempt,
                )

                if (
                    e.code not in RETRY_CODES
                    or attempt == MAX_ATTEMPTS
                ):
                    break

                wait = 30 * attempt

                print(
                    f"Retrying in {wait}s "
                    f"(attempt {attempt}/{MAX_ATTEMPTS})",
                    flush=True,
                )

                time.sleep(wait)

            except Exception as e:

                record.update(
                    secs=round(
                        time.perf_counter() - start,
                        2,
                    ),
                    status=type(e).__name__,
                    error=str(e)[:200],
                    attempts=attempt,
                )

                break

        print(
            {
                k: v
                for k, v in record.items()
                if k not in ("answer", "error")
            },
            flush=True,
        )

        results.append(record)

        # Save after EVERY run
        save_results()

        time.sleep(PAUSE)

print(f"\nSaved to {OUTPUT_PATH}")