"""Shared helpers for the AI Solution Factory scripts.

Standard library plus PyYAML and jsonschema only. No network access.
"""

import csv
import datetime
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import jsonschema
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
FRAMEWORK = REPO_ROOT / "framework"
TEMPLATES = FRAMEWORK / "templates"
REFERENCE = FRAMEWORK / "reference"
SCHEMA_PATH = FRAMEWORK / "schemas" / "usecase.schema.json"
DEFAULT_USECASES = REPO_ROOT / "usecases"

GATES = ["g0_intake", "g1_requirements", "g2_stack", "g3_design", "g4_test", "g5_rollout"]

PHASE_DIRS = ["inputs", "00-intake", "01-requirements", "02-stack", "03-design",
              "03-design/agents", "04-testing", "05-rollout", "reviews", "handoff"]

# key: (template file, path inside the use case folder)
ARTIFACTS = {
    "intake": ("00-intake.md", "00-intake/intake.md"),
    "canvas": ("01-usecase-canvas.md", "01-requirements/usecase-canvas.md"),
    "process": ("01-process-map.md", "01-requirements/process-map.md"),
    "nfr": ("01-nfr.md", "01-requirements/nfr.md"),
    "components": ("02-component-map.md", "02-stack/component-map.md"),
    "decisions": ("02-tech-decisions.md", "02-stack/tech-decisions.md"),
    "architecture": ("03-solution-architecture.md", "03-design/solution-architecture.md"),
    "hitl": ("03-hitl-design.md", "03-design/hitl-design.md"),
    "threats": ("03-threat-model.md", "03-design/threat-model.md"),
    "backlog": ("03-backlog.md", "03-design/backlog.md"),
    "golden": ("03-eval-golden-set.csv", "03-design/eval-golden-set.csv"),
    "testplan": ("04-test-plan.md", "04-testing/test-plan.md"),
    "rollout": ("05-rollout-plan.md", "05-rollout/rollout-plan.md"),
}
AGENT_TEMPLATE = "03-agent-spec.md"
AGENTS_DIR = "03-design/agents"

LAYERS = [
    "Channel / UI", "Orchestration", "Models", "Knowledge and retrieval",
    "Tools and integrations", "Memory and state", "HITL workflow", "Guardrails",
    "Identity and access", "Observability and evaluation", "Hosting and environments",
]

GOLDEN_SET_MINIMUM = {1: 25, 2: 100, 3: 250}
AUTONOMY_ORDER = ["L0", "L1", "L2", "L3"]
TIER1_NA = "N/A (tier 1)"


# ---------- use case state ----------

def _stringify_dates(value):
    """PyYAML turns unquoted 2026-10-30 into a date; the schema wants strings."""
    if isinstance(value, (datetime.date, datetime.datetime)):
        return value.isoformat()[:10]
    if isinstance(value, dict):
        return {k: _stringify_dates(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_stringify_dates(v) for v in value]
    return value


def load_yaml(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return _stringify_dates(data)


def dump_yaml(data: dict, path: Path) -> None:
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True, width=100)


def validate_state(data: dict) -> List[str]:
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        schema = json.load(f)
    validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
    errors = []
    for err in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        where = "/".join(str(p) for p in err.path) or "(root)"
        errors.append("usecase.yaml {}: {}".format(where, err.message))
    return errors


def find_usecase(ref: Optional[str], usecases_dir: Path = DEFAULT_USECASES) -> Path:
    """Resolve 'UC-001', 'UC-001-slug', a slug, or None (uses usecases/.active)."""
    if ref is None:
        active = usecases_dir / ".active"
        if not active.exists():
            raise SystemExit("No use case given and no usecases/.active file. Pass an ID like UC-001.")
        ref = active.read_text(encoding="utf-8").strip()
    direct = Path(ref)
    if direct.is_dir() and (direct / "usecase.yaml").exists():
        return direct.resolve()
    matches = [p for p in sorted(usecases_dir.glob("UC-*"))
               if p.is_dir() and (p.name == ref or p.name.startswith(ref + "-") or p.name.endswith("-" + ref))]
    if len(matches) != 1:
        raise SystemExit("Use case '{}' not found (or ambiguous) in {}".format(ref, usecases_dir))
    return matches[0]


def today() -> str:
    return datetime.date.today().isoformat()


# ---------- markdown parsing ----------

COMMENT_RE = re.compile(r"<!--.*?-->", re.S)


def strip_comments(text: str) -> str:
    return COMMENT_RE.sub("", text)


def sections(text: str, level: int = 2) -> Dict[str, str]:
    """Map heading text -> body for headings of the given level.

    A body runs until the next heading of the same or higher level.
    Fenced code blocks are kept as body text and never split.
    """
    text = strip_comments(text)
    out: Dict[str, str] = {}
    current = None
    body: List[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
        m = None if in_fence else re.match(r"^(#{1,6})\s+(.*?)\s*$", line)
        if m and len(m.group(1)) <= level:
            if current is not None:
                out[current] = "\n".join(body)
            current = m.group(2) if len(m.group(1)) == level else None
            body = []
        elif current is not None:
            body.append(line)
    if current is not None:
        out[current] = "\n".join(body)
    return out


def _meaningful_lines(body: str) -> List[str]:
    lines = []
    for line in body.splitlines():
        s = line.strip()
        if not s or re.fullmatch(r"\|?[\s:\-|]+\|?", s):
            continue
        lines.append(s)
    return lines


def template_sections(template_name: str) -> Dict[str, List[str]]:
    text = (TEMPLATES / template_name).read_text(encoding="utf-8")
    return {h: _meaningful_lines(b) for h, b in sections(text).items()}


def empty_sections(text: str, template_name: str, required: Optional[List[str]] = None) -> Tuple[List[str], List[str]]:
    """Return (missing headings, empty headings) compared with the template.

    A section is empty when everything in it is still the template's own text
    (placeholders, header rows, example diagrams).
    """
    tmpl = template_sections(template_name)
    filled = sections(text)
    missing, empty = [], []
    for heading in (required if required is not None else list(tmpl)):
        if heading not in filled:
            missing.append(heading)
            continue
        lines = _meaningful_lines(filled[heading])
        if not [l for l in lines if l not in tmpl.get(heading, [])]:
            empty.append(heading)
    return missing, empty


def table_records(body: str, columns: List[str]) -> List[Dict[str, str]]:
    """Rows of the first table as dicts keyed by the wanted column names.

    Columns are found by header name (case-insensitive), so extra columns
    such as "Description" don't shift anything. Falls back to position when
    a header is missing.
    """
    header: List[str] = []
    for line in body.splitlines():
        s = line.strip()
        if s.startswith("|"):
            header = [c.strip().strip("*").lower() for c in s.strip("|").split("|")]
            break
    index = {}
    for pos, col in enumerate(columns):
        index[col] = header.index(col.lower()) if col.lower() in header else pos
    records = []
    for row in table_rows(body):
        records.append({col: (row[i] if i < len(row) else "") for col, i in index.items()})
    return records


def table_rows(body: str) -> List[List[str]]:
    """Data rows of the first markdown table in body (header and separator dropped)."""
    rows: List[List[str]] = []
    seen_header = False
    for line in body.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            if rows or seen_header:
                break
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if not seen_header:
            seen_header = True
            continue
        if all(re.fullmatch(r":?-+:?", c) for c in cells if c):
            continue
        rows.append(cells)
    return rows


def ids(text: str, prefix: str) -> List[str]:
    """Normalised IDs like BR-01 found in text (BR-1 and BR-01 are the same)."""
    found = set()
    for m in re.finditer(r"\b{}-(\d+)\b".format(prefix), strip_comments(text)):
        found.add("{}-{:02d}".format(prefix, int(m.group(1))))
    return sorted(found)


def percent(body: str, label: str) -> Optional[float]:
    """Number in 'Label: 95%', also accepting '≥ 95%', '>= 95%', 'at least 95%', 'minimum 95%'."""
    m = re.search(r"{}:\s*(?:≥|>=|>|at least|min(?:imum)?\.?)?\s*([\d.]+)\s*%".format(label), body, re.I)
    return float(m.group(1)) if m else None


def tech_stack(tier: Optional[int]) -> List[str]:
    """Technologies allowed for this tier, lower-cased."""
    path = REFERENCE / "tech-stack.md"
    allowed = []
    for body in sections(path.read_text(encoding="utf-8"), level=1).values():
        for row in table_rows(body):
            if len(row) < 3:
                continue
            tech, status = row[1], row[2].lower()
            if not tech or tech.upper() == "TODO" or status == "retiring":
                continue
            if status == "pilot" and tier != 1:
                continue
            allowed.append(tech.lower())
    return allowed


def golden_set_size(path: Path) -> int:
    with open(path, encoding="utf-8", newline="") as f:
        return sum(1 for r in csv.DictReader(f)
                   if (r.get("input") or "").strip() and (r.get("expected_output") or "").strip())


def open_blockers(reviews_dir: Path, skip: Optional[str] = None) -> List[str]:
    """Rows with severity 'blocker' in any review table that are not marked RESOLVED."""
    found = []
    if not reviews_dir.exists():
        return found
    for f in sorted(reviews_dir.glob("*.md")):
        if skip and f.name == skip:
            continue
        for line in strip_comments(f.read_text(encoding="utf-8")).splitlines():
            s = line.strip()
            if not s.startswith("|"):
                continue
            cells = [c.strip() for c in s.strip("|").split("|")]
            if cells and cells[0].strip("* ").lower() == "blocker" and "RESOLVED" not in s:
                found.append("{}: {}".format(f.name, " | ".join(cells[1:3])))
    return found


def _norm(q: str) -> str:
    q = re.sub(r"\(owner:[^)]*\)", "", q, flags=re.I)
    q = re.sub(r"\bOQ-\d+\b", "", q)
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", q.lower())).strip()


def _words(q: str) -> set:
    stop = {"the", "a", "an", "of", "to", "for", "and", "or", "if", "is", "are", "on", "in", "by", "be", "eg", "e", "g", "so"}
    return {w for w in _norm(q).split() if w not in stop}


def _same_question(item: str, listed: str) -> bool:
    """Same question despite small wording changes: containment or 70% word overlap."""
    a, b = _norm(item), _norm(listed)
    if not a or not b:
        return False
    if a in b or b in a:
        return True
    wa, wb = _words(item), _words(listed)
    return bool(wa and wb) and len(wa & wb) / min(len(wa), len(wb)) >= 0.7


def unlisted_open_items(texts: List[Tuple[str, str]], state: dict) -> List[str]:
    """OPEN: items in artifacts that are not in usecase.yaml open_questions with an owner.

    An item matches when it cites a listed question's ID (e.g. "OPEN: OQ-03 ...")
    or when its wording is close enough to a listed question.
    """
    owned = [q for q in state.get("open_questions", []) if q.get("owner")]
    ids = {q["id"] for q in owned if q.get("id")}
    problems = []
    for name, text in texts:
        for m in re.finditer(r"OPEN:\s*(.+)", strip_comments(text)):
            item = m.group(1)
            if set(re.findall(r"\bOQ-\d+\b", item)) & ids:
                continue
            if not any(_same_question(item, q.get("question", "")) for q in owned):
                problems.append("{}: 'OPEN: {}' is not in open_questions with an owner".format(name, item.strip()))
    return problems
