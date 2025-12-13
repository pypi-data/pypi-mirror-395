#!/usr/bin/env python3
"""
gptsummarize
============

Command-line helper that turns the current Git changeset into a crisp commit
message using an LLM.

Typical workflow
----------------

    # Stage whatever you want to commit
    git add -A

    # Let Ada draft the commit message ✨
    gptsummarize --show-diff

The tool
  • gathers a **full unified diff** (staged by default, optionally unstaged);
  • feeds it to the configured LLM; and
  • prints the suggested commit message to stdout.

Environment
-----------
• `GPTDIFF_LLM_API_KEY` (Required) API key for the LLM backend  
• `GPTDIFF_LLM_BASE_URL` (Optional) Override endpoint (default `https://nano-gpt.com/api/v1/`)  
• `GPTDIFF_MODEL`      (Optional) Default model name
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

from gptdiff.gptdiff import call_llm, color_code_diff, domain_for_url  # reuse helpers

# --------------------------------------------------------------------------- #
# Git utilities
# --------------------------------------------------------------------------- #


def _run_git(cmd: list[str]) -> str:
    """Run a git command, returning *stdout* (raises on other failures)."""
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # `git diff` returns 1 when differences are found; treat that as success.
    if res.returncode not in (0, 1):
        print(res.stderr.strip(), file=sys.stderr)
        sys.exit(res.returncode)
    return res.stdout


def collect_diff(include_unstaged: bool = False) -> str:
    """
    Build a single unified diff containing:
      • staged changes (index → HEAD)
      • **optional** unstaged working-tree edits (working-tree → index)
      • newly created untracked text files
    """
    diff = _run_git(["git", "diff", "--cached", "--binary", "--full-index", "-M", "-C"])

    if include_unstaged:
        diff += _run_git(["git", "diff", "--binary", "--full-index", "-M", "-C"])

    # — Untracked files ----------------------------------------------------- #
    untracked = (
        _run_git(["git", "ls-files", "--others", "--exclude-standard"]).splitlines()
    )
    for path in untracked:
        p = Path(path)
        try:
            content = p.read_text(encoding="utf8")
        except (UnicodeDecodeError, FileNotFoundError):
            # Skip binaries or vanished paths; they're unlikely to be committed.
            continue

        header = (
            f"diff --git a/{path} b/{path}\n"
            "new file mode 100644\n"
            "--- /dev/null\n"
            f"+++ b/{path}\n"
            "@@ 0,0 @@\n"
        )
        body = "\n".join(f"+{ln}" for ln in content.splitlines())
        diff += f"{header}{body}\n"

    return diff


# --------------------------------------------------------------------------- #
# LLM-driven commit-message generation
# --------------------------------------------------------------------------- #


def summarise(diff_text: str, *, model: str, temperature: float, max_tokens: int, verbose: bool) -> str:
    """Ask the LLM to draft a commit message for *diff_text*."""

    system_prompt = (
        "You are Ada, a meticulous software engineer who writes excellent Git "
        "commit messages.\n"
        "Given a *unified* git diff, craft a concise commit message:\n"
        "  • **Same line** – poignant (3-5 words no puncuation).\n"
        "Respond with plaintext only – no code fences, no diff, no newlines."
    )

    user_prompt = f"Here is the diff:\n```diff\n{diff_text}\n```"

    api_key = os.getenv("GPTDIFF_LLM_API_KEY")
    if not api_key:
        print("Error: GPTDIFF_LLM_API_KEY is not set.", file=sys.stderr)
        sys.exit(1)
    base_url = os.getenv("GPTDIFF_LLM_BASE_URL", "https://nano-gpt.com/api/v1/")

    resp = call_llm(
        api_key=api_key,
        base_url=base_url,
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=max_tokens,
        temperature=temperature,
    )

    if verbose:
        u = resp.usage
        print(
            f"LLM usage – prompt {u.prompt_tokens}, completion {u.completion_tokens}, total {u.total_tokens}"
        )

    return resp.choices[0].message.content.strip()


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #


def _parse_args() -> argparse.Namespace:
    dflt_model = os.getenv("GPTDIFF_MODEL", "openai/gpt-4o-mini")
    p = argparse.ArgumentParser(
        prog="gptsummarize",
        description="Generate an LLM-powered Git commit message for the current repo.",
    )
    p.add_argument(
        "--all",
        action="store_true",
        help="Include unstaged working-tree edits as well as staged changes.",
    )
    p.add_argument(
        "--show-diff",
        action="store_true",
        help="Print a colourised diff before the summary.",
    )
    p.add_argument("--model", default=dflt_model, help=f"Model to use (default {dflt_model}).")
    p.add_argument("--temperature", type=float, default=0.3, help="LLM creativity (default 0.3).")
    p.add_argument(
        "--max_tokens",
        type=int,
        default=4096,
        help="Maximum tokens to request from the LLM (default 4096).",
    )
    p.add_argument("--verbose", action="store_true", help="Print usage/debug info.")
    return p.parse_args()


def main() -> None:
    args = _parse_args()

    diff_text = collect_diff(include_unstaged=args.all)
    if not diff_text.strip():
        print("No changes detected; working tree is clean.")
        sys.exit(0)

    if args.show_diff:
        print("\n\033[1;34mDiff to summarise:\033[0m")
        print(color_code_diff(diff_text))
        print("")

    summary = summarise(
        diff_text,
        model=args.model,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        verbose=args.verbose,
    )

    #print("\033[1;32mSuggested commit message:\033[0m\n")
    print(summary)


if __name__ == "__main__":
    main()
