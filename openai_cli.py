#!/usr/bin/env python3
"""Simple command-line client for sending a prompt to OpenAI."""

from __future__ import annotations

import argparse
import json
import importlib.util
import os
import sys
from typing import Any

DEFAULT_MODEL = "gpt-5.5"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Send a prompt to an OpenAI model and print the response."
    )
    parser.add_argument(
        "prompt",
        nargs="+",
        help="Prompt text to send. Quote multi-word prompts or pass them as separate words.",
    )
    parser.add_argument(
        "--model",
        default=os.environ.get("OPENAI_MODEL", DEFAULT_MODEL),
        help=f"OpenAI model to use (default: OPENAI_MODEL or {DEFAULT_MODEL}).",
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("OPENAI_API_KEY"),
        help="OpenAI API key (default: OPENAI_API_KEY environment variable).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=60.0,
        help="Request timeout in seconds (default: 60).",
    )
    return parser.parse_args()


def get_value(item: Any, key: str) -> Any:
    """Read a value from either an SDK object or a dictionary."""
    if isinstance(item, dict):
        return item.get(key)
    return getattr(item, key, None)


def extract_text(response: Any) -> str:
    """Return printable text from an OpenAI Responses API response."""
    output_text = get_value(response, "output_text")
    if isinstance(output_text, str) and output_text:
        return output_text

    parts: list[str] = []
    for item in get_value(response, "output") or []:
        for content in get_value(item, "content") or []:
            text = get_value(content, "text")
            if isinstance(text, str):
                parts.append(text)
    if parts:
        return "\n".join(parts)

    if hasattr(response, "model_dump"):
        return json.dumps(response.model_dump(), indent=2)
    return json.dumps(response, indent=2)


def request_completion(prompt: str, model: str, api_key: str, timeout: float) -> Any:
    from openai import OpenAI

    client = OpenAI(api_key=api_key, timeout=timeout)
    return client.responses.create(model=model, input=prompt)


def main() -> int:
    args = parse_args()
    if not args.api_key:
        print(
            "Error: provide an API key with --api-key or set OPENAI_API_KEY.",
            file=sys.stderr,
        )
        return 2

    if importlib.util.find_spec("openai") is None:
        print(
            "Error: install the OpenAI Python SDK with `python -m pip install -r requirements.txt`.",
            file=sys.stderr,
        )
        return 2

    prompt = " ".join(args.prompt)
    try:
        response = request_completion(prompt, args.model, args.api_key, args.timeout)
    except Exception as exc:
        print(f"OpenAI API request failed: {exc}", file=sys.stderr)
        return 1

    print(extract_text(response))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
