"""Build deterministic downstream exports and a browsable index."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from validate import ROOT, read, validate


def write_json(path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def index(root=ROOT):
    lines = ["# 器件索引", "", "自动生成，请维护 parts 中的源文件。所有首次迁移资料均待复核。", ""]
    for manufacturer in sorted((root / "manufacturers").glob("*.json")):
        info = read(manufacturer)
        lines += [f"## {info['name']}", ""]
        for path in sorted((root / "parts" / info["id"]).glob("*/part.json")):
            part = read(path)
            note = (path.parent / "README.md").relative_to(root).as_posix()
            lines.append(f"- [{part['name']}]({note}) — `{part['product_type']}` / `{part['validation']['status']}`")
        lines.append("")
    (root / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")


def export(output, root=ROOT):
    errors = validate(root)
    if errors:
        raise ValueError("\n".join(errors))
    index(root)
    output.mkdir(parents=True, exist_ok=True)
    paths = sorted((root / "parts").glob("*/*/part.json"))
    parts = [read(path) for path in paths]
    knowledge = []
    for path, part in zip(paths, parts):
        pin = path.parent / "pinout.json"
        knowledge.append({"part": part, "engineering_notes": (path.parent / "README.md").read_text(encoding="utf-8"), "pinout": read(pin) if pin.exists() else None})
    write_json(output / "catalog.json", {"schema_version": "0.1.0", "parts": parts})
    write_json(output / "knowledge.json", {"schema_version": "0.1.0", "entries": knowledge})
    source_paths = []
    for directory in ("parts", "manufacturers", "schemas", "vocabulary", "LICENSES"):
        source_paths.extend(path for path in (root / directory).rglob("*") if path.is_file())
    source_paths.append(root / "LICENSE")
    try:
        commit = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], stderr=subprocess.DEVNULL, text=True).strip()
        dirty = bool(subprocess.check_output(["git", "-C", str(root), "status", "--porcelain"], text=True).strip())
    except subprocess.CalledProcessError:
        commit, dirty = None, True
    manifest = {"schema_version": "0.1.0", "part_count": len(parts), "git_commit": commit, "working_tree_dirty": dirty,
        "source_sha256": {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(source_paths)},
        "export_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (output / "catalog.json", output / "knowledge.json")}}
    write_json(output / "manifest.json", manifest)
    return len(parts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    parser.add_argument("--index-only", action="store_true")
    args = parser.parse_args()
    if args.index_only:
        errors = validate()
        if errors:
            raise SystemExit("\n".join(errors))
        index()
        print("INDEX.md updated")
    else:
        print(f"Exported {export(args.output.resolve())} parts to {args.output.resolve()}")
