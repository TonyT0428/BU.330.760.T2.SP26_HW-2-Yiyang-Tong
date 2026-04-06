#!/usr/bin/env python3
"""CLI prototype: load meeting notes, apply prompts from prompts.md, call Gemini, print or save output."""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from google import genai
from google.genai import types


def load_prompt_sections(prompt_path: Path) -> tuple[str, str]:
    """Parse `## system` and `## user_template` blocks from prompts.md."""
    raw = prompt_path.read_text(encoding="utf-8")
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in raw.splitlines():
        if line.startswith("## "):
            name = line[3:].strip().split()[0].lower()
            current = name
            sections.setdefault(current, [])
            continue
        if current is None:
            continue
        sections[current].append(line)
    system = "\n".join(sections.get("system", [])).strip()
    user_tpl = "\n".join(sections.get("user_template", [])).strip() or "{meeting_notes}"
    return system, user_tpl


def read_meeting_notes(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def build_user_message(template: str, meeting_notes: str) -> str:
    if "{meeting_notes}" not in template:
        return f"{template.rstrip()}\n\n{meeting_notes}"
    return template.replace("{meeting_notes}", meeting_notes)


def resolve_api_key() -> str:
    for key in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        v = os.environ.get(key, "").strip()
        if v:
            return v
    print(
        "Missing API key. Set environment variable GEMINI_API_KEY (or GOOGLE_API_KEY). "
        "Create a key in Google AI Studio: https://aistudio.google.com/app/apikey",
        file=sys.stderr,
    )
    sys.exit(1)


def format_run_header(model: str, prompt_file: Path, notes_file: Path) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = [
        "=" * 60,
        "Meeting notes → structured brief (Gemini)",
        f"Time:        {ts}",
        f"Model:       {model}",
        f"Prompt file: {prompt_file}",
        f"Notes file:  {notes_file}",
        "=" * 60,
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Call Gemini with prompts from prompts.md.")
    parser.add_argument(
        "notes_file",
        type=Path,
        help="Path to a text file with raw meeting notes (UTF-8).",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Write full run (header + model output) to this file. Still prints to stdout.",
    )
    parser.add_argument(
        "--prompt-file",
        type=Path,
        default=Path("prompts.md"),
        help="Markdown file with ## system and ## user_template (default: prompts.md).",
    )
    parser.add_argument(
        "--model",
        default=os.environ.get("GEMINI_MODEL", "gemini-2.5-flash"),
        help='Gemini model id (default: gemini-2.5-flash or $GEMINI_MODEL).',
    )
    args = parser.parse_args()

    if not args.notes_file.is_file():
        print(f"Notes file not found: {args.notes_file}", file=sys.stderr)
        sys.exit(1)
    if not args.prompt_file.is_file():
        print(f"Prompt file not found: {args.prompt_file}", file=sys.stderr)
        sys.exit(1)

    api_key = resolve_api_key()
    system_instruction, user_template = load_prompt_sections(args.prompt_file)
    meeting_notes = read_meeting_notes(args.notes_file)
    user_message = build_user_message(user_template, meeting_notes)

    client = genai.Client(api_key=api_key)
    if system_instruction:
        response = client.models.generate_content(
            model=args.model,
            contents=user_message,
            config=types.GenerateContentConfig(system_instruction=system_instruction),
        )
    else:
        response = client.models.generate_content(
            model=args.model,
            contents=user_message,
        )

    body = (response.text or "").strip()
    if not body:
        print("Empty model response (check safety blocks or prompt).", file=sys.stderr)
        if getattr(response, "prompt_feedback", None) is not None:
            print(response.prompt_feedback, file=sys.stderr)
        sys.exit(2)

    header = format_run_header(args.model, args.prompt_file, args.notes_file)
    out = f"{header}\n--- Model output ---\n\n{body}\n"

    print(out, end="")
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(out, encoding="utf-8")
        print(f"\n--- Saved to {args.output} ---", file=sys.stderr)


if __name__ == "__main__":
    main()
