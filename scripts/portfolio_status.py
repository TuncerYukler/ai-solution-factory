#!/usr/bin/env python3
"""Print a table of all use cases: ID, name, department, phase, tier, status, next gate, days in phase.

Usage: python3 scripts/portfolio_status.py [--usecases-dir DIR]
"""

import argparse
import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import factory_lib as fl  # noqa: E402

COLUMNS = ["ID", "Name", "Department", "Phase", "Tier", "Status", "Next gate", "Days in phase"]


def row_for(path: Path) -> list:
    state = fl.load_yaml(path)
    gates = state.get("gates", {})
    next_gate = next((g for g in fl.GATES if gates.get(g, {}).get("status") != "passed"), None)
    passed_dates = [g.get("date") for g in gates.values() if g.get("status") == "passed" and g.get("date")]
    since = max(passed_dates + [state.get("created") or fl.today()])
    days = (datetime.date.today() - datetime.date.fromisoformat(since)).days
    invalid = " (INVALID)" if fl.validate_state(state) else ""
    return [
        state.get("id", path.parent.name), state.get("name", ""), state.get("department", ""),
        str(state.get("phase", "")), str(state.get("risk_tier") or "—"),
        str(state.get("status", "")) + invalid,
        next_gate.replace("_", " ").upper().split()[0] if next_gate else "—",
        str(days),
    ]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--usecases-dir", type=Path, default=fl.DEFAULT_USECASES)
    args = ap.parse_args(argv)

    rows = [row_for(p) for p in sorted(args.usecases_dir.glob("UC-*/usecase.yaml"))]
    if not rows:
        print("No use cases yet. Start one with /new-usecase <slug>.")
        return 0
    widths = [max(len(c), *(len(r[i]) for r in rows)) for i, c in enumerate(COLUMNS)]
    fmt = "| " + " | ".join("{:<%d}" % w for w in widths) + " |"
    print(fmt.format(*COLUMNS))
    print("|" + "|".join("-" * (w + 2) for w in widths) + "|")
    for r in rows:
        print(fmt.format(*r))
    active = args.usecases_dir / ".active"
    if active.exists():
        print("\nActive use case: {}".format(active.read_text(encoding="utf-8").strip()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
