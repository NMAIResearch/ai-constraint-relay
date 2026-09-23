"""Exercise the public reproduction command only on disposable bundle copies.

AI-assisted implementation: OpenAI GPT-6, directed by the author.
"""

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

BUNDLE = Path(__file__).resolve().parent


class ReproductionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="relay-reproduction-test-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.bundle = self.base / "bundle"
        self.bundle.mkdir()
        for source in BUNDLE.iterdir():
            if source.is_file() and not source.is_symlink():
                shutil.copyfile(source, self.bundle / source.name)

    def call(self, *args):
        return subprocess.run([sys.executable, "-B", str(self.bundle / "reproduce.py"), *args],
                              capture_output=True, text=True, timeout=15, check=False)

    def data_change(self, change):
        path = self.bundle / "QUANTITATIVE_INPUTS.json"
        data = json.loads(path.read_text())
        change(data)
        path.write_text(json.dumps(data))

    def value_change(self, identity, value):
        self.data_change(lambda data: next(r for r in data["quantities"] if r["id"] == identity).update(value=value))

    def assert_failed(self, result, text):
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(text, result.stderr)

    def test_clean_check(self):
        result = self.call("--check")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_default_is_read_only_check(self):
        result = self.call()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["mode"], "check")

    def test_follow_up_missing_source(self):
        path = self.bundle / "FOLLOWUPS.json"
        data = json.loads(path.read_text())
        data["row_provenance"][0]["source_ids"] = ["UNKNOWN"]
        path.write_text(json.dumps(data))
        self.assert_failed(self.call("--check"), "Unknown or empty follow-up source")

    def test_generation_matches_shipped_outputs(self):
        output = self.base / "generated"
        result = self.call("--output-dir", str(output))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(list(output.iterdir())), 4)
        for path in output.iterdir():
            self.assertEqual(path.read_bytes(), (self.bundle / path.name).read_bytes())

    def test_changed_amount_drives_paper_and_stale_check(self):
        self.value_change("C021", "106")
        self.assert_failed(self.call("--check"), "different outputs")
        output = self.base / "changed"
        result = self.call("--output-dir", str(output))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("conditional USD106B guarantee cap", (output / "PAPER_v7_1.md").read_text())
        self.assertIn("C021,106,billion USD", (output / "QUANTITIES.csv").read_text())

    def test_calculation_changes_from_inputs(self):
        self.value_change("C_GE_OPEN_RES", "57")
        self.value_change("C_GE_DERIVED_RESIDUAL", "2")
        output = self.base / "changed"
        result = self.call("--output-dir", str(output))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("2GW unreconciled residual", (output / "PAPER_v7_1.md").read_text())
        results = json.loads((output / "RESULTS.json").read_text())
        self.assertEqual(results["calculations"][0]["value"], "2")

    def test_residual_mismatch(self):
        self.value_change("C_GE_OPEN_RES", "57")
        self.assert_failed(self.call("--check"), "residual differs")

    def test_backlog_mismatch(self):
        self.value_change("C094", "4")
        self.assert_failed(self.call("--check"), "backlog does not reconcile")

    def test_duplicate_source_value_mismatch(self):
        self.value_change("C091", "19")
        self.assert_failed(self.call("--check"), "Repeated source quantity differs")

    def test_wrong_unit(self):
        self.data_change(lambda data: next(r for r in data["quantities"] if r["id"] == "C095").update(unit="MW"))
        self.assert_failed(self.call("--check"), "requires GW")

    def test_missing_source(self):
        self.data_change(lambda data: data["quantities"][0].update(source_ids=["MISSING"], locators={"MISSING": "page 1"}))
        self.assert_failed(self.call("--check"), "Unknown source ID")

    def test_duplicate_record(self):
        self.data_change(lambda data: data["quantities"].append(data["quantities"][0]))
        self.assert_failed(self.call("--check"), "Duplicate quantity ID")

    def test_invalid_decimal(self):
        for value in ("NaN", "Infinity", True, "1e309"):
            with self.subTest(value=value):
                self.value_change("C021", value)
                self.assert_failed(self.call("--check"), "quantity" if isinstance(value, str) else "decimal strings")

    def test_follow_up_changes_both_outputs(self):
        path = self.bundle / "FOLLOWUPS.json"
        data = json.loads(path.read_text())
        data["rows"][0][2] = "Fixture: replacement observation"
        path.write_text(json.dumps(data))
        self.assert_failed(self.call("--check"), "different outputs")
        output = self.base / "changed"
        result = self.call("--output-dir", str(output))
        self.assertEqual(result.returncode, 0, result.stderr)
        for name in ("PAPER_v7_1.md", "FOLLOWUPS.md"):
            self.assertIn("Fixture: replacement observation", (output / name).read_text())

    def test_missing_input(self):
        (self.bundle / "FOLLOWUPS.json").unlink()
        self.assert_failed(self.call("--check"), "Missing or linked input")

    def test_duplicate_json_key(self):
        (self.bundle / "FOLLOWUPS.json").write_text('{"rows": [], "rows": []}')
        self.assert_failed(self.call("--check"), "Duplicate JSON key")

    def test_unknown_template_token(self):
        path = self.bundle / "PAPER.template.md"
        path.write_text(path.read_text() + "\n{{UNKNOWN}}\n")
        self.assert_failed(self.call("--check"), "Unknown paper token")

    def test_wrong_schema(self):
        self.data_change(lambda data: data.update(schema_version="unknown"))
        self.assert_failed(self.call("--check"), "Unsupported input schema")

    def test_refuses_existing_output_directory(self):
        path = self.base / "occupied"
        path.mkdir()
        sentinel = path / "PAPER_v7_1.md"
        sentinel.write_text("protected")
        self.assert_failed(self.call("--output-dir", str(path)), "refusing overwrite")
        self.assertEqual(sentinel.read_text(), "protected")

    def test_refuses_output_inside_bundle(self):
        self.assert_failed(self.call("--output-dir", str(self.bundle / "new")), "outside this bundle")
        self.assertFalse((self.bundle / "new").exists())

    def test_missing_parent_late_path(self):
        self.assert_failed(self.call("--output-dir", str(self.base / "missing" / "new")), "No such file")
        self.assertFalse((self.base / "missing").exists())

    def test_check_preserves_all_bytes(self):
        def hashes():
            return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in self.bundle.iterdir() if p.is_file()}
        before = hashes()
        self.assertEqual(self.call("--check").returncode, 0)
        self.assertEqual(hashes(), before)

    def test_explain_carries_qualifier_source_and_location(self):
        result = self.call("--explain", "C021")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        evidence = report["evidence"]
        self.assertEqual(evidence["value"], "105")
        self.assertEqual(evidence["unit"], "billion USD")
        self.assertIn("neither paid cash nor expected loss", evidence["qualifier"])
        self.assertEqual(evidence["sources"][0]["id"], "S01")
        self.assertIn("sec.gov/Archives/", evidence["sources"][0]["url"])
        self.assertEqual(evidence["paper_locations"][0]["passage"], "D04")
        self.assertIn("not certified verbatim", evidence["text_origin"])
        self.assertEqual(evidence["source_truth"], "not_assessed")
        self.assertEqual(report["checks"]["output_parity"]["status"], "not_run")

    def test_explain_source_only_and_derived_calculations(self):
        for identity in ("C_GE_OPEN_RES", "C_GE_DERIVED_RESIDUAL", "C096"):
            result = self.call("--explain", identity)
            self.assertEqual(result.returncode, 0, result.stderr)
            evidence = json.loads(result.stdout)["evidence"]
            self.assertTrue(evidence["calculations"])
            if identity == "C_GE_OPEN_RES":
                self.assertTrue(evidence["source_only"])
                self.assertEqual(evidence["paper_locations"], [])

    def test_unknown_explanation_fails(self):
        self.assert_failed(self.call("--explain", "UNKNOWN"), "Unknown quantity ID")

    def test_check_reports_separate_statuses(self):
        result = self.call("--check")
        self.assertEqual(result.returncode, 0, result.stderr)
        checks = json.loads(result.stdout)["checks"]
        for name in ("input_validation", "arithmetic", "output_generation", "output_parity", "package_integrity"):
            self.assertEqual(checks[name]["status"], "pass", name)
        for name in ("source_truth", "interpretation", "pdf_layout"):
            self.assertEqual(checks[name]["status"], "not_assessed", name)

    def test_arithmetic_failure_identifies_record_and_values(self):
        self.value_change("C_GE_OPEN_RES", "57")
        result = self.call("--check")
        self.assertNotEqual(result.returncode, 0)
        checks = json.loads(result.stderr)["checks"]
        self.assertEqual(checks["input_validation"]["status"], "pass")
        self.assertEqual(checks["arithmetic"]["record"], "C_GE_DERIVED_RESIDUAL")
        self.assertEqual(checks["arithmetic"]["expected"], "1")
        self.assertEqual(checks["arithmetic"]["observed"], "2")
        self.assertEqual(checks["output_parity"]["status"], "not_run")

    def test_invalid_value_identifies_record(self):
        self.value_change("C021", "not-a-number")
        result = self.call("--check")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stderr)["checks"]["input_validation"]["record"], "C021")

    def test_manifest_detects_non_generated_file_change(self):
        path = self.bundle / "README.md"
        path.write_text(path.read_text() + "\nFixture change\n")
        result = self.call("--check")
        self.assertNotEqual(result.returncode, 0)
        checks = json.loads(result.stderr)["checks"]
        self.assertEqual(checks["output_parity"]["status"], "pass")
        self.assertEqual(checks["package_integrity"]["status"], "fail")
        self.assertEqual(checks["package_integrity"]["differences"][0]["file"], "README.md")
        self.assert_failed(self.call("--explain", "C021"), "integrity")

    def test_manifest_inventory_cannot_omit_duplicate_or_escape(self):
        path = self.bundle / "REPRODUCTION.json"
        original = json.loads(path.read_text())
        for operation in ("omit", "duplicate", "escape"):
            data = json.loads(json.dumps(original))
            if operation == "omit":
                data["files"].pop()
            elif operation == "duplicate":
                data["files"].append(data["files"][0])
            else:
                data["files"][0]["path"] = "../outside.txt"
            path.write_text(json.dumps(data))
            self.assert_failed(self.call("--check"), "Manifest file inventory differs")

    def test_manifest_required_and_duplicate_keys_rejected(self):
        path = self.bundle / "REPRODUCTION.json"
        path.unlink()
        self.assert_failed(self.call("--check"), "Missing or linked input")
        path.write_text('{"files": [], "files": []}')
        self.assert_failed(self.call("--check"), "Duplicate JSON key")

    def test_linked_output_is_rejected(self):
        path = self.bundle / "RESULTS.json"
        outside = self.base / "same-results.json"
        shutil.copyfile(path, outside)
        path.unlink()
        path.symlink_to(outside)
        self.assert_failed(self.call("--check"), "linked")

    def test_generate_reports_unchecked_manifest(self):
        self.value_change("C021", "106")
        result = self.call("--output-dir", str(self.base / "example"))
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["checks"]["package_integrity"]["status"], "not_run")
        self.assertEqual(report["checks"]["source_truth"]["status"], "not_assessed")

    def test_reuse_example_preserves_bundle_and_runs_from_other_directory(self):
        before = {p.name: p.read_bytes() for p in self.bundle.iterdir() if p.is_file()}
        result = subprocess.run([sys.executable, "-B", str(self.bundle / "reuse_example.py")],
                                capture_output=True, text=True, cwd=self.base, timeout=30, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)["illustrative_change"]["inconsistent_input_rejected"])
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.bundle.iterdir() if p.is_file()})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, default=BUNDLE, help="Read-only source for disposable test copies")
    args, remaining = parser.parse_known_args()
    BUNDLE = args.bundle.resolve()
    unittest.main(argv=[sys.argv[0], *remaining])
