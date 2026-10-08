from __future__ import annotations

import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from validate import validate, read
from export import export


class KnowledgeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repository"
        for name in ("parts", "manufacturers", "schemas", "vocabulary", "LICENSES"):
            shutil.copytree(ROOT / name, self.root / name)
        shutil.copyfile(ROOT / "LICENSE", self.root / "LICENSE")
        self.path = sorted((self.root / "parts").glob("*/*/part.json"))[0]

    def mutate(self, fn):
        part = read(self.path)
        fn(part)
        self.path.write_text(json.dumps(part), encoding="utf-8")

    def test_current_catalog(self):
        self.assertEqual(validate(self.root), [])

    def test_unknown_manufacturer(self):
        self.mutate(lambda p: p.update(manufacturer_id="missing"))
        self.assertTrue(any("manufacturer" in error for error in validate(self.root)))

    def test_range(self):
        self.mutate(lambda p: p["specifications"].update(bad={"unit": "V", "basis": "typical", "min": 5, "max": 3}))
        self.assertTrue(any("invalid range" in error for error in validate(self.root)))

    def test_missing_evidence_source(self):
        self.mutate(lambda p: p["evidence"].append({"field": "/name", "source_id": "missing", "binding": "explicit", "locator": "p1"}))
        self.assertTrue(any("unknown source" in error for error in validate(self.root)))

    def test_missing_evidence_field(self):
        self.mutate(lambda p: p["evidence"].append({"field": "/nonexistent", "source_id": "primary", "binding": "explicit", "locator": "p1"}))
        self.assertTrue(any("missing field" in error for error in validate(self.root)))

    def test_false_review(self):
        self.mutate(lambda p: p["validation"].update(status="source_reviewed"))
        self.assertTrue(any("reviewed record" in error for error in validate(self.root)))

    def test_relation(self):
        self.mutate(lambda p: p["relations"].append({"type": "uses_chip", "target": "missing/part"}))
        self.assertTrue(any("relation target" in error for error in validate(self.root)))

    def test_unknown_capability(self):
        self.mutate(lambda p: p["capabilities"].append("imaginary-capability"))
        self.assertTrue(any("unknown capabilities" in error for error in validate(self.root)))

    def test_legacy_snapshot_identity(self):
        paths = sorted((self.root / "parts").glob("*/*/part.json"))
        self.assertGreater(len(paths), 0)
        for path in paths:
            part = read(path)
            if "legacy" in part:
                self.assertIn(part["legacy"]["id"], part["legacy_ids"])
                self.assertEqual(part["provenance"]["origin_id"], part["legacy"]["id"])

    def test_pinout_source(self):
        path = sorted((self.root / "parts").glob("*/*/pinout.json"))[0]
        pin = read(path)
        pin["source_id"] = "missing"
        path.write_text(json.dumps(pin), encoding="utf-8")
        self.assertTrue(any("wrong part/source" in error for error in validate(self.root)))

    def test_duplicate_legacy_id(self):
        paths = sorted((self.root / "parts").glob("*/*/part.json"))
        first = read(paths[0])
        second = read(paths[1])
        second["legacy_ids"] = first["legacy_ids"]
        paths[1].write_text(json.dumps(second), encoding="utf-8")
        self.assertTrue(any("duplicate legacy" in error for error in validate(self.root)))

    def test_export_deterministic_and_includes_notes(self):
        output = Path(self.temp.name) / "export"
        count = export(output, self.root)
        first = {p.name: p.read_bytes() for p in output.glob("*.json")}
        self.assertGreater(count, 0)
        self.assertEqual(len(read(output / "knowledge.json")["entries"]), count)
        self.assertTrue(read(output / "knowledge.json")["entries"][0]["engineering_notes"])
        export(output, self.root)
        self.assertEqual(first, {p.name: p.read_bytes() for p in output.glob("*.json")})


if __name__ == "__main__":
    unittest.main()
