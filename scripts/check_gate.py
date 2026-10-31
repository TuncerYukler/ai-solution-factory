#!/usr/bin/env python3
"""Mechanical gate check for a use case. Exit code 0 = pass, 1 = fail.

Usage:
  python3 scripts/check_gate.py <gate 0-5> [UC-001]     # default: usecases/.active
  python3 scripts/check_gate.py --validate-only [UC-001 | path/to/usecase.yaml]

Quality is checked separately by the gate-reviewer subagent (see /gate).
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List

sys.path.insert(0, str(Path(__file__).resolve().parent))
import factory_lib as fl  # noqa: E402


class Report:
    def __init__(self) -> None:
        self.items = []  # (ok, message)

    def check(self, ok: bool, message: str) -> bool:
        self.items.append((bool(ok), message))
        return bool(ok)

    def fail(self, message: str) -> None:
        self.check(False, message)

    @property
    def passed(self) -> bool:
        return all(ok for ok, _ in self.items)

    def print(self, title: str) -> None:
        print(title)
        for ok, msg in self.items:
            print("  [{}] {}".format("PASS" if ok else "FAIL", msg))
        print("RESULT: {}".format("PASS" if self.passed else "FAIL"))


class GateChecker:
    def __init__(self, folder: Path, state: dict, report: Report) -> None:
        self.folder = folder
        self.state = state
        self.r = report
        self.tier = state.get("risk_tier")
        self.checked_texts = []  # (name, text) for OPEN: item checks

    # --- helpers ---

    def read(self, key: str):
        rel = fl.ARTIFACTS[key][1]
        path = self.folder / rel
        if not self.r.check(path.exists(), "{} exists".format(rel)):
            return None
        text = path.read_text(encoding="utf-8")
        self.checked_texts.append((rel, text))
        return text

    def headings(self, rel: str, text: str, template: str, required: List[str] = None) -> None:
        missing, empty = fl.empty_sections(text, template, required)
        self.r.check(not missing, "{}: all required headings present{}".format(
            rel, "" if not missing else " (missing: {})".format(", ".join(missing))))
        self.r.check(not empty, "{}: no empty sections{}".format(
            rel, "" if not empty else " (empty: {})".format(", ".join(empty))))
        if self.tier and self.tier > 1 and fl.TIER1_NA in fl.strip_comments(text):
            self.r.fail("{}: '{}' used but use case is tier {}".format(rel, fl.TIER1_NA, self.tier))

    def artifact(self, key: str, required: List[str] = None):
        text = self.read(key)
        if text is not None:
            template, rel = fl.ARTIFACTS[key]
            self.headings(rel, text, template, required)
        return text

    def previous_gate(self, n: int) -> None:
        if n == 0:
            return
        prev = fl.GATES[n - 1]
        self.r.check(self.state["gates"][prev]["status"] == "passed", "previous gate {} passed".format(prev))

    def level_ok(self, level: str) -> bool:
        target = self.state.get("autonomy_target")
        if target not in fl.AUTONOMY_ORDER or level not in fl.AUTONOMY_ORDER:
            return False
        return fl.AUTONOMY_ORDER.index(level) <= fl.AUTONOMY_ORDER.index(target)

    # --- gates ---

    def g0(self) -> None:
        text = self.artifact("intake")
        if text is None:
            return
        s = fl.sections(text)
        for heading in ("Value score", "Feasibility score"):
            m = re.search(r"Score:\s*([1-5])\s*/\s*5", s.get(heading, ""))
            self.r.check(m, "intake.md: {} set (Score: n/5)".format(heading.lower()))
        m = re.search(r"Tier:\s*([123])", s.get("Risk tier rationale", ""))
        self.r.check(m, "intake.md: risk tier set (Tier: n)")
        self.r.check(self.tier in (1, 2, 3), "usecase.yaml: risk_tier set")
        if m and self.tier in (1, 2, 3):
            self.r.check(int(m.group(1)) == self.tier, "intake.md tier matches usecase.yaml risk_tier")
        self.r.check(self.state.get("autonomy_target") in fl.AUTONOMY_ORDER, "usecase.yaml: autonomy_target set")
        self.r.check(self.state.get("data_classification"), "usecase.yaml: data_classification set")
        self.r.check(re.search(r"Recommendation:\s*(go|no-go|park)\b", s.get("Recommendation", ""), re.I),
                     "intake.md: recommendation present (go | no-go | park)")

    def g1(self) -> None:
        canvas = self.artifact("canvas")
        if canvas is not None:
            self.r.check(fl.ids(canvas, "BR"), "usecase-canvas.md: business requirements numbered BR-nn")
        nfr = self.artifact("nfr")
        if nfr is not None:
            self.r.check(fl.ids(nfr, "AC"), "nfr.md: acceptance criteria numbered AC-nn")
            self.r.check(fl.percent(fl.sections(nfr).get("Accuracy", ""), "Target") is not None,
                         "nfr.md: accuracy target set (Target: nn%)")
        process = self.artifact("process")
        if process is None:
            return
        rows = fl.table_records(fl.sections(process).get("To-be steps", ""), ["Step", "Actor", "Autonomy", "HITL action"])
        self.r.check(rows, "process-map.md: to-be steps table has rows")
        bad_actor, bad_level, too_high = [], [], []
        for row in rows:
            step, actor = row["Step"], row["Actor"].strip().lower()
            level = row["Autonomy"].strip().upper()
            m = re.match(r"(L[0-3]|N/A)\b", level)  # allow notes such as "L2 (provisional — see OQ-04)"
            level = m.group(1) if m else level
            if actor not in ("ai", "human", "system"):
                bad_actor.append(step)
            elif actor == "ai":
                if level not in fl.AUTONOMY_ORDER:
                    bad_level.append(step)
                elif not self.level_ok(level):
                    too_high.append("{} ({})".format(step, level))
            elif level not in ("N/A", "-", "—"):
                bad_level.append(step)
        self.r.check(not bad_actor, "process-map.md: every to-be step has actor AI | human | system{}".format(
            "" if not bad_actor else " (fix: {})".format(", ".join(bad_actor))))
        self.r.check(not bad_level, "process-map.md: AI steps have L0-L3, others n/a{}".format(
            "" if not bad_level else " (fix: {})".format(", ".join(bad_level))))
        self.r.check(not too_high, "process-map.md: no step above autonomy_target {}{}".format(
            self.state.get("autonomy_target"), "" if not too_high else " (too high: {})".format(", ".join(too_high))))

    def g2(self) -> None:
        pattern = self.state.get("pattern")
        self.r.check(pattern, "usecase.yaml: pattern set")
        text = self.artifact("components")
        if text is not None:
            s = fl.sections(text)
            if pattern:
                self.r.check(re.search(r"Pattern:\s*`?{}`?".format(re.escape(pattern)),
                                       s.get("Pattern chosen and why", "")),
                             "component-map.md: pattern matches usecase.yaml ({})".format(pattern))
            cols = ["Layer", "Needed", "Technology", "Reuse", "Owner"]
            rows = {r["Layer"]: [r[c] for c in cols] for r in fl.table_records(s.get("Layers", ""), cols) if r["Layer"]}
            missing = [l for l in fl.LAYERS if l not in rows]
            self.r.check(not missing, "component-map.md: all 11 layers listed{}".format(
                "" if not missing else " (missing: {})".format(", ".join(missing))))
            allowed = fl.tech_stack(self.tier)
            self.r.check(allowed, "tech-stack.md has approved technologies (fill the TODO rows)")
            unmarked, unknown, no_reuse = [], [], []
            for layer in fl.LAYERS:
                if layer not in rows:
                    continue
                _, needed, tech, reuse, _ = rows[layer]
                needed = needed.lower()
                if needed not in ("needed", "not needed"):
                    unmarked.append(layer)
                    continue
                if needed == "needed":
                    for t in [t.strip() for t in re.split(r"[,;+]", tech) if t.strip()] or [""]:
                        if t.lower() not in allowed:
                            unknown.append("{}: '{}'".format(layer, t))
                    if reuse.lower() not in ("reuse", "extend", "new"):
                        no_reuse.append(layer)
            self.r.check(not unmarked, "component-map.md: every layer marked needed / not needed{}".format(
                "" if not unmarked else " (fix: {})".format(", ".join(unmarked))))
            self.r.check(not unknown, "component-map.md: every technology is in tech-stack.md{}".format(
                "" if not unknown else " (not approved: {})".format("; ".join(unknown))))
            self.r.check(not no_reuse, "component-map.md: needed layers marked reuse / extend / new{}".format(
                "" if not no_reuse else " (fix: {})".format(", ".join(no_reuse))))
        if self.tier and self.tier > 1:
            self.tech_decisions()

    def tech_decisions(self) -> None:
        text = self.read("decisions")
        if text is None:
            return
        records = {h: b for h, b in fl.sections(text).items() if h.startswith("TD-")}
        self.r.check(records and not any("<title>" in h for h in records),
                     "tech-decisions.md: at least one titled TD record")
        incomplete = []
        for h, body in records.items():
            sub = fl.sections("## x\n" + body, level=3)
            if any(not fl._meaningful_lines(sub.get(k, "")) for k in ("Context", "Options", "Decision", "Consequences")):
                incomplete.append(h.split(":")[0])
        self.r.check(not incomplete, "tech-decisions.md: every record has context, options, decision, consequences{}".format(
            "" if not incomplete else " (incomplete: {})".format(", ".join(incomplete))))

    def g3(self) -> None:
        arch = self.artifact("architecture")
        if arch is not None:
            self.agent_specs(arch)
        self.artifact("hitl")
        self.artifact("threats", ["Lightweight checklist"] if self.tier == 1 else None)
        backlog = self.artifact("backlog")
        golden_rel = fl.ARTIFACTS["golden"][1]
        golden = self.folder / golden_rel
        if self.r.check(golden.exists(), "{} exists".format(golden_rel)):
            minimum = fl.GOLDEN_SET_MINIMUM.get(self.tier, 25)
            size = fl.golden_set_size(golden)
            self.r.check(size >= minimum, "golden set has {} cases (tier {} minimum {})".format(size, self.tier, minimum))
        if backlog is not None:
            self.trace(backlog, "backlog.md")

    def agent_specs(self, arch: str) -> None:
        body = fl.sections(arch).get("Agents", "")
        rows = [r for r in fl.table_rows(body) if r and r[0]]
        if not rows:
            self.r.check(re.search(r"\bNone\b", body), "solution-architecture.md: agents table filled or 'None'")
            return
        for row in rows:
            agent = row[0].strip("` ")
            spec_name = (row[2] if len(row) > 2 and row[2] else agent + ".md").strip("` ")
            rel = "{}/{}".format(fl.AGENTS_DIR, Path(spec_name).name)
            path = self.folder / rel
            if not self.r.check(path.exists(), "agent spec for '{}' exists ({})".format(agent, rel)):
                continue
            text = path.read_text(encoding="utf-8")
            self.checked_texts.append((rel, text))
            self.headings(rel, text, fl.AGENT_TEMPLATE)
            m = re.search(r"Level:\s*(L[0-3])", fl.sections(text).get("Autonomy level", ""))
            self.r.check(m and self.level_ok(m.group(1)),
                         "{}: autonomy level set and within autonomy_target".format(rel))

    def trace(self, text: str, name: str, prefixes=("BR", "AC")) -> None:
        canvas = self.folder / fl.ARTIFACTS["canvas"][1]
        nfr = self.folder / fl.ARTIFACTS["nfr"][1]
        sources = {"BR": canvas, "AC": nfr}
        found = set(fl.ids(text, "BR") + fl.ids(text, "AC"))
        for prefix in prefixes:
            src = sources[prefix]
            wanted = fl.ids(src.read_text(encoding="utf-8"), prefix) if src.exists() else []
            missing = [i for i in wanted if i not in found]
            self.r.check(wanted and not missing, "{}: every {} traced{}".format(
                name, prefix, "" if not missing else " (missing: {})".format(", ".join(missing))))

    def g4(self) -> None:
        plan = self.artifact("testplan")
        if plan is not None:
            self.trace(plan, "test-plan.md")
        rel = "04-testing/eval-results.md"
        path = self.folder / rel
        if not self.r.check(path.exists(), "{} exists".format(rel)):
            return
        results = path.read_text(encoding="utf-8")
        self.checked_texts.append((rel, results))
        actual = fl.percent(results, "Accuracy")
        nfr = self.folder / fl.ARTIFACTS["nfr"][1]
        target = fl.percent(fl.sections(nfr.read_text(encoding="utf-8")).get("Accuracy", ""), "Target") if nfr.exists() else None
        self.r.check(actual is not None and target is not None and actual >= target,
                     "eval accuracy {}% meets NFR target {}%".format(actual, target))
        self.r.check(re.search(r"UAT:\s*signed by\s+\S+", results, re.I), "eval-results.md: 'UAT: signed by <name>'")

    def g5(self) -> None:
        text = self.artifact("rollout")
        if text is not None:
            s = fl.sections(text)
            self.r.check(fl.table_rows(s.get("Stages", "")), "rollout-plan.md: stages listed")
            mon = fl.table_rows(s.get("Monitoring", ""))
            self.r.check(mon and all(len(r) > 1 and r[1] for r in mon), "rollout-plan.md: every monitoring metric has a threshold")
            self.r.check(re.search(r"Owner:\s*\S+", s.get("Ownership", "")), "rollout-plan.md: owner named")
        rel = "05-rollout/pilot-results.md"
        self.r.check((self.folder / rel).exists(), "{} exists".format(rel))

    def common(self, n: int) -> None:
        blockers = fl.open_blockers(self.folder / "reviews", skip="gate-{}.md".format(n))
        self.r.check(not blockers, "no open blockers in reviews/{}".format(
            "" if not blockers else " ({})".format("; ".join(blockers))))
        problems = fl.unlisted_open_items(self.checked_texts, self.state)
        self.r.check(not problems, "every OPEN: item is in open_questions with an owner{}".format(
            "" if not problems else "\n      " + "\n      ".join(problems)))


def run_gate(n: int, folder: Path) -> Report:
    report = Report()
    state = fl.load_yaml(folder / "usecase.yaml")
    errors = fl.validate_state(state)
    report.check(not errors, "usecase.yaml valid against schema" + ("" if not errors else "\n      " + "\n      ".join(errors)))
    if errors:
        return report
    checker = GateChecker(folder, state, report)
    checker.previous_gate(n)
    getattr(checker, "g{}".format(n))()
    checker.common(n)
    return report


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("gate", nargs="?", help="gate number 0-5")
    ap.add_argument("usecase", nargs="?", help="UC-001, slug, or folder (default: usecases/.active)")
    ap.add_argument("--validate-only", action="store_true", help="only validate usecase.yaml")
    ap.add_argument("--usecases-dir", type=Path, default=fl.DEFAULT_USECASES)
    args = ap.parse_args(argv)

    if args.validate_only:
        ref = args.usecase or args.gate
        if ref and ref.endswith(".yaml"):
            path = Path(ref)
        else:
            path = fl.find_usecase(ref, args.usecases_dir) / "usecase.yaml"
        errors = fl.validate_state(fl.load_yaml(path))
        print("\n".join(errors) if errors else "{}: valid".format(path))
        return 1 if errors else 0

    if args.gate not in [str(i) for i in range(6)]:
        ap.error("gate must be 0-5")
    folder = fl.find_usecase(args.usecase, args.usecases_dir)
    report = run_gate(int(args.gate), folder)
    report.print("Gate G{} mechanical check — {}".format(args.gate, folder.name))
    return 0 if report.passed else 1


if __name__ == "__main__":
    sys.exit(main())
