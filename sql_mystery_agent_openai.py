"""An OpenAI Responses API agent for the SQL Murder Mystery.

The model starts with only the public crime prompt. It can inspect the SQLite
database with read-only queries and submit suspects to the game's own solution
checker. The on-disk database is never modified.
"""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional


DEFAULT_PROMPT = (
    "A murder occurred on January 15, 2018 in SQL City. "
    "Find the murderer and then solve the second stage to identify the person "
    "behind the crime."
)

SYSTEM_INSTRUCTIONS = """\
You are an autonomous SQL detective. Solve both stages of the SQL Murder
Mystery using only evidence obtained through the supplied tools.

Start with the user's prompt. Inspect SQLite's schema when needed, form
hypotheses, and use query_database to test them. Do not guess or use prior
knowledge of this game. Call submit_solution only when database evidence
supports a person's exact name.

The first accepted submission identifies the murderer. The database response
then tells you how to investigate the second stage. Continue until
submit_solution confirms the person behind the murder as well. Explain the
evidence for both conclusions in your final response.
"""


class MysteryDatabase:
    """An isolated, queryable copy of the game database."""

    def __init__(self, path: Path, max_rows: int = 100) -> None:
        self.path = path
        self.max_rows = max_rows
        self.stage_one_passed = False
        self.stage_two_passed = False
        self.failed_solution_submissions = 0

        if not path.is_file():
            raise FileNotFoundError("Database not found: {}".format(path))

        source = sqlite3.connect(str(path))
        self.connection = sqlite3.connect(":memory:")
        try:
            source.backup(self.connection)
        finally:
            source.close()

        self._denied_actions = {
            value
            for name in (
                "SQLITE_ATTACH",
                "SQLITE_CREATE_INDEX",
                "SQLITE_CREATE_TABLE",
                "SQLITE_CREATE_TEMP_INDEX",
                "SQLITE_CREATE_TEMP_TABLE",
                "SQLITE_CREATE_TEMP_TRIGGER",
                "SQLITE_CREATE_TEMP_VIEW",
                "SQLITE_CREATE_TRIGGER",
                "SQLITE_CREATE_VIEW",
                "SQLITE_DELETE",
                "SQLITE_DETACH",
                "SQLITE_DROP_INDEX",
                "SQLITE_DROP_TABLE",
                "SQLITE_DROP_TEMP_INDEX",
                "SQLITE_DROP_TEMP_TABLE",
                "SQLITE_DROP_TEMP_TRIGGER",
                "SQLITE_DROP_TEMP_VIEW",
                "SQLITE_DROP_TRIGGER",
                "SQLITE_DROP_VIEW",
                "SQLITE_INSERT",
                "SQLITE_PRAGMA",
                "SQLITE_REINDEX",
                "SQLITE_TRANSACTION",
                "SQLITE_UPDATE",
            )
            if (value := getattr(sqlite3, name, None)) is not None
        }
        self.connection.set_authorizer(self._authorize_read)

    def _authorize_read(
        self,
        action: int,
        _arg1: Optional[str],
        _arg2: Optional[str],
        _database: Optional[str],
        _trigger: Optional[str],
    ) -> int:
        if action in self._denied_actions:
            return sqlite3.SQLITE_DENY
        return sqlite3.SQLITE_OK

    def query(self, sql: str) -> str:
        """Run one read-only SQL statement and return compact JSON."""
        if not sql.strip():
            return json.dumps({"error": "The SQL query was empty."})

        try:
            cursor = self.connection.execute(sql)
            if cursor.description is None:
                return json.dumps({"error": "Only read-only queries are allowed."})

            columns = [item[0] for item in cursor.description]
            rows = cursor.fetchmany(self.max_rows + 1)
            truncated = len(rows) > self.max_rows
            rows = rows[: self.max_rows]
            result = {
                "columns": columns,
                "rows": [list(row) for row in rows],
                "row_count": len(rows),
                "truncated": truncated,
            }
            encoded = json.dumps(result, ensure_ascii=False, default=str)
            if len(encoded) > 20_000:
                return json.dumps(
                    {
                        "error": "Result was too large. Select fewer columns or rows.",
                        "row_count": len(rows),
                    }
                )
            return encoded
        except sqlite3.Error as error:
            return json.dumps({"error": str(error)})

    def submit_solution(self, name: str) -> str:
        """Ask the database's original trigger to check a suspect."""
        clean_name = name.strip()
        if not clean_name:
            return json.dumps({"error": "A suspect name is required."})

        # The solution trigger writes its verdict into the solution table.
        # Temporarily lift the read-only authorizer only for this parameterized
        # statement against the isolated in-memory database.
        self.connection.set_authorizer(None)
        try:
            self.connection.execute(
                "INSERT INTO solution (user, value) VALUES (?, ?)",
                (1, clean_name),
            )
            verdict_row = self.connection.execute(
                "SELECT value FROM solution LIMIT 1"
            ).fetchone()
            self.connection.commit()
        except sqlite3.Error as error:
            self.connection.rollback()
            return json.dumps({"error": str(error)})
        finally:
            self.connection.set_authorizer(self._authorize_read)

        verdict = str(verdict_row[0]) if verdict_row else "No verdict returned."
        accepted = False
        if "found the murderer" in verdict:
            self.stage_one_passed = True
            accepted = True
        if "found the brains behind the murder" in verdict:
            self.stage_two_passed = True
            accepted = True
        if not accepted:
            self.failed_solution_submissions += 1

        return json.dumps(
            {
                "submitted_name": clean_name,
                "verdict": verdict,
                "stage_one_passed": self.stage_one_passed,
                "stage_two_passed": self.stage_two_passed,
                "failed_solution_submissions": self.failed_solution_submissions,
            },
            ensure_ascii=False,
        )

    @property
    def solved(self) -> bool:
        return self.stage_one_passed and self.stage_two_passed

    def close(self) -> None:
        self.connection.close()


class ResponsesClient:
    """Minimal dependency-free client for POST /v1/responses."""

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
        self.request_count = 0

    def create(
        self,
        input_data: Any,
        tools: List[Dict[str, Any]],
        previous_response_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        self.request_count += 1
        payload: Dict[str, Any] = {
            "model": self.model,
            "instructions": SYSTEM_INSTRUCTIONS,
            "input": input_data,
            "tools": tools,
            "reasoning": {"effort": self.reasoning_effort},
            "text": {"verbosity": "low"},
        }
        if previous_response_id:
            payload["previous_response_id"] = previous_response_id

        request = urllib.request.Request(
            "https://api.openai.com/v1/responses",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": "Bearer {}".format(self.api_key),
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            details = error.read().decode("utf-8", errors="replace")
            raise RuntimeError(
                "OpenAI API returned HTTP {}: {}".format(error.code, details)
            ) from error
        except urllib.error.URLError as error:
            raise RuntimeError("Could not reach the OpenAI API: {}".format(error)) from error


TOOLS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "name": "query_database",
        "description": (
            "Execute one read-only SQLite statement. Returns JSON with columns, "
            "rows, row_count, and truncated, or an error. Results are limited "
            "to 100 rows; narrow large queries."
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
        "strict": True,
    },
    {
        "type": "function",
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
                    "description": "The exact full name supported by the evidence.",
                }
            },
            "required": ["name"],
            "additionalProperties": False,
        },
        "strict": True,
    },
]


def _response_text(response: Dict[str, Any]) -> str:
    if isinstance(response.get("output_text"), str):
        return response["output_text"]

    parts: List[str] = []
    for item in response.get("output", []):
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                parts.append(content.get("text", ""))
    return "\n".join(parts)


def format_run_metrics(
    turns: int,
    failed_submissions: int,
    elapsed_seconds: float,
) -> str:
    """Format provider-independent benchmark metrics."""
    turn_label = "turn" if turns == 1 else "turns"
    failure_label = (
        "failed solution submission"
        if failed_submissions == 1
        else "failed solution submissions"
    )
    return "Run metrics: {} model {}, {} {}, {:.2f} seconds total.".format(
        turns,
        turn_label,
        failed_submissions,
        failure_label,
        elapsed_seconds,
    )


def run_agent(
    database: MysteryDatabase,
    client: ResponsesClient,
    prompt: str = DEFAULT_PROMPT,
    max_tool_calls: int = 30,
    verbose: bool = True,
) -> str:
    """Run the model/tool loop until both database stages pass."""
    response = client.create(prompt, TOOLS)
    tool_call_count = 0

    while True:
        calls = [
            item
            for item in response.get("output", [])
            if item.get("type") == "function_call"
        ]

        if not calls:
            final_text = _response_text(response)
            if database.solved:
                return final_text
            raise RuntimeError(
                "The model stopped before both stages passed. Last response:\n{}".format(
                    final_text or "(no text)"
                )
            )

        outputs: List[Dict[str, str]] = []
        for call in calls:
            tool_call_count += 1
            if tool_call_count > max_tool_calls:
                raise RuntimeError(
                    "Tool-call limit ({}) reached before solving both stages.".format(
                        max_tool_calls
                    )
                )

            try:
                arguments = json.loads(call.get("arguments", "{}"))
            except json.JSONDecodeError as error:
                result = json.dumps({"error": "Invalid tool arguments: {}".format(error)})
            else:
                if call.get("name") == "query_database":
                    result = database.query(arguments.get("sql", ""))
                elif call.get("name") == "submit_solution":
                    result = database.submit_solution(arguments.get("name", ""))
                else:
                    result = json.dumps(
                        {"error": "Unknown tool: {}".format(call.get("name"))}
                    )

            if verbose:
                print(
                    "[{}] {}\n{}\n".format(
                        tool_call_count,
                        call.get("name", "unknown"),
                        result,
                    ),
                    flush=True,
                )
            outputs.append(
                {
                    "type": "function_call_output",
                    "call_id": call["call_id"],
                    "output": result,
                }
            )

        response = client.create(
            outputs,
            TOOLS,
            previous_response_id=response["id"],
        )


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Let an OpenAI model solve both stages of SQL Murder Mystery."
    )
    parser.add_argument(
        "--database",
        type=Path,
        default=Path(__file__).with_name("sql-murder-mystery.db"),
        help="Path to sql-murder-mystery.db.",
    )
    parser.add_argument(
        "--model",
        default=os.environ.get("OPENAI_MODEL", "gpt-5.6-sol"),
        help="Responses API model (default: gpt-5.6-sol).",
    )
    parser.add_argument(
        "--reasoning-effort",
        choices=("none", "low", "medium", "high", "xhigh", "max"),
        default="medium",
    )
    parser.add_argument("--max-tool-calls", type=int, default=30)
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print(
            "OPENAI_API_KEY is not set. Set it in your environment and try again.",
            file=sys.stderr,
        )
        return 2

    database = MysteryDatabase(args.database)
    client = ResponsesClient(
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
