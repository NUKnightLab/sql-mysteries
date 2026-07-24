"""An OpenRouter tool-using agent for the SQL Murder Mystery.

The model starts with only the public crime prompt. It can inspect an isolated
copy of the SQLite database and submit suspects to the game's own checker.
OpenRouter provides access to tool-capable models from multiple providers.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

from sql_mystery_agent_openai import (
    DEFAULT_PROMPT,
    format_run_metrics,
    MysteryDatabase,
    SYSTEM_INSTRUCTIONS,
)


OPENROUTER_TOOLS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "query_database",
            "description": (
                "Execute one read-only SQLite statement. Returns JSON with "
                "columns, rows, row_count, and truncated, or an error. Results "
                "are limited to 100 rows; narrow large queries."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "sql": {
                        "type": "string",
                        "description": "A single read-only SQLite query.",
                    }
                },
                "required": ["sql"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "submit_solution",
            "description": (
                "Submit one person's exact name to the game's built-in checker. "
                "Returns the database verdict and both stage-completion flags."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": (
                            "The exact full name supported by the evidence."
                        ),
                    }
                },
                "required": ["name"],
                "additionalProperties": False,
            },
        },
    },
]


class OpenRouterClient:
    """Dependency-free client for OpenRouter chat completions."""

    def __init__(
        self,
        api_key: str,
        model: str,
        reasoning_effort: str = "medium",
        timeout: int = 120,
    ) -> None:
        self.api_key = api_key
        self.model = model
        self.reasoning_effort = reasoning_effort
        self.timeout = timeout
        self.session_id = "sql-mystery-{}".format(uuid.uuid4().hex)
        self.request_count = 0

    def create(
        self,
        messages: List[Dict[str, Any]],
        tools: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        self.request_count += 1
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "tools": tools,
            "tool_choice": "auto",
            "parallel_tool_calls": False,
            "reasoning": {"effort": self.reasoning_effort},
            "session_id": self.session_id,
        }

        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Content-Type": "application/json",
            "X-Title": "SQL Murder Mystery Agent",
        }
        site_url = os.environ.get("OPENROUTER_SITE_URL")
        if site_url:
            headers["HTTP-Referer"] = site_url

        request = urllib.request.Request(
            "https://openrouter.ai/api/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            details = error.read().decode("utf-8", errors="replace")
            raise RuntimeError(
                "OpenRouter returned HTTP {}: {}".format(error.code, details)
            ) from error
        except urllib.error.URLError as error:
            raise RuntimeError("Could not reach OpenRouter: {}".format(error)) from error


def _message_text(message: Dict[str, Any]) -> str:
    content = message.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and isinstance(item.get("text"), str):
                parts.append(item["text"])
        return "\n".join(parts)
    return ""


def _execute_tool(database: MysteryDatabase, call: Dict[str, Any]) -> str:
    function = call.get("function") or {}
    try:
        arguments = json.loads(function.get("arguments") or "{}")
    except json.JSONDecodeError as error:
        return json.dumps({"error": "Invalid tool arguments: {}".format(error)})

    name = function.get("name")
    if name == "query_database":
        return database.query(arguments.get("sql", ""))
    if name == "submit_solution":
        return database.submit_solution(arguments.get("name", ""))
    return json.dumps({"error": "Unknown tool: {}".format(name)})


def run_agent(
    database: MysteryDatabase,
    client: OpenRouterClient,
    prompt: str = DEFAULT_PROMPT,
    max_tool_calls: int = 30,
    verbose: bool = True,
) -> str:
    """Run the OpenRouter model/tool loop until both database stages pass."""
    messages: List[Dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_INSTRUCTIONS},
        {"role": "user", "content": prompt},
    ]
    tool_call_count = 0
    last_model: Optional[str] = None

    while True:
        response = client.create(messages, OPENROUTER_TOOLS)
        if response.get("error"):
            raise RuntimeError(
                "OpenRouter error: {}".format(json.dumps(response["error"]))
            )

        choices = response.get("choices") or []
        if not choices or not isinstance(choices[0].get("message"), dict):
            raise RuntimeError(
                "OpenRouter returned no assistant message: {}".format(
                    json.dumps(response)
                )
            )

        served_model = response.get("model")
        if verbose and served_model and served_model != last_model:
            print("[model] {}\n".format(served_model), flush=True)
            last_model = served_model

        # Preserve this object intact. Some providers return reasoning_details
        # that must be sent back unmodified when continuing after a tool call.
        assistant_message = choices[0]["message"]
        calls = assistant_message.get("tool_calls") or []

        if not calls:
            final_text = _message_text(assistant_message)
            if database.solved:
                return final_text
            raise RuntimeError(
                "The model stopped before both stages passed. Last response:\n{}".format(
                    final_text or "(no text)"
                )
            )

        messages.append(assistant_message)
        for call in calls:
            tool_call_count += 1
            if tool_call_count > max_tool_calls:
                raise RuntimeError(
                    "Tool-call limit ({}) reached before solving both stages.".format(
                        max_tool_calls
                    )
                )

            result = _execute_tool(database, call)
            function = call.get("function") or {}
            if verbose:
                print(
                    "[{}] {}\n{}\n".format(
                        tool_call_count,
                        function.get("name", "unknown"),
                        result,
                    ),
                    flush=True,
                )

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.get("id", ""),
                    "name": function.get("name", "unknown"),
                    "content": result,
                }
            )


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Let an OpenRouter model solve both stages of SQL Murder Mystery."
        )
    )
    parser.add_argument(
        "--database",
        type=Path,
        default=Path(__file__).with_name("sql-murder-mystery.db"),
        help="Path to sql-murder-mystery.db.",
    )
    parser.add_argument(
        "--model",
        default=os.environ.get("OPENROUTER_MODEL", "openrouter/auto-beta"),
        help=(
            "OpenRouter model slug (default: OPENROUTER_MODEL or "
            "openrouter/auto-beta). The model must support tool calling."
        ),
    )
    parser.add_argument(
        "--reasoning-effort",
        choices=("none", "minimal", "low", "medium", "high", "xhigh"),
        default="medium",
    )
    parser.add_argument("--max-tool-calls", type=int, default=30)
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print(
            "OPENROUTER_API_KEY is not set. Set it in your environment and try again.",
            file=sys.stderr,
        )
        return 2

    database = MysteryDatabase(args.database)
    client = OpenRouterClient(
        api_key=api_key,
        model=args.model,
        reasoning_effort=args.reasoning_effort,
    )
    started_at = time.perf_counter()
    try:
        final_text = run_agent(
            database,
            client,
            max_tool_calls=args.max_tool_calls,
        )
        print("Solved both stages.\n")
        print(final_text)
        return 0
    except (RuntimeError, OSError) as error:
        print("Agent failed: {}".format(error), file=sys.stderr)
        return 1
    finally:
        database.close()
        elapsed_seconds = time.perf_counter() - started_at
        print(
            format_run_metrics(
                client.request_count,
                database.failed_solution_submissions,
                elapsed_seconds,
            )
        )


if __name__ == "__main__":
    raise SystemExit(main())
