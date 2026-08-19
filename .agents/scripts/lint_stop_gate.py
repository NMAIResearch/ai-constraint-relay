#!/usr/bin/env python3
import json
import os
import subprocess
import sys
from pathlib import Path

def locate_tellscrub() -> str:
    candidates = [
        Path(__file__).resolve().parents[2] / "House style" / "tellscrub.py",
        Path.cwd() / "House style" / "tellscrub.py",
        Path("/var/home/Noel/Desktop/House style/tellscrub.py"),
    ]
    for c in candidates:
        if c.is_file():
            return str(c)
    return ""

def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}

    tellscrub_path = locate_tellscrub()
    if not tellscrub_path:
        print(json.dumps({"decision": "allow"}))
        return

    # Check git status for modified or staged markdown files
    res = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=False
    )

    modified_files = []
    for line in res.stdout.splitlines():
        if line.strip():
            path_str = line[3:].strip()
            if path_str.endswith(".md") and os.path.isfile(path_str):
                modified_files.append(path_str)

    failures = []
    for f in modified_files:
        proc = subprocess.run(
            ["python3", tellscrub_path, f],
            capture_output=True,
            text=True,
            check=False
        )
        if proc.returncode != 0:
            err_msg = proc.stdout.strip() or proc.stderr.strip()
            failures.append(f"{f}:\n{err_msg}")

    if failures:
        output = {
            "decision": "continue",
            "reason": (
                "Automated style check failed. You must fix these violations before finishing:\n\n"
                + "\n\n".join(failures)
            )
        }
    else:
        output = {
            "decision": "allow"
        }

    print(json.dumps(output))

if __name__ == "__main__":
    main()
