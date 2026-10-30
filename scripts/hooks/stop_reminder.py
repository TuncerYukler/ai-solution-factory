#!/usr/bin/env python3
"""Stop hook: remind the product owner of open questions and the next command for the active use case."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import factory_lib as fl  # noqa: E402

NEXT = {
    "g0_intake": "/intake, then /gate 0",
    "g1_requirements": "/discover, then /gate 1",
    "g2_stack": "/stack, then /gate 2",
    "g3_design": "/design, then /gate 3",
    "g4_test": "/test-plan and /rollout; /gate 4 once eval results are in",
    "g5_rollout": "/gate 5 once pilot results are in",
}

try:
    json.load(sys.stdin)
except ValueError:
    pass
try:
    folder = fl.find_usecase(None)
    state = fl.load_yaml(folder / "usecase.yaml")
except (SystemExit, OSError, ValueError):
    sys.exit(0)
if state.get("status") not in ("in_progress", "blocked", "handed_off"):
    sys.exit(0)
gate = next((g for g in fl.GATES if state["gates"].get(g, {}).get("status") != "passed"), None)
if not gate:
    sys.exit(0)
questions = state.get("open_questions", [])
msg = "{} {}: next {}.".format(state["id"], state["name"], NEXT[gate])
if questions:
    msg += " {} open question(s), e.g. \"{}\" (owner: {}).".format(
        len(questions), questions[0]["question"], questions[0]["owner"])
print(json.dumps({"systemMessage": msg}))
sys.exit(0)
