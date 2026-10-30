#!/usr/bin/env python3
"""Scaffold a new use case: next free ID, folder tree, usecase.yaml with defaults.

Usage: python3 scripts/new_usecase.py <slug> [--name N] [--department D]
           [--sponsor S] [--sme X --sme Y] [--product-owner P]
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import factory_lib as fl  # noqa: E402


def next_id(usecases_dir: Path) -> str:
    nums = [int(m.group(1)) for p in usecases_dir.glob("UC-*")
            for m in [re.match(r"UC-(\d+)", p.name)] if m]
    return "UC-{:03d}".format(max(nums, default=0) + 1)


def git_user() -> str:
    try:
        out = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True, timeout=5)
        return out.stdout.strip() or "TBD"
    except (OSError, subprocess.SubprocessError):
        return "TBD"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug")
    ap.add_argument("--name")
    ap.add_argument("--department", default="TBD")
    ap.add_argument("--sponsor", default="TBD")
    ap.add_argument("--sme", action="append", default=[])
    ap.add_argument("--product-owner")
    ap.add_argument("--usecases-dir", type=Path, default=fl.DEFAULT_USECASES)
    args = ap.parse_args(argv)

    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", args.slug):
        print("Slug must be lower-case words joined by hyphens, e.g. invoice-triage", file=sys.stderr)
        return 1
    usecases = args.usecases_dir
    usecases.mkdir(parents=True, exist_ok=True)
    if any(p.name.endswith("-" + args.slug) for p in usecases.glob("UC-*")):
        print("A use case with slug '{}' already exists".format(args.slug), file=sys.stderr)
        return 1

    uc_id = next_id(usecases)
    folder = usecases / "{}-{}".format(uc_id, args.slug)
    for d in fl.PHASE_DIRS:
        (folder / d).mkdir(parents=True, exist_ok=True)
    (folder / "inputs" / "README.md").write_text(
        "Drop department material here: meeting notes, documents, sample data.\n"
        "Skills read this folder and never edit it.\n", encoding="utf-8")

    state = {
        "id": uc_id,
        "slug": args.slug,
        "name": args.name or args.slug.replace("-", " ").capitalize(),
        "department": args.department,
        "sponsor": args.sponsor,
        "smes": args.sme,
        "product_owner": args.product_owner or git_user(),
        "created": fl.today(),
        "phase": 0,
        "status": "in_progress",
        "risk_tier": None,
        "autonomy_target": None,
        "data_classification": None,
        "pattern": None,
        "gates": {g: {"status": "open"} for g in fl.GATES},
        "decisions": [],
        "open_questions": [],
    }
    errors = fl.validate_state(state)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    fl.dump_yaml(state, folder / "usecase.yaml")
    (usecases / ".active").write_text(uc_id + "\n", encoding="utf-8")

    print("Created {} at {}".format(uc_id, folder))
    print("Active use case set to {}.".format(uc_id))
    print("Next: drop department material into {}/inputs/, then run /intake.".format(folder.name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
