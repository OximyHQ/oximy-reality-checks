#!/usr/bin/env python3
"""Validate a did-it-land JSON evidence ledger."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


VERDICTS = {"verified", "partial", "failed", "claimed-only", "unknown", "not-applicable"}
OVERALL = {"verified-complete", "partially-verified", "failed", "not-verifiable"}


def validate(payload: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["root must be an object"]
    for field in ("task", "checked_at", "overall_status", "claims"):
        if field not in payload:
            errors.append(f"missing root field: {field}")
    if payload.get("overall_status") not in OVERALL:
        errors.append(f"overall_status must be one of {sorted(OVERALL)}")
    claims = payload.get("claims")
    if not isinstance(claims, list) or not claims:
        errors.append("claims must be a non-empty array")
        return errors
    for index, claim in enumerate(claims):
        prefix = f"claims[{index}]"
        if not isinstance(claim, dict):
            errors.append(f"{prefix} must be an object")
            continue
        for field in ("claim", "required", "system_of_record", "verdict"):
            if field not in claim:
                errors.append(f"{prefix} missing {field}")
        if claim.get("verdict") not in VERDICTS:
            errors.append(f"{prefix}.verdict must be one of {sorted(VERDICTS)}")
        if not isinstance(claim.get("required"), bool):
            errors.append(f"{prefix}.required must be boolean")
        evidence = claim.get("evidence", [])
        gap = claim.get("evidence_gap", "")
        if claim.get("verdict") == "verified" and not evidence:
            errors.append(f"{prefix} is verified without evidence")
        if claim.get("verdict") in {"claimed-only", "unknown"} and not gap:
            errors.append(f"{prefix} needs evidence_gap for {claim.get('verdict')}")
    required = [c for c in claims if isinstance(c, dict) and c.get("required")]
    if payload.get("overall_status") == "verified-complete" and any(c.get("verdict") != "verified" for c in required):
        errors.append("verified-complete requires every required claim to be verified")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    try:
        payload = json.loads(args.report.read_text())
    except (OSError, json.JSONDecodeError) as error:
        print(f"validate_outcome: {error}", file=sys.stderr)
        return 2
    errors = validate(payload)
    if errors:
        print(json.dumps({"valid": False, "errors": errors}, indent=2))
        return 1
    print(json.dumps({"valid": True, "claims": len(payload["claims"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

