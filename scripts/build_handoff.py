#!/usr/bin/env python3
"""Assemble usecases/<id>/handoff/ from the phase outputs. Requires G3 passed.

Usage: python3 scripts/build_handoff.py [UC-001] [--by NAME]
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import factory_lib as fl  # noqa: E402

# handoff path -> source path inside the use case folder
LAYOUT = {
    "requirements/usecase-canvas.md": "01-requirements/usecase-canvas.md",
    "requirements/process-map.md": "01-requirements/process-map.md",
    "requirements/nfr.md": "01-requirements/nfr.md",
    "architecture/solution-architecture.md": "03-design/solution-architecture.md",
    "architecture/component-map.md": "02-stack/component-map.md",
    "architecture/tech-decisions.md": "02-stack/tech-decisions.md",
    "hitl/hitl-design.md": "03-design/hitl-design.md",
    "security/threat-model.md": "03-design/threat-model.md",
    "backlog.md": "03-design/backlog.md",
    "evals/eval-golden-set.csv": "03-design/eval-golden-set.csv",
    "evals/test-plan.md": "04-testing/test-plan.md",
}


def fill(template: str, values: dict) -> str:
    return re.sub(r"\{\{(\w+)\}\}", lambda m: str(values.get(m.group(1), "")), template)


def component_rows(folder: Path):
    path = folder / fl.ARTIFACTS["components"][1]
    if not path.exists():
        return []
    rows = fl.table_rows(fl.sections(path.read_text(encoding="utf-8")).get("Layers", ""))
    return [(r + [""] * 5)[:5] for r in rows if len(r) > 1 and r[1].lower() == "needed"]


def agent_limits(folder: Path):
    limits = []
    for spec in sorted((folder / fl.AGENTS_DIR).glob("*.md")):
        m = re.search(r"Level:\s*(L[0-3])", fl.sections(spec.read_text(encoding="utf-8")).get("Autonomy level", ""))
        limits.append((spec.stem, m.group(1) if m else "UNSET"))
    return limits


def dev_claude_md(state: dict, folder: Path) -> str:
    comps = component_rows(folder)
    reuse = [r for r in comps if r[3].lower() in ("reuse", "extend")]
    new = [r for r in comps if r[3].lower() == "new"]
    lines = [
        "# {} {} — build rules for Claude Code".format(state["id"], state["name"]),
        "",
        "This repository builds the solution designed in the AI Solution Factory handoff package.",
        "Design documents are the source of truth; if code and design disagree, raise it with the product owner ({}).".format(state["product_owner"]),
        "",
        "## Architecture to follow",
        "- Pattern: `{}`. Do not introduce agents or orchestration beyond `architecture/solution-architecture.md`.".format(state.get("pattern")),
        "- Use only the technologies in `architecture/component-map.md`.",
        "- Data classification: {}. Never log or send this data anywhere the threat model does not allow.".format(state.get("data_classification")),
        "",
        "## Reuse these internal components (do not rebuild them)",
    ]
    lines += ["- {} — {} ({}, owner: {})".format(r[0], r[2], r[3], r[4] or "see component-library") for r in reuse] or ["- None"]
    lines += ["", "## New components to build"]
    lines += ["- {} — {}".format(r[0], r[2]) for r in new] or ["- None"]
    lines += ["", "## Autonomy limits per agent (never exceed in code)",
              "Overall autonomy target: {}. A HITL step in `hitl/hitl-design.md` must never be bypassable.".format(state.get("autonomy_target"))]
    lines += ["- `{}`: {}".format(a, lvl) for a, lvl in agent_limits(folder)] or ["- No agents in this design."]
    lines += [
        "",
        "## Definition of done",
        "- The golden set in `evals/eval-golden-set.csv` must pass at or above the accuracy target in `requirements/nfr.md` before any PR to main.",
        "- Every story in `backlog.md` keeps its BR / AC trace in the PR description.",
        "- Controls in `security/threat-model.md` are implemented, not deferred.",
        "- Overrides and approvals are logged as specified in `hitl/hitl-design.md`.",
    ]
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("usecase", nargs="?")
    ap.add_argument("--by", help="name recorded in the decision log (default: product owner)")
    ap.add_argument("--usecases-dir", type=Path, default=fl.DEFAULT_USECASES)
    args = ap.parse_args(argv)

    folder = fl.find_usecase(args.usecase, args.usecases_dir)
    state_path = folder / "usecase.yaml"
    state = fl.load_yaml(state_path)
    errors = fl.validate_state(state)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    if state["gates"]["g3_design"]["status"] != "passed":
        print("G3 is not passed for {}. Run /gate 3 first.".format(state["id"]), file=sys.stderr)
        return 1

    out = folder / "handoff"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir()
    copied, skipped = [], []
    for dest, src in LAYOUT.items():
        s = folder / src
        if s.exists():
            (out / dest).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(s, out / dest)
            copied.append(dest)
        else:
            skipped.append(dest)
    agents = sorted((folder / fl.AGENTS_DIR).glob("*.md"))
    (out / "agents").mkdir(exist_ok=True)
    for spec in agents:
        shutil.copy2(spec, out / "agents" / spec.name)
        copied.append("agents/" + spec.name)

    canvas = folder / fl.ARTIFACTS["canvas"][1]
    purpose = fl.sections(canvas.read_text(encoding="utf-8")).get("Purpose", "").strip() if canvas.exists() else ""
    contacts = ["- Product owner: {}".format(state["product_owner"]),
                "- Sponsor: {} ({})".format(state["sponsor"], state["department"])]
    contacts += ["- SME: {}".format(s) for s in state.get("smes", [])]
    values = dict(state)
    values.update({
        "purpose": purpose or "See requirements/usecase-canvas.md.",
        "contents": "\n".join("- `{}`".format(c) for c in sorted(copied)),
        "open_questions": "\n".join("- {} (owner: {})".format(q["question"], q["owner"])
                                    for q in state.get("open_questions", [])) or "None.",
        "contacts": "\n".join(contacts),
    })
    template = (fl.TEMPLATES / "handoff-readme.md").read_text(encoding="utf-8")
    (out / "README.md").write_text(fill(template, values), encoding="utf-8")
    (out / "CLAUDE.md").write_text(dev_claude_md(state, folder), encoding="utf-8")

    state["status"] = "handed_off"
    state["decisions"].append({"date": fl.today(), "decision": "Handoff package built for development",
                               "by": args.by or state["product_owner"]})
    fl.dump_yaml(state, state_path)

    print("Handoff package written to {}".format(out))
    print("  {} files copied, plus README.md and CLAUDE.md".format(len(copied)))
    if skipped:
        print("  Not yet available (add later and re-run): {}".format(", ".join(skipped)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
