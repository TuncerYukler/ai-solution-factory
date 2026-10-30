#!/usr/bin/env python3
"""PostToolUse hook for Write/Edit: validate usecase.yaml against the schema after every change.

Exit code 2 sends the errors back to Claude so it fixes the file immediately.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import factory_lib as fl  # noqa: E402

try:
    event = json.load(sys.stdin)
except ValueError:
    sys.exit(0)
raw = (event.get("tool_input") or {}).get("file_path", "")
if Path(raw).name != "usecase.yaml":
    sys.exit(0)
path = Path(raw)
if not path.is_absolute():
    path = Path(event.get("cwd") or ".") / path
try:
    errors = fl.validate_state(fl.load_yaml(path))
except Exception as exc:  # unreadable YAML is also invalid state
    errors = ["{} could not be parsed: {}".format(path.name, exc)]
if errors:
    print("usecase.yaml is now INVALID. Fix it before doing anything else:\n" + "\n".join(errors), file=sys.stderr)
    sys.exit(2)
sys.exit(0)
