"""Schema and cross-record validation; never claims electrical correctness."""
from __future__ import annotations

import json
from pathlib import Path
import sys

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def pointer(document, field):
    for token in field[1:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        document = document[int(token)] if isinstance(document, list) else document[token]
    return document


def validate(root=ROOT):
    errors = []
    validators = {}
    for kind in ("part", "manufacturer", "pinout"):
        schema = read(root / "schemas" / f"{kind}.schema.json")
        Draft202012Validator.check_schema(schema)
        validators[kind] = Draft202012Validator(schema, format_checker=FormatChecker())

    def check(kind, path, item):
        findings = sorted(validators[kind].iter_errors(item), key=lambda e: str(e.path))
        errors.extend(f"{path.relative_to(root)}: {list(e.path)} {e.message}" for e in findings)
        return not findings

    taxonomy = read(root / "vocabulary/taxonomy.json")
    capabilities = {c for group in taxonomy["capability_groups"].values() for c in group}
    manufacturers = set()
    for path in sorted((root / "manufacturers").glob("*.json")):
        item = read(path)
        if not check("manufacturer", path, item):
            continue
        if item["id"] in manufacturers or path.stem != item["id"]:
            errors.append(f"{path}: duplicate manufacturer or filename mismatch")
        manufacturers.add(item["id"])
    parts = {}
    legacy_ids = set()
    part_paths = sorted((root / "parts").glob("*/*/part.json"))
    if not part_paths:
        errors.append("no component records found")
    for path in part_paths:
        item = read(path)
        if not check("part", path, item):
            continue
        part_id = item["id"]
        prefix = f"{part_id}: "
        if part_id in parts:
            errors.append(prefix + "duplicate ID")
        parts[part_id] = item
        if "/".join(path.parent.relative_to(root / "parts").parts) != part_id:
            errors.append(prefix + "path must match ID")
        if item["manufacturer_id"] not in manufacturers or part_id.split("/")[0] != item["manufacturer_id"]:
            errors.append(prefix + "unknown/mismatched manufacturer")
        for old_id in item.get("legacy_ids", []):
            if old_id in legacy_ids:
                errors.append(prefix + "duplicate legacy ID")
            legacy_ids.add(old_id)
        if item["category"] not in taxonomy["categories"]:
            errors.append(prefix + "unknown category")
        if set(item["capabilities"]) - capabilities:
            errors.append(prefix + "unknown capabilities")
        if set(item["interfaces"]) - set(taxonomy["interfaces"]):
            errors.append(prefix + "unknown interfaces")
        for key, quantity in item["specifications"].items():
            values = [quantity[k] for k in ("min", "typ", "max") if quantity.get(k) is not None]
            if values != sorted(values):
                errors.append(prefix + f"invalid range: {key}")
            if quantity["basis"] == "measured" and quantity.get("value") is not None and not quantity.get("conditions"):
                errors.append(prefix + f"measured value missing conditions: {key}")
        source_ids = [s["id"] for s in item["sources"]]
        if len(source_ids) != len(set(source_ids)):
            errors.append(prefix + "duplicate source ID")
        explicit = set()
        for evidence in item["evidence"]:
            if evidence["source_id"] not in source_ids:
                errors.append(prefix + "evidence references unknown source")
            try:
                pointer(item, evidence["field"])
            except (KeyError, IndexError, ValueError, TypeError):
                errors.append(prefix + f"evidence references missing field: {evidence['field']}")
            if evidence["binding"] == "explicit":
                if not evidence["locator"]:
                    errors.append(prefix + "explicit evidence requires document locator")
                explicit.add(evidence["field"])
        if item["validation"]["status"] == "source_reviewed":
            required = {"/manufacturer_id", "/manufacturer_role", "/mpn", "/hardware_revision", "/product_type", "/capabilities", "/interfaces"}
            required |= {f"/specifications/{key}" for key in item["specifications"]}
            if not item["validation"]["reviews"] or required - explicit:
                errors.append(prefix + "reviewed record lacks reviewer or explicit fact evidence")
            if item["unresolved"]:
                errors.append(prefix + "reviewed record still has unresolved issues")
        if not (path.parent / "README.md").is_file():
            errors.append(prefix + "missing engineering note")
        pin_path = path.parent / "pinout.json"
        if pin_path.exists():
            pinout = read(pin_path)
            if check("pinout", pin_path, pinout):
                if pinout["part_id"] != part_id or pinout["source_id"] not in source_ids:
                    errors.append(prefix + "pinout references wrong part/source")
                pin_names = [p["pin"] for p in pinout["legacy"]["pins"]]
                if len(pin_names) != len(set(pin_names)):
                    errors.append(prefix + "duplicate pin name")
                if pinout["validation_status"] == "source_reviewed" and item["validation"]["status"] != "source_reviewed":
                    errors.append(prefix + "pinout cannot be reviewed while parent record is unreviewed")
    for part_id, item in parts.items():
        for relation in item["relations"]:
            if relation["target"] not in parts or relation["target"] == part_id:
                errors.append(f"{part_id}: invalid relation target {relation['target']}")
    return errors


if __name__ == "__main__":
    try:
        errors = validate()
    except (ValueError, OSError) as exc:
        raise SystemExit(f"Invalid input: {exc}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        raise SystemExit(1)
    print("PASS: schema, IDs, vocabulary, sources, evidence, relations and pinouts")
    print("This is structural validation, not an electrical or source-content review.")
