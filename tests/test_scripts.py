"""Tests for the factory scripts. Run: python3 -m unittest discover tests"""

import contextlib
import io
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import build_handoff  # noqa: E402
import check_gate  # noqa: E402
import factory_lib as fl  # noqa: E402
import new_usecase  # noqa: E402
import portfolio_status  # noqa: E402

FIXTURES = ROOT / "tests" / "fixtures" / "usecases"

TECH_STACK = """# Approved internal tech stack

| Layer | Technology | Status | Notes / constraints |
|---|---|---|---|
| Channel / UI | Internal web portal | approved | |
| Orchestration | Workflow engine | approved | |
| Models | Claude Sonnet | approved | |
| HITL workflow | Approval service | approved | |
| Guardrails | Guardrail layer | approved | |
| Identity and access | Entra ID | approved | |
| Observability and evaluation | Eval harness | approved | |
| Hosting and environments | Private cloud | approved | |
| Models | Old model | retiring | |
"""

NEEDED = {
    "Channel / UI": "Internal web portal", "Orchestration": "Workflow engine", "Models": "Claude Sonnet",
    "HITL workflow": "Approval service", "Guardrails": "Guardrail layer", "Identity and access": "Entra ID",
    "Observability and evaluation": "Eval harness", "Hosting and environments": "Private cloud",
}


def quiet(fn, *args):
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
        code = fn(*args)
    return code, out.getvalue()


def failures(report):
    return [msg for ok, msg in report.items if not ok]


class Workspace(unittest.TestCase):
    """Copies fixtures into a temp dir and points the reference catalogs at a filled tech stack."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.usecases = self.tmp / "usecases"
        shutil.copytree(FIXTURES, self.usecases)
        ref = self.tmp / "reference"
        ref.mkdir()
        (ref / "tech-stack.md").write_text(TECH_STACK, encoding="utf-8")
        self._ref = fl.REFERENCE
        fl.REFERENCE = ref

    def tearDown(self):
        fl.REFERENCE = self._ref
        shutil.rmtree(self.tmp)

    def uc(self, name="UC-001-invoice-triage"):
        return self.usecases / name

    def set_state(self, folder, **changes):
        state = fl.load_yaml(folder / "usecase.yaml")
        for key, value in changes.items():
            if key in fl.GATES:
                state["gates"][key] = value
            else:
                state[key] = value
        fl.dump_yaml(state, folder / "usecase.yaml")

    def write(self, folder, rel, text):
        path = folder / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def passed(self):
        return {"status": "passed", "date": "2026-10-20", "approver": "Tuncer"}

    def stack_phase(self, folder):
        self.set_state(folder, g1_requirements=self.passed(), pattern="workflow-automation", phase=2)
        rows = []
        for layer in fl.LAYERS:
            if layer in NEEDED:
                rows.append("| {} | needed | {} | reuse | Platform team |".format(layer, NEEDED[layer]))
            else:
                rows.append("| {} | not needed | — | — | — |".format(layer))
        self.write(folder, "02-stack/component-map.md",
                   "# Component map\n\n## Pattern chosen and why\nPattern: workflow-automation\nFixed process.\n"
                   "Runner-up: document-processing — routing needs judgment.\n\n## Layers\n"
                   "| Layer | Needed | Technology | Reuse | Owner |\n|---|---|---|---|---|\n" + "\n".join(rows) +
                   "\n\n## Component diagram\n```mermaid\nflowchart TB\n  Portal --> Engine --> Model\n```\n")
        self.write(folder, "02-stack/tech-decisions.md",
                   "# Tech decisions\n\n## TD-01: Use workflow engine\n\n### Context\nFixed steps.\n\n"
                   "### Options\nEngine or agent.\n\n### Decision\nEngine.\n\n### Consequences\nLess flexible.\n")

    def design_phase(self, folder, golden_rows=100):
        self.stack_phase(folder)
        self.set_state(folder, g2_stack=self.passed(), phase=3)
        self.write(folder, "03-design/solution-architecture.md",
                   "# Arch\n\n## Context\nPortal, engine, ERP.\n\n## Logical view\nThree components.\n\n"
                   "## Agents\n| Agent | Purpose | Spec file |\n|---|---|---|\n| triage-agent | Proposes queue | triage-agent.md |\n\n"
                   "## Data flow\nPDF to engine to model.\n\n## Integration contracts\nERP REST.\n\n"
                   "## Deployment view\nPrivate cloud.\n\n## Environments\ndev, test, prod.\n\n## Error handling\nRetry then queue.\n")
        self.write(folder, "03-design/agents/triage-agent.md",
                   "# Agent spec\n\n## Role\nTriage.\n\n## Goal\nRoute.\n\n## Instructions draft\nYou route invoices.\n\n"
                   "## Tools and scopes\n| Tool | Operations | Scope | Access |\n|---|---|---|---|\n| ERP | read | invoices | read |\n\n"
                   "## Input schema\nInvoice text.\n\n## Output schema\nQueue JSON.\n\n## Autonomy level\nLevel: L1\n\n"
                   "## Escalation\nSupervisor.\n\n## Fallback\nManual queue.\n")
        self.write(folder, "03-design/hitl-design.md",
                   "# HITL\n\n## Approval points\nClerk approves queue.\n\n## Queue fields\nSupplier, amount.\n\n"
                   "## Screen layout\nTwo panes.\n\n## SLA\n1 day.\n\n## Reject and timeout handling\nBack to manual.\n\n"
                   "## Override logging\nWho, when, before, after.\n")
        self.write(folder, "03-design/threat-model.md",
                   "# Threats\n\n## Lightweight checklist\n- [x] Classification known\n\n## Assets\nInvoices.\n\n"
                   "## Trust boundaries\nMailbox to engine.\n\n## Data flows\nSee architecture.\n\n"
                   "## Threats\n| ID | Threat | Category | Component | Likelihood | Impact |\n|---|---|---|---|---|---|\n"
                   "| T1 | Prompt injection in PDF | AI | Model | M | M |\n\n"
                   "## Controls\n| Threat ID | Control | Owner |\n|---|---|---|\n| T1 | No write tools | Dev |\n\n"
                   "## Residual risk\nLow.\n")
        self.write(folder, "03-design/backlog.md",
                   "# Backlog\n\n## Epics\nEP-01: Triage\n\n## User stories\n### US-01: Propose queue (EP-01)\n"
                   "As a clerk I want a proposed queue.\nTraces: BR-01, BR-02, AC-01, AC-02\n")
        lines = ["id,input,expected_output,category,difficulty,source"]
        lines += ["{0},invoice {0},queue A,routing,easy,synthetic".format(i) for i in range(golden_rows)]
        self.write(folder, "03-design/eval-golden-set.csv", "\n".join(lines) + "\n")


class SchemaTests(unittest.TestCase):
    def test_fixture_is_valid(self):
        self.assertEqual(fl.validate_state(fl.load_yaml(FIXTURES / "UC-001-invoice-triage" / "usecase.yaml")), [])

    def test_invalid_state_rejected(self):
        state = fl.load_yaml(FIXTURES / "UC-001-invoice-triage" / "usecase.yaml")
        state["risk_tier"] = 7
        state["gates"]["g1_requirements"] = {"status": "passed"}  # no approver / date
        errors = fl.validate_state(state)
        self.assertTrue(any("risk_tier" in e for e in errors))
        self.assertTrue(any("g1_requirements" in e for e in errors))


class GateOneTests(unittest.TestCase):
    def test_passing_fixture(self):
        report = check_gate.run_gate(1, FIXTURES / "UC-001-invoice-triage")
        self.assertTrue(report.passed, failures(report))

    def test_failing_fixture(self):
        report = check_gate.run_gate(1, FIXTURES / "UC-002-hr-letters")
        self.assertFalse(report.passed)
        text = "\n".join(failures(report))
        self.assertIn("empty: Latency", text)
        self.assertIn("Post to ERP queue", text)
        self.assertIn("too high", text)
        self.assertIn("What is the SLA for supervisors?", text)

    def test_cli_exit_codes(self):
        code, _ = quiet(check_gate.main, ["1", "UC-001", "--usecases-dir", str(FIXTURES)])
        self.assertEqual(code, 0)
        code, _ = quiet(check_gate.main, ["1", "UC-002", "--usecases-dir", str(FIXTURES)])
        self.assertEqual(code, 1)

    def test_gate_zero_passes(self):
        report = check_gate.run_gate(0, FIXTURES / "UC-001-invoice-triage")
        self.assertTrue(report.passed, failures(report))


class LaterGateTests(Workspace):
    def test_g2_requires_g1(self):
        report = check_gate.run_gate(2, self.uc())
        self.assertIn("previous gate g1_requirements passed", failures(report))

    def test_g2_passes_with_approved_stack(self):
        self.stack_phase(self.uc())
        report = check_gate.run_gate(2, self.uc())
        self.assertTrue(report.passed, failures(report))

    def test_g2_rejects_unapproved_technology(self):
        self.stack_phase(self.uc())
        path = self.uc() / "02-stack/component-map.md"
        path.write_text(path.read_text().replace("Claude Sonnet", "Old model"))
        report = check_gate.run_gate(2, self.uc())
        self.assertTrue(any("not approved" in f for f in failures(report)), failures(report))

    def test_g3_passes(self):
        self.design_phase(self.uc())
        report = check_gate.run_gate(3, self.uc())
        self.assertTrue(report.passed, failures(report))

    def test_g3_golden_set_and_traceability(self):
        self.design_phase(self.uc(), golden_rows=10)
        path = self.uc() / "03-design/backlog.md"
        path.write_text(path.read_text().replace("BR-02, ", ""))
        text = "\n".join(failures(check_gate.run_gate(3, self.uc())))
        self.assertIn("golden set has 10 cases", text)
        self.assertIn("missing: BR-02", text)

    def test_open_blocker_fails_gate(self):
        self.design_phase(self.uc())
        self.write(self.uc(), "reviews/phase3-security.md",
                   "| severity | location | issue | fix |\n|---|---|---|---|\n| blocker | threat-model.md | No DLP | Add DLP |\n")
        self.assertFalse(check_gate.run_gate(3, self.uc()).passed)
        self.write(self.uc(), "reviews/phase3-security.md",
                   "| severity | location | issue | fix |\n|---|---|---|---|\n| blocker | threat-model.md | No DLP | Add DLP RESOLVED |\n")
        self.assertTrue(check_gate.run_gate(3, self.uc()).passed)

    def test_g4_accuracy_and_uat(self):
        self.design_phase(self.uc())
        self.set_state(self.uc(), g3_design=self.passed(), phase=4)
        self.write(self.uc(), "04-testing/test-plan.md",
                   "# Test plan\n\n## Functional tests\nUS-01 covers BR-01 BR-02 AC-01 AC-02.\n\n"
                   "## Integration tests\nERP.\n\n## AI quality evals\nGolden set.\n\n## Red-team\nT1.\n\n"
                   "## UAT\nClerks.\n\n## Performance and cost\n2x volume.\n")
        self.write(self.uc(), "04-testing/eval-results.md", "Accuracy: 93%\n")
        text = "\n".join(failures(check_gate.run_gate(4, self.uc())))
        self.assertIn("eval accuracy 93.0% meets NFR target 95.0%", text)
        self.assertIn("UAT", text)
        self.write(self.uc(), "04-testing/eval-results.md", "Accuracy: 96.5%\nUAT: signed by Dana Lee\n")
        report = check_gate.run_gate(4, self.uc())
        self.assertTrue(report.passed, failures(report))


class NewUsecaseTests(Workspace):
    def test_scaffold(self):
        code, out = quiet(new_usecase.main, ["claims-intake", "--department", "Claims",
                                             "--usecases-dir", str(self.usecases)])
        self.assertEqual(code, 0, out)
        folder = self.usecases / "UC-003-claims-intake"
        for d in fl.PHASE_DIRS:
            self.assertTrue((folder / d).is_dir(), d)
        state = fl.load_yaml(folder / "usecase.yaml")
        self.assertEqual(fl.validate_state(state), [])
        self.assertEqual(state["department"], "Claims")
        self.assertEqual((self.usecases / ".active").read_text().strip(), "UC-003")

    def test_rejects_bad_or_duplicate_slug(self):
        self.assertEqual(quiet(new_usecase.main, ["Bad Slug", "--usecases-dir", str(self.usecases)])[0], 1)
        self.assertEqual(quiet(new_usecase.main, ["invoice-triage", "--usecases-dir", str(self.usecases)])[0], 1)


class HandoffTests(Workspace):
    def test_refuses_before_g3(self):
        code, out = quiet(build_handoff.main, ["UC-001", "--usecases-dir", str(self.usecases)])
        self.assertEqual(code, 1)
        self.assertIn("G3 is not passed", out)

    def test_builds_package(self):
        self.design_phase(self.uc())
        self.set_state(self.uc(), g3_design=self.passed())
        code, out = quiet(build_handoff.main, ["UC-001", "--usecases-dir", str(self.usecases)])
        self.assertEqual(code, 0, out)
        h = self.uc() / "handoff"
        for rel in ["README.md", "CLAUDE.md", "requirements/nfr.md", "architecture/component-map.md",
                    "agents/triage-agent.md", "hitl/hitl-design.md", "security/threat-model.md",
                    "backlog.md", "evals/eval-golden-set.csv"]:
            self.assertTrue((h / rel).exists(), rel)
        self.assertIn("`triage-agent`: L1", (h / "CLAUDE.md").read_text())
        readme = (h / "README.md").read_text()
        self.assertIn("Reduce invoice triage time", readme)
        self.assertNotIn("{{", readme)
        state = fl.load_yaml(self.uc() / "usecase.yaml")
        self.assertEqual(state["status"], "handed_off")
        self.assertEqual(fl.validate_state(state), [])


class StatusTests(Workspace):
    def test_table(self):
        code, out = quiet(portfolio_status.main, ["--usecases-dir", str(self.usecases)])
        self.assertEqual(code, 0)
        self.assertIn("UC-001", out)
        self.assertIn("G1", out)
        self.assertIn("Days in phase", out)


if __name__ == "__main__":
    unittest.main()
