#!/usr/bin/env python3
"""Demonstrate evidence lookup and changed-input checks in a disposable copy.

Illustrative values are not source updates or new research findings.
AI-assisted implementation: OpenAI GPT-6, directed by the author.
"""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def run_example():
    bundle = Path(__file__).resolve().parent

    def call(root, *args):
        result = subprocess.run([sys.executable, "-B", str(root / "reproduce.py"), *args],
                                capture_output=True, text=True, timeout=30, check=False)
        return result.returncode, json.loads(result.stdout if result.returncode == 0 else result.stderr)

    def need(condition, message):
        if not condition:
            raise ValueError(message)

    code, lookup = call(bundle, "--explain", "C021")
    need(code == 0, "Original bundle failed evidence lookup; run reproduce.py --check")
    evidence = lookup["evidence"]
    with tempfile.TemporaryDirectory(prefix="ai-infrastructure-example-") as temporary:
        scratch = Path(temporary) / "bundle"
        scratch.mkdir()
        for path in bundle.iterdir():
            if path.is_file() and not path.is_symlink():
                shutil.copyfile(path, scratch / path.name)
        inputs = scratch / "QUANTITATIVE_INPUTS.json"
        data = json.loads(inputs.read_text(encoding="utf-8"))
        rows = {row["id"]: row for row in data["quantities"]}
        rows["C_GE_OPEN_RES"]["value"] = "57"
        inputs.write_text(json.dumps(data), encoding="utf-8")
        code, rejected = call(scratch, "--check")
        need(code != 0 and rejected["checks"]["arithmetic"]["status"] == "fail",
             "Inconsistent reservation balance was not rejected")
        need(rejected["checks"]["arithmetic"]["observed"] == "2", "Unexpected illustrative residual")
        rows["C_GE_DERIVED_RESIDUAL"]["value"] = "2"
        inputs.write_text(json.dumps(data), encoding="utf-8")
        output = Path(temporary) / "illustrative-output"
        code, generated = call(scratch, "--output-dir", str(output))
        need(code == 0, "Consistent illustrative inputs did not generate")
        result = json.loads((output / "RESULTS.json").read_text(encoding="utf-8"))
        residual = result["calculations"][0]["value"]
        need(residual == "2", "Illustrative value did not reach the calculation output")
        need("2GW unreconciled residual" in (output / "PAPER_v7_1.md").read_text(encoding="utf-8"),
             "Illustrative value did not reach the paper")
    return {"purpose": "Worked reuse example, not new source evidence", "status": "pass",
            "lookup": {key: evidence[key] for key in ("id", "value", "unit", "qualifier", "paper_locations")},
            "source_url": evidence["sources"][0]["url"],
            "illustrative_change": {"opening_GW": "57", "declared_residual_GW": "2",
                                    "inconsistent_input_rejected": True, "generated_residual_GW": residual},
            "original_bundle_modified": False,
            "limits": "Temporary values are illustrative. Frozen excerpts and context are not updated source evidence. All temporary files are removed."}


if __name__ == "__main__":
    try:
        print(json.dumps(run_example(), indent=2))
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        print(json.dumps({"status": "fail", "error": str(error)}), file=sys.stderr)
        sys.exit(1)
