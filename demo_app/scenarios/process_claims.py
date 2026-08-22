"""Batch-process one or more claim files through handle_claim().

Usage:
    python -m demo_app.scenarios.process_claims demo_app/sample_claims
    python -m demo_app.scenarios.process_claims path/to/claim1.json path/to/claim2.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from demo_app.agent import handle_claim  # noqa: E402
from demo_app.claim_files import build_message, find_claim_files, load_claim_file  # noqa: E402
from demo_app.db import get_client  # noqa: E402


def process_claim_file(path: Path) -> dict:
    claim = load_claim_file(path)
    client = get_client()
    client.table("claims").upsert(
        {
            "claim_id": claim["claim_id"],
            "category": claim["category"],
            "description": claim.get("description", ""),
            "amount": claim["amount"],
            "status": "pending",
        }
    ).execute()

    message = build_message(claim)
    result = handle_claim(claim["claim_id"], message)
    return {"file": str(path), "claim_id": claim["claim_id"], **result}


def main(argv: list[str]) -> None:
    if not argv:
        print("Usage: python -m demo_app.scenarios.process_claims <file_or_dir> [...]", file=sys.stderr)
        sys.exit(1)

    files = find_claim_files(argv)
    if not files:
        print("No .json claim files found.", file=sys.stderr)
        sys.exit(1)

    results = []
    for path in files:
        print(f"Processing {path} ...")
        result = process_claim_file(path)
        results.append(result)
        print(json.dumps(result, indent=2))

    print(f"\nProcessed {len(results)} claim(s).")


if __name__ == "__main__":
    main(sys.argv[1:])
