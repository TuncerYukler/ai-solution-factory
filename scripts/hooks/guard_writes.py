#!/usr/bin/env python3
"""PreToolUse hook for Write/Edit: protect department originals and the framework.

- Blocks any write inside usecases/*/inputs/.
- Blocks writes to framework/ unless the product owner is maintaining it:
  create the file .claude/maintain-framework (or set FACTORY_MAINTAIN=1).
Exit code 2 blocks the tool call and shows the reason to Claude.
"""

import json
import os
import sys
from pathlib import Path

root = Path(os.environ.get("CLAUDE_PROJECT_DIR", Path(__file__).resolve().parents[2])).resolve()
try:
    event = json.load(sys.stdin)
except ValueError:
    sys.exit(0)
raw = (event.get("tool_input") or {}).get("file_path") or (event.get("tool_input") or {}).get("notebook_path")
if not raw:
    sys.exit(0)
path = Path(raw)
if not path.is_absolute():
    path = Path(event.get("cwd") or root) / path
try:
    parts = path.resolve().relative_to(root).parts
except ValueError:
    sys.exit(0)

if len(parts) >= 3 and parts[0] == "usecases" and parts[2] == "inputs":
    print("Blocked: usecases/*/inputs/ holds department originals and is read-only. "
          "Write your output to the phase folder instead.", file=sys.stderr)
    sys.exit(2)

maintaining = os.environ.get("FACTORY_MAINTAIN") == "1" or (root / ".claude" / "maintain-framework").exists()
if parts and parts[0] == "framework" and not maintaining:
    print("Blocked: framework/ is owned by the product owner. If they asked you to maintain the framework, "
          "ask them to run `touch .claude/maintain-framework` (and remove it afterwards).", file=sys.stderr)
    sys.exit(2)
sys.exit(0)
