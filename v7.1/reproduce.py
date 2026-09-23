#!/usr/bin/env python3
"""Reproduce the declared paper text, tables and arithmetic from frozen inputs.

Python standard library only. No network, model calls or third-party downloads.
Output parity does not establish the truth of sources or editorial judgements.
AI-assisted implementation: OpenAI GPT-6, directed by the author.
"""

import argparse
import csv
from decimal import Decimal, InvalidOperation
import hashlib
import io
import json
from pathlib import Path
import re
import sys

SCHEMA = "ai-infrastructure-reproduction/1"
OUTPUTS = ("PAPER_v7_1.md", "QUANTITIES.csv", "FOLLOWUPS.md", "RESULTS.json")
INPUTS = ("QUANTITATIVE_INPUTS.json", "FOLLOWUPS.json", "PAPER.template.md", "SOURCE_CATALOGUE.json")
PUBLIC_FILES = OUTPUTS + INPUTS + ("PAPER_v7_1.pdf", "README.md", "reproduce.py", "test_reproduce.py", "reuse_example.py")
WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 9: "nine"}
SOURCE_ONLY = {"C_GE_OPEN_RES", "C_GE_NEW_RES", "C_GE_CONV_RES", "C_GE_CLOSE_RES"}
TOKEN = re.compile(r"\{\{([A-Z][A-Z0-9_]*)(?::(word|comma))?\}\}")


class CheckError(ValueError):
    """A machine-readable failure with an optional record, expected and observed value."""

    def __init__(self, message, **details):
        super().__init__(message)
        self.details = details


def require(condition, message, **details):
    if not condition:
        raise CheckError(message, **details)


def pairs_unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "Duplicate JSON key: " + key)
        result[key] = value
    return result


def read_text(root, name):
    path = root / name
    require(path.is_file() and not path.is_symlink(), "Missing or linked input: " + name)
    return path.read_text(encoding="utf-8")


def read_json(root, name):
    return json.loads(read_text(root, name), object_pairs_hook=pairs_unique)


def numeric(value):
    require(isinstance(value, str), "Quantities must be decimal strings")
    require(bool(re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", value)), "Invalid decimal quantity")
    result = Decimal(value)
    require(result.is_finite(), "Non-finite quantity")
    return result


def decimal_text(value):
    return format(value, "f")


def table_cell(value):
    require(isinstance(value, str) and bool(value.strip()), "Empty table cell")
    require(not any(char in value for char in "|\r\n"), "Unsupported table delimiter")
    return value


def reproduce(root, checks=None):
    checks = {} if checks is None else checks
    checks["input_validation"] = {"status": "running"}
    catalogue = read_json(root, "SOURCE_CATALOGUE.json")
    sources = {}
    for source in catalogue["sources"]:
        identity = source["id"]
        require(identity not in sources, "Duplicate source ID: " + identity)
        require(source["url"].startswith("https://"), "Missing HTTPS source URL")
        sources[identity] = source

    data = read_json(root, "QUANTITATIVE_INPUTS.json")
    require(data["schema_version"] == SCHEMA, "Unsupported input schema")
    require(data["paper_version"] == "v7.1", "Wrong paper version")
    rows, values = {}, {}
    for row in data["quantities"]:
        identity = row["id"]
        require(bool(re.fullmatch(r"C[A-Z0-9_]+", identity)), "Invalid quantity ID")
        require(identity not in rows, "Duplicate quantity ID: " + identity)
        for field in ("unit", "period", "qualifier", "context", "excerpt"):
            require(isinstance(row[field], str) and bool(row[field].strip()), "Missing " + field,
                    record=identity, field=field, expected="non-empty text", observed=row[field])
        require(row["source_ids"] and len(set(row["source_ids"])) == len(row["source_ids"]),
                "Empty or duplicate source references")
        require(set(row["source_ids"]) == set(row["locators"]), "Source/locator mismatch")
        for source_id in row["source_ids"]:
            require(source_id in sources, "Unknown source ID: " + source_id, record=identity, source_id=source_id)
            require(bool(row["locators"][source_id].strip()), "Missing source locator")
        rows[identity] = row
        try:
            values[identity] = numeric(row["value"])
        except ValueError as error:
            raise CheckError(str(error), record=identity, field="value",
                             expected="non-negative decimal string", observed=row["value"]) from error

    def gw(identity):
        require(rows[identity]["unit"] == "GW", "Calculation requires GW: " + identity)
        return values[identity]

    followups = read_json(root, "FOLLOWUPS.json")
    require(followups["schema_version"] == SCHEMA, "Unsupported follow-up schema")
    require(followups["paper_version"] == "v7.1", "Wrong follow-up version")
    header = [table_cell(x) for x in followups["columns"]]
    require(len(header) == 3 and followups["rows"], "Expected non-empty three-column table")
    require(len(followups["row_provenance"]) == len(followups["rows"]), "Follow-up provenance count")
    for provenance in followups["row_provenance"]:
        require(bool(provenance["basis"].strip()), "Missing follow-up basis")
        require(provenance["source_ids"] and all(s in sources for s in provenance["source_ids"]),
                "Unknown or empty follow-up source")
    lines = ["| " + " | ".join(header) + " |", "| --- | --- | --- |"]
    for row in followups["rows"]:
        require(len(row) == 3, "Follow-up column count")
        lines.append("| " + " | ".join(table_cell(x) for x in row) + " |")
    table = "\n".join(lines)

    checks["input_validation"] = {"status": "pass", "scope": "quantity, source and follow-up records"}
    checks["arithmetic"] = {"status": "running"}
    for duplicate, original in (("C091", "C_GE_NEW_RES"), ("C093", "C_GE_CONV_RES")):
        require(gw(duplicate) == gw(original), "Repeated source quantity differs: " + duplicate,
                record=duplicate, expected=decimal_text(gw(original)), observed=decimal_text(gw(duplicate)))
    residual = gw("C_GE_OPEN_RES") + gw("C_GE_NEW_RES") - gw("C_GE_CONV_RES") - gw("C_GE_CLOSE_RES")
    require(residual == gw("C_GE_DERIVED_RESIDUAL"), "Reservation residual differs from declared value",
            record="C_GE_DERIVED_RESIDUAL", expected=decimal_text(gw("C_GE_DERIVED_RESIDUAL")),
            observed=decimal_text(residual))
    backlog = gw("C095") + gw("C092") + gw("C093") - gw("C094")
    require(backlog == gw("C096"), "Firm backlog does not reconcile", record="C096",
            expected=decimal_text(gw("C096")), observed=decimal_text(backlog))
    values["C_GE_DERIVED_RESIDUAL"] = residual
    checks["arithmetic"] = {"status": "pass", "calculations": ["ge_reservation_residual", "ge_firm_backlog"]}
    checks["output_generation"] = {"status": "running"}

    template = read_text(root, "PAPER.template.md")
    require(template.count("{{FOLLOWUPS}}") == 1, "Expected one follow-up slot")
    used = set()

    def substitute(match):
        identity, style = match.groups()
        require(identity in values, "Unknown paper token: " + identity)
        used.add(identity)
        value = values[identity]
        if style == "word":
            require(value == int(value) and int(value) in WORDS, "Unsupported word quantity")
            return WORDS[int(value)]
        return format(value, ",f") if style == "comma" else decimal_text(value)

    paper = TOKEN.sub(substitute, template.replace("{{FOLLOWUPS}}", table))
    require("{{" not in paper and "}}" not in paper, "Unresolved template token")
    require(set(rows) == used | SOURCE_ONLY, "Unrendered or missing registered quantity")
    disclosure = paper.split("## AI assistance, conflicts and limitations\n", 1)[1]
    standalone_table = (
        "# Case follow-ups\n\n"
        "Purpose: reproduce the paper's author-selected follow-up table as a standalone document.\n\n"
        "This work was produced through an AI-assisted workflow directed by the author.\n\n"
        + table + "\n\n## Verification and limits\n\n"
        "The table is generated from FOLLOWUPS.json, whose row_provenance identifies the source records "
        "and boundaries behind each relationship. SOURCE_CATALOGUE.json records their original URLs and "
        "inspection limits. The rows are editorial selections, not calculated risk scores, backtested "
        "predictors or observations that the proposed events occurred. No automated current-source check "
        "or matched project-finance baseline was run.\n\n"
        "## AI assistance, conflicts and limitations\n" + disclosure
    )

    ledger = io.StringIO(newline="")
    writer = csv.writer(ledger, lineterminator="\n")
    writer.writerow(["id", "value", "unit", "period", "qualifier", "excerpt", "context", "sources", "locators"])
    for identity, row in rows.items():
        writer.writerow([identity, decimal_text(values[identity]), row["unit"], row["period"],
                         row["qualifier"], row["excerpt"], row["context"],
                         "; ".join(row["source_ids"]),
                         "; ".join(k + ": " + v for k, v in row["locators"].items())])
    results = {
        "purpose": "Calculated GE Vernova balances and declared reproduction coverage; no causal validation.",
        "schema_version": SCHEMA,
        "paper_version": "v7.1",
        "quantity_records": len(rows),
        "paper_quantity_records": len(used),
        "source_only_records": len(SOURCE_ONLY),
        "follow_up_rows": len(followups["rows"]),
        "calculations": [
            {"id": "ge_reservation_residual", "unit": "GW", "value": decimal_text(residual),
             "inputs": ["C_GE_OPEN_RES", "C_GE_NEW_RES", "C_GE_CONV_RES", "C_GE_CLOSE_RES"],
             "formula": "opening + new - converted - closing", "source_ids": ["S16"],
             "interpretation": "Unreconciled reservation residual; cause unverified, not labelled cancellation."},
            {"id": "ge_firm_backlog", "unit": "GW", "value": decimal_text(backlog),
             "inputs": ["C095", "C092", "C093", "C094"], "reported_closing_id": "C096",
             "formula": "opening + direct_orders + converted - shipments", "source_ids": ["S16"],
             "interpretation": "Reported firm equipment backlog reconciles at the stated precision."}
        ],
        "excluded": ["source retrieval", "complete prose fact checking", "PDF typography",
                     "causal inference", "automated assessment of follow-up events", "historical model experiments"]
    }
    for calculation in results["calculations"]:
        calculation["operands"] = [
            {"id": identity, "value": decimal_text(values[identity]), "unit": rows[identity]["unit"],
             "period": rows[identity]["period"], "description": rows[identity]["excerpt"]}
            for identity in calculation["inputs"]
        ]
    checks["output_generation"] = {"status": "pass"}
    return dict(zip(OUTPUTS, [paper, ledger.getvalue(), standalone_table, json.dumps(results, indent=2) + "\n"]))


def package_integrity(root):
    """Check the fixed public inventory against the local manifest, not authenticity."""
    manifest = read_json(root, "REPRODUCTION.json")
    require(manifest["schema_version"] == "ai-infrastructure-package/1", "Unsupported package schema")
    require(manifest["version"] == "v7.1", "Wrong manifest version")
    require(manifest["inputs"] == list(INPUTS), "Manifest input inventory differs")
    require(manifest["generated_outputs"] == list(OUTPUTS), "Manifest output inventory differs")
    require(manifest["main_document"] == "PAPER_v7_1.pdf" and
            manifest["separately_rendered"] == ["PAPER_v7_1.pdf"], "Manifest PDF identity differs")
    entries = manifest["files"]
    names = [item["path"] for item in entries]
    require(len(names) == len(set(names)) and set(names) == set(PUBLIC_FILES),
            "Manifest file inventory differs", expected=sorted(PUBLIC_FILES), observed=names)
    differences = []
    for entry in entries:
        name = entry["path"]
        path = root / name
        require(type(entry["bytes"]) is int and entry["bytes"] >= 0 and
                isinstance(entry["sha256"], str) and bool(re.fullmatch(r"[0-9a-f]{64}", entry["sha256"])),
                "Invalid manifest size or hash", file=name)
        if path.is_symlink() or not path.is_file():
            differences.append({"file": name, "error": "missing or linked file"})
            continue
        data = path.read_bytes()
        observed = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
        expected = {key: entry[key] for key in ("bytes", "sha256")}
        if observed != expected:
            differences.append({"file": name, "expected": expected, "observed": observed})
    return {"status": "fail" if differences else "pass", "differences": differences,
            "scope": "files listed in the bundled manifest; manifest does not hash itself",
            "authenticity": "not_assessed"}


def explain(root, identity, outputs):
    """Join a frozen quantity to its sources, current calculations and paper locations."""
    data = read_json(root, "QUANTITATIVE_INPUTS.json")
    rows = {row["id"]: row for row in data["quantities"]}
    require(identity in rows, "Unknown quantity ID: " + identity, record=identity)
    row = rows[identity]
    sources = {source["id"]: source for source in read_json(root, "SOURCE_CATALOGUE.json")["sources"]}
    locations = []
    section = "Front matter"
    passage = None
    for number, line in enumerate(read_text(root, "PAPER.template.md").splitlines(), 1):
        if line.startswith("#"):
            section = line.lstrip("# ")
        marker = re.search(r"<!-- (D[0-9]+) -->", line)
        if marker:
            passage = marker.group(1)
        if any(match.group(1) == identity for match in TOKEN.finditer(line)):
            locations.append({"file": "PAPER.template.md", "line": number, "section": section,
                              "passage": passage, "generated_file": "PAPER_v7_1.md"})
    results = json.loads(outputs["RESULTS.json"])
    related = [calc for calc in results["calculations"] if identity in calc["inputs"] or
               identity == calc.get("reported_closing_id") or
               (identity == "C_GE_DERIVED_RESIDUAL" and calc["id"] == "ge_reservation_residual")]
    return {"id": identity, "value": row["value"], "unit": row["unit"], "period": row["period"],
            "qualifier": row["qualifier"], "extraction": "manual, frozen",
            "paper_excerpt": row["excerpt"], "paper_context": row["context"],
            "text_origin": "author-prepared extraction wording; not certified verbatim source quotation",
            "sources": [{**sources[key], "quantity_locator": row["locators"][key]} for key in row["source_ids"]],
            "paper_locations": locations, "source_only": identity in SOURCE_ONLY,
            "calculations": related, "source_truth": "not_assessed", "interpretation": "not_assessed"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Recompute in memory and compare all shipped generated outputs")
    mode.add_argument("--output-dir", type=Path, help="Write outputs to a new directory outside this bundle; never overwrite")
    mode.add_argument("--explain", metavar="QUANTITY_ID", help="Return joined evidence and paper locations as JSON, read-only")
    args = parser.parse_args()
    if args.output_dir is None and args.explain is None:
        args.check = True
    root = Path(__file__).resolve().parent
    checks = {name: {"status": "not_run"} for name in
              ("input_validation", "arithmetic", "output_generation", "output_parity", "package_integrity")}
    checks.update({name: {"status": "not_assessed"} for name in ("source_truth", "interpretation", "pdf_layout")})
    operation = "explain" if args.explain is not None else "check" if args.check else "generate"
    report = {"schema_version": "ai-infrastructure-check/1", "mode": operation, "checks": checks}
    if operation in ("check", "explain"):
        try:
            checks["package_integrity"] = package_integrity(root)
        except (OSError, ValueError, KeyError, TypeError) as error:
            checks["package_integrity"] = {"status": "fail", "error": str(error),
                                           **getattr(error, "details", {})}
    else:
        checks["package_integrity"]["reason"] = "Generation permits edited inputs; use --check to verify the frozen bundle."
    try:
        outputs = reproduce(root, checks)
        if args.check:
            differences = []
            for name, content in outputs.items():
                path = root / name
                if path.is_symlink() or not path.is_file():
                    differences.append({"file": name, "error": "missing or linked output"})
                elif path.read_bytes() != content.encode("utf-8"):
                    differences.append({"file": name, "expected_sha256": hashlib.sha256(content.encode()).hexdigest(),
                                        "observed_sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
            checks["output_parity"] = {"status": "fail" if differences else "pass", "differences": differences}
            if differences:
                report["error"] = "Missing or different outputs: " + ", ".join(item["file"] for item in differences)
        elif args.explain is not None:
            report["evidence"] = explain(root, args.explain, outputs)
            checks["output_parity"]["reason"] = "Lookup recomputes calculations; use --check for included output comparison."
        else:
            target = args.output_dir.resolve()
            require(target != root and root not in target.parents, "Output must be outside this bundle")
            require(not target.exists(), "Output directory already exists; refusing overwrite")
            target.mkdir()
            for name, content in outputs.items():
                with (target / name).open("xb") as handle:
                    handle.write(content.encode("utf-8"))
        report["outputs"] = list(outputs)
    except (OSError, ValueError, KeyError, TypeError, InvalidOperation) as error:
        report["error"] = str(error)
        report["failure"] = getattr(error, "details", {})
        for name, check in checks.items():
            if check["status"] == "running":
                checks[name] = {"status": "fail", "error": str(error), **getattr(error, "details", {})}
    failed = "error" in report or any(check["status"] == "fail" for check in checks.values())
    report["status"] = "fail" if failed else "pass"
    if failed and "error" not in report:
        report["error"] = "Package integrity check failed"
    print(json.dumps(report, indent=2), file=sys.stderr if failed else sys.stdout)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
