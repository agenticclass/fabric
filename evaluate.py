#!/usr/bin/env python3
"""
FABRIC Benchmark Evaluation Script

Evaluates a language model on the FABRIC benchmark
(Financial AI Benchmark for Reliability in Indian Context).

Usage:
    python evaluate.py \
        --api-url https://api.example.com/v1/chat/completions \
        --api-key YOUR_KEY \
        --model model-name \
        --output results.json

Works with any OpenAI-compatible API endpoint.
Loads the dataset from HuggingFace or from local data/ directory.
"""

import argparse
import json
import time

import requests

LANGUAGES = ["en", "hi", "hinglish", "te", "bn", "ta"]

PROMPT_TEMPLATE = (
    "You are a financial advisor for Indian markets. "
    "Give a specific answer with exact numbers and Indian regulations.\n\n"
    "Question: {question}\n\n"
    "Answer concisely:"
)


def load_benchmark(local_data=None):
    """Load FABRIC benchmark from HuggingFace or local files."""
    if local_data:
        import glob
        import os
        questions = []
        for f in sorted(glob.glob(os.path.join(local_data, "questions_*.json"))):
            with open(f) as fh:
                questions.extend(json.load(fh))
        return questions
    else:
        from datasets import load_dataset
        return list(load_dataset("agenticclass/fabric", split="train"))


def query_model(prompt, api_url, api_key, model):
    """Query an OpenAI-compatible API. Retries on rate limits."""
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    for attempt in range(3):
        try:
            r = requests.post(
                api_url,
                headers=headers,
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 500,
                },
                timeout=(10, 90),
            )
            if r.status_code == 429:
                time.sleep(5 * (attempt + 1))
                continue
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
        except Exception:
            if attempt < 2:
                time.sleep(3)
    return None


def main():
    parser = argparse.ArgumentParser(description="Evaluate a model on FABRIC")
    parser.add_argument("--api-url", required=True, help="OpenAI-compatible endpoint")
    parser.add_argument("--api-key", default="", help="API key")
    parser.add_argument("--model", required=True, help="Model name")
    parser.add_argument("--languages", nargs="+", default=LANGUAGES)
    parser.add_argument("--output", default="fabric_results.json")
    parser.add_argument("--local-data", default=None, help="Local data/ directory")
    parser.add_argument("--delay", type=float, default=0, help="Seconds between calls")
    args = parser.parse_args()

    questions = load_benchmark(args.local_data)
    print(f"FABRIC: {len(questions)} questions, {len(args.languages)} languages, model={args.model}")

    results = []
    total = len(questions) * len(args.languages)
    done = 0

    for q in questions:
        for lang in args.languages:
            question_text = q.get(f"question_{lang}", "")
            if not question_text:
                continue

            done += 1
            response = query_model(
                PROMPT_TEMPLATE.format(question=question_text),
                args.api_url, args.api_key, args.model,
            )

            results.append({
                "qid": q["id"],
                "category": q["category"],
                "model": args.model,
                "lang": lang,
                "response": response,
            })

            if done % 20 == 0:
                print(f"  [{done}/{total}] {q['id']}/{lang}")

            if args.delay > 0:
                time.sleep(args.delay)

    with open(args.output, "w") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    ok = sum(1 for r in results if r.get("response"))
    print(f"Done: {ok}/{len(results)} responses saved to {args.output}")


if __name__ == "__main__":
    main()
