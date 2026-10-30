#!/usr/bin/env python3
"""Load a sample request so you can test the factory end to end.

Usage: python3 samples/load_sample.py <it-policy-assistant | invoice-triage>

- Copies the sample tech-stack.md and component-library.md into framework/reference/,
  but only while those files still contain only TODO rows (your real data is never overwritten).
- Scaffolds the use case with scripts/new_usecase.py and copies the sample inputs/ into it.
"""

import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "scripts"))
import factory_lib as fl  # noqa: E402
import new_usecase  # noqa: E402


def is_placeholder(path: Path) -> bool:
    rows = [r for b in fl.sections(path.read_text(encoding="utf-8"), level=1).values() for r in fl.table_rows(b)]
    return all(r[0].upper() == "TODO" or (len(r) > 1 and r[1].upper() == "TODO") for r in rows)


def main(argv) -> int:
    choices = sorted(p.name for p in (HERE / "requests").iterdir() if p.is_dir())
    if len(argv) != 1 or argv[0] not in choices:
        print("Usage: python3 samples/load_sample.py <{}>".format(" | ".join(choices)))
        return 1
    sample = HERE / "requests" / argv[0]

    for name in ("tech-stack.md", "component-library.md"):
        target = fl.REFERENCE / name
        if is_placeholder(target):
            shutil.copy2(HERE / "framework" / name, target)
            print("Copied sample {} into framework/reference/".format(name))
        else:
            print("Kept your existing framework/reference/{} (it has real rows)".format(name))

    meta = fl.load_yaml(sample / "sample.yaml")
    args = [meta["slug"], "--name", meta["name"], "--department", meta["department"], "--sponsor", meta["sponsor"]]
    for sme in meta.get("smes", []):
        args += ["--sme", sme]
    if new_usecase.main(args) != 0:
        return 1
    folder = fl.find_usecase(meta["slug"])
    shutil.copytree(sample / "inputs", folder / "inputs", dirs_exist_ok=True)
    print("Copied sample inputs into {}/inputs/".format(folder.name))
    print("\nNow open Claude Code in this folder and run /intake.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
