#!/usr/bin/env python3
"""Local web UI for the AI Solution Factory.

Usage: python3 ui/server.py [--port 8000]
Then open http://localhost:8000

Runs only on 127.0.0.1. Phase commands run through the Claude Code CLI
(`claude -p`) in the repository root, so skills, subagents, hooks and
permissions in .claude/ apply exactly as in a terminal session.
Set FACTORY_CLAUDE_BIN to use a different claude executable.
"""

import argparse
import base64
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "samples"))
import factory_lib as fl  # noqa: E402

UI_DIR = Path(__file__).resolve().parent
CLAUDE_BIN = os.environ.get("FACTORY_CLAUDE_BIN") or shutil.which("claude") or "claude"
DOC_DIRS = ["00-intake", "01-requirements", "02-stack", "03-design", "04-testing", "05-rollout", "reviews", "handoff"]
COMMANDS = {"intake", "discover", "stack", "design", "test-plan", "rollout", "handoff", "gate", "status"}

UI_PROMPT = (
    "You are running behind the AI Solution Factory web UI. The product owner reads your replies in a chat panel "
    "and cannot see or answer permission prompts. When you need input, ask your questions as a short numbered list "
    "in plain text and end your turn; the answers arrive as the next message. Never use the AskUserQuestion tool. "
    "Keep replies concise and use markdown. The active use case is {uc}."
)

RUNS = {}  # use case id -> subprocess.Popen
RUNS_LOCK = threading.Lock()


# ---------- helpers ----------

def usecase_dir(uc_id: str) -> Path:
    if not re.fullmatch(r"UC-\d{3,}", uc_id or ""):
        raise ValueError("bad use case id")
    return fl.find_usecase(uc_id)


def safe_child(base: Path, rel: str) -> Path:
    path = (base / rel).resolve()
    if base.resolve() not in path.parents and path != base.resolve():
        raise ValueError("path outside use case")
    return path


def list_files(folder: Path, subdirs):
    out = []
    for d in subdirs:
        base = folder / d
        if not base.exists():
            continue
        for p in sorted(base.rglob("*")):
            if p.is_file() and not p.name.startswith("."):
                out.append({"path": str(p.relative_to(folder)), "size": p.stat().st_size,
                            "modified": int(p.stat().st_mtime)})
    return out


def summary(folder: Path) -> dict:
    state = fl.load_yaml(folder / "usecase.yaml")
    state["valid"] = not fl.validate_state(state)
    state["folder"] = folder.name
    with RUNS_LOCK:
        proc = RUNS.get(state.get("id"))
        state["running"] = bool(proc and proc.poll() is None)
    return state


def chat_log(folder: Path) -> Path:
    return folder / ".ui-chat.jsonl"


def append_chat(folder: Path, event: dict) -> None:
    event.setdefault("ts", int(time.time()))
    with open(chat_log(folder), "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")


def session_file(folder: Path) -> Path:
    return folder / ".ui-session"


def tool_summary(name: str, data: dict) -> str:
    for key in ("file_path", "command", "pattern", "description", "skill", "path"):
        if data.get(key):
            value = str(data[key]).replace(str(ROOT) + "/", "")
            return "{}: {}".format(name, value[:160])
    return name


def stream_events(proc, folder: Path):
    """Turn claude stream-json lines into UI events, logging them as we go."""
    for raw in proc.stdout:
        raw = raw.strip()
        if not raw:
            continue
        try:
            msg = json.loads(raw)
        except ValueError:
            continue
        kind = msg.get("type")
        if kind == "system" and msg.get("subtype") == "init":
            session_file(folder).write_text(msg.get("session_id", ""), encoding="utf-8")
        elif kind == "system" and msg.get("subtype") == "api_retry" and msg.get("error_status") == 401:
            text = "Claude Code is not signed in. Open a terminal, run `claude`, and use /login. Then try again."
            append_chat(folder, {"kind": "error", "text": text})
            proc.kill()
            yield {"kind": "done", "error": True, "text": text}
            return
        elif kind == "assistant":
            for block in msg.get("message", {}).get("content", []):
                if block.get("type") == "text" and block.get("text", "").strip():
                    ev = {"kind": "assistant", "text": block["text"]}
                    append_chat(folder, ev)
                    yield ev
                elif block.get("type") == "tool_use":
                    ev = {"kind": "tool", "text": tool_summary(block.get("name", "tool"), block.get("input") or {})}
                    append_chat(folder, ev)
                    yield ev
        elif kind == "result":
            ev = {"kind": "done", "error": bool(msg.get("is_error")),
                  "text": msg.get("result", "") if msg.get("is_error") else "",
                  "cost": msg.get("total_cost_usd"), "turns": msg.get("num_turns")}
            if ev["error"]:
                append_chat(folder, {"kind": "error", "text": ev["text"]})
            yield ev


# ---------- HTTP ----------

class Handler(BaseHTTPRequestHandler):
    server_version = "FactoryUI/1.0"

    def log_message(self, fmt, *args):
        sys.stderr.write("[ui] " + fmt % args + "\n")

    def send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def body(self) -> dict:
        n = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(n) or b"{}") if n else {}

    def do_GET(self):
        url = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(url.query).items()}
        try:
            if url.path in ("/", "/index.html"):
                data = (UI_DIR / "index.html").read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
            elif url.path == "/api/usecases":
                rows = [summary(p.parent) for p in sorted(fl.DEFAULT_USECASES.glob("UC-*/usecase.yaml"))]
                active = fl.DEFAULT_USECASES / ".active"
                samples = sorted(p.name for p in (ROOT / "samples" / "requests").iterdir() if p.is_dir())
                self.send_json({"usecases": rows, "samples": samples,
                                "active": active.read_text().strip() if active.exists() else None,
                                "tech_stack_filled": bool(fl.tech_stack(2))})
            elif url.path == "/api/usecase":
                folder = usecase_dir(q.get("id"))
                log = chat_log(folder)
                chat = [json.loads(l) for l in log.read_text(encoding="utf-8").splitlines() if l.strip()] if log.exists() else []
                self.send_json({"state": summary(folder), "documents": list_files(folder, DOC_DIRS),
                                "inputs": list_files(folder, ["inputs"]), "chat": chat})
            elif url.path == "/api/file":
                folder = usecase_dir(q.get("id"))
                path = safe_child(folder, q.get("path", ""))
                self.send_json({"path": q.get("path"), "content": path.read_text(encoding="utf-8", errors="replace")})
            else:
                self.send_json({"error": "not found"}, 404)
        except (ValueError, SystemExit, OSError) as exc:
            self.send_json({"error": str(exc)}, 400)

    def do_POST(self):
        url = urlparse(self.path)
        try:
            data = self.body()
            if url.path == "/api/new":
                self.create(data)
            elif url.path == "/api/sample":
                self.load_sample(data)
            elif url.path == "/api/upload":
                self.upload(data)
            elif url.path == "/api/activate":
                usecase_dir(data.get("id"))
                (fl.DEFAULT_USECASES / ".active").write_text(data["id"] + "\n", encoding="utf-8")
                self.send_json({"ok": True})
            elif url.path == "/api/run":
                self.run_claude(data)
            elif url.path == "/api/stop":
                with RUNS_LOCK:
                    proc = RUNS.get(data.get("id"))
                if proc and proc.poll() is None:
                    proc.terminate()
                self.send_json({"ok": True})
            elif url.path == "/api/clear-chat":
                folder = usecase_dir(data.get("id"))
                for f in (chat_log(folder), session_file(folder)):
                    if f.exists():
                        f.unlink()
                self.send_json({"ok": True})
            else:
                self.send_json({"error": "not found"}, 404)
        except (ValueError, SystemExit, OSError, KeyError) as exc:
            self.send_json({"error": str(exc)}, 400)

    # --- actions ---

    def capture(self, fn, args):
        import contextlib
        import io
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            code = fn(args)
        return code, out.getvalue()

    def create(self, data):
        import new_usecase
        args = [data.get("slug", "").strip()]
        for key, flag in (("name", "--name"), ("department", "--department"), ("sponsor", "--sponsor")):
            if data.get(key, "").strip():
                args += [flag, data[key].strip()]
        for sme in [s.strip() for s in data.get("smes", "").split(",") if s.strip()]:
            args += ["--sme", sme]
        code, out = self.capture(new_usecase.main, args)
        self.send_json({"ok": code == 0, "output": out, "id": (fl.DEFAULT_USECASES / ".active").read_text().strip() if code == 0 else None},
                       200 if code == 0 else 400)

    def load_sample(self, data):
        import load_sample
        code, out = self.capture(load_sample.main, [data.get("name", "")])
        self.send_json({"ok": code == 0, "output": out, "id": (fl.DEFAULT_USECASES / ".active").read_text().strip() if code == 0 else None},
                       200 if code == 0 else 400)

    def upload(self, data):
        folder = usecase_dir(data.get("id"))
        name = re.sub(r"[^A-Za-z0-9._ -]", "_", Path(data.get("name", "")).name).strip()
        if not name or name.startswith("."):
            raise ValueError("bad file name")
        target = folder / "inputs" / name
        if target.exists():
            raise ValueError("{} already exists in inputs/ (department originals are never overwritten)".format(name))
        target.write_bytes(base64.b64decode(data.get("content", "")))
        self.send_json({"ok": True, "path": "inputs/" + name})

    def run_claude(self, data):
        uc = data.get("id")
        folder = usecase_dir(uc)
        command, message = data.get("command"), (data.get("message") or "").strip()
        if command:
            if command not in COMMANDS:
                raise ValueError("unknown command")
            arg = data.get("arg", "")
            if command == "gate" and not re.fullmatch(r"[0-5]", str(arg)):
                raise ValueError("gate needs 0-5")
            prompt = "/{} {}".format(command, " ".join(x for x in [str(arg) if command == "gate" else "", uc] if x)).strip()
            resume = None  # each phase command starts a fresh conversation
        elif message:
            prompt = message
            sf = session_file(folder)
            resume = sf.read_text().strip() if sf.exists() else None
        else:
            raise ValueError("nothing to run")
        with RUNS_LOCK:
            if RUNS.get(uc) and RUNS[uc].poll() is None:
                raise ValueError("Claude is already working on {}. Wait or press Stop.".format(uc))
            (fl.DEFAULT_USECASES / ".active").write_text(uc + "\n", encoding="utf-8")
            cmd = [CLAUDE_BIN, "-p", prompt, "--output-format", "stream-json", "--verbose",
                   "--permission-mode", "acceptEdits", "--disallowedTools", "AskUserQuestion",
                   "--append-system-prompt", UI_PROMPT.format(uc=uc)]
            if resume:
                cmd += ["--resume", resume]
            env = dict(os.environ, CLAUDE_PROJECT_DIR=str(ROOT))
            try:
                proc = subprocess.Popen(cmd, cwd=str(ROOT), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                        stdin=subprocess.DEVNULL, text=True, bufsize=1, env=env)
            except OSError as exc:
                raise ValueError("Could not start Claude Code ({}): {}".format(CLAUDE_BIN, exc))
            RUNS[uc] = proc
        append_chat(folder, {"kind": "user", "text": prompt})

        self.send_response(200)
        self.send_header("Content-Type", "application/x-ndjson")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()

        def emit(ev):
            try:
                self.wfile.write((json.dumps(ev) + "\n").encode("utf-8"))
                self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError):
                pass  # browser went away; keep logging so the chat history is complete

        emit({"kind": "user", "text": prompt})
        finished = False
        for ev in stream_events(proc, folder):
            emit(ev)
            finished = finished or ev["kind"] == "done"
        proc.wait()
        if not finished:
            text = "Claude stopped." if proc.returncode in (-15, 143) else "Claude exited (code {}).".format(proc.returncode)
            append_chat(folder, {"kind": "error", "text": text})
            emit({"kind": "done", "error": True, "text": text})


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port", type=int, default=int(os.environ.get("PORT", 8000)))
    args = ap.parse_args()
    fl.DEFAULT_USECASES.mkdir(exist_ok=True)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    server.daemon_threads = True
    print("AI Solution Factory UI on http://localhost:{}  (claude: {})".format(args.port, CLAUDE_BIN))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
