#!/usr/bin/env python3
"""Review prompt-response pairs for missing fields and format issues."""
from __future__ import annotations
import argparse, json
from collections import Counter
from pathlib import Path
from typing import Any

REQUIRED = ("id", "prompt", "response", "instruction_check")

def validate_pair(item: dict[str, Any]) -> list[str]:
    issues = []
    for field in REQUIRED:
        if field not in item or str(item.get(field, "")).strip() == "":
            issues.append(f"missing:{field}")
    response = str(item.get("response", ""))
    expected = item.get("expected_format")
    if expected == "bullets" and "- " not in response:
        issues.append("format:expected_bullets")
    if expected == "json":
        try:
            json.loads(response)
        except Exception:
            issues.append("format:invalid_json")
    return issues

def review_file(path: Path) -> dict[str, Any]:
    pairs = json.loads(path.read_text(encoding="utf-8"))
    rows = []
    counts = Counter()
    for item in pairs:
        issues = validate_pair(item)
        for issue in issues:
            counts[issue] += 1
        rows.append({"id": item.get("id"), "ok": not issues, "issues": issues})
    return {
        "total": len(pairs),
        "passed": sum(1 for r in rows if r["ok"]),
        "failed": sum(1 for r in rows if not r["ok"]),
        "common_errors": dict(counts.most_common()),
        "rows": rows,
    }

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", default="reports/review_summary.json")
    args = parser.parse_args()
    result = review_file(Path(args.input))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"passed={result['passed']} failed={result['failed']} -> {out}")

if __name__ == "__main__":
    main()
