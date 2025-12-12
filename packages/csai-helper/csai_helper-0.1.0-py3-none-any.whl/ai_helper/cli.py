"""Command-line interface for ai-helper."""

from __future__ import annotations

import argparse
import sys
from typing import Optional

from ai_helper import format_response, get_response, summarize_text
from ai_helper.providers.local import LocalProvider


def _provider_from_args(name: str, model: Optional[str]) -> object:
    if name == "openai":
        from ai_helper.providers.openai import OpenAIProvider

        return OpenAIProvider(model=model or "gpt-4o-mini")
    return LocalProvider()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ai-helper CLI")
    parser.add_argument(
        "--provider",
        choices=["local", "openai"],
        default="local",
        help="Provider backend to use.",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Model name (provider-specific)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    ask = subparsers.add_parser("ask", help="Send a prompt and print the response.")
    ask.add_argument("prompt", nargs="?", help="Prompt to send. Reads stdin if omitted.")
    ask.add_argument("--system", dest="system_prompt", default=None, help="System prompt.")

    summarize = subparsers.add_parser("summarize", help="Summarize text.")
    summarize.add_argument("text", nargs="?", help="Text to summarize. Reads stdin if omitted.")
    summarize.add_argument(
        "--max-words",
        type=int,
        default=120,
        help="Maximum words in the summary (default: 120).",
    )

    fmt = subparsers.add_parser("format", help="Normalize whitespace in a response.")
    fmt.add_argument("text", nargs="?", help="Text to format. Reads stdin if omitted.")

    return parser


def _read_positional_or_stdin(value: Optional[str]) -> str:
    if value is not None:
        return value
    data = sys.stdin.read().strip()
    if not data:
        raise SystemExit("No input provided")
    return data


def main(argv: Optional[list[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    provider = _provider_from_args(args.provider, args.model)

    if args.command == "ask":
        prompt = _read_positional_or_stdin(args.prompt)
        print(get_response(prompt, provider=provider, system_prompt=args.system_prompt))
    elif args.command == "summarize":
        text = _read_positional_or_stdin(args.text)
        print(summarize_text(text, provider=provider, max_words=args.max_words))
    elif args.command == "format":
        text = _read_positional_or_stdin(args.text)
        print(format_response(text))
    else:  # pragma: no cover - argparse enforces choices
        parser.error(f"Unknown command: {args.command}")


if __name__ == "__main__":  # pragma: no cover
    main()
