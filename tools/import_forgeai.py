"""One-time, lossless migration. Does not import or modify the application."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUFACTURERS = {
    "Espressif": "espressif", "STMicroelectronics": "stmicroelectronics",
    "Texas Instruments": "texas-instruments", "Blue Robotics": "blue-robotics",
    "Sensirion": "sensirion", "Bosch Sensortec": "bosch-sensortec", "ROHM": "rohm",
    "TDK InvenSense": "tdk-invensense", "Semtech": "semtech", "Analog Devices": "analog-devices",
    "DFRobot": "dfrobot", "WIZnet": "wiznet", "Microchip Technology": "microchip",
    "Waveshare": "waveshare", "NXP Semiconductors": "nxp", "OMRON": "omron",
    "Bitcraze": "bitcraze", "TE Connectivity": "te-connectivity", "u-blox": "u-blox",
    "Water Linked": "water-linked",
}


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def product_type(kind):
    if "reference" in kind:
        return "reference_design"
    if "board" in kind:
        return "board"
    if "module" in kind:
        return "module"
    if "microcontroller" in kind or "_ic" in kind or kind == "integrated_sensor":
        return "chip"
    if "sonar" in kind or kind == "doppler_velocity_log":
        return "instrument"
    return "component"


def migrate(source):
    if (ROOT / "parts").exists():
        raise SystemExit("parts already exists; migration refuses to overwrite maintained data")
    seed = source / "data/components.json"
    entries = {item["id"]: (item, None, [seed]) for item in json.loads(seed.read_text())}
    for path in sorted((source / "data/electronics_kb/entries").glob("*.json")):
        for item in json.loads(path.read_text()):
            if item["id"] in entries:
                raise ValueError(f"duplicate JSON id: {item['id']}")
            entries[item["id"]] = (item, None, [path])
    for path in sorted((source / "data/electronics_kb/entries").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        metadata, body = text[4:].split("\n---\n", 1)
        item = json.loads(metadata)
        prior = entries.get(item["id"])
        entries[item["id"]] = (item, body, ([seed, path] if prior else [path]))
    pins_file = source / "data/board_pins.json"
    pins = json.loads(pins_file.read_text())
    sources_file = source / "data/sources.json"
    sources = {item["id"]: item for item in json.loads(sources_file.read_text())}
    manufacturers = {}
    report = []
    for old_id, (item, body, source_files) in sorted(entries.items()):
        label = item["manufacturer"]
        name = label.split("/")[0]
        manufacturer_id = MANUFACTURERS.get(name, re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-"))
        manufacturers.setdefault(manufacturer_id, {"id": manufacturer_id, "name": name, "aliases": set()})["aliases"].add(label)
        part_id = f"{manufacturer_id}/{old_id}"
        kind = item.get("kind", "")
        specs = {}
        if item.get("supply_v"):
            specs["supply_voltage"] = {**item["supply_v"], "unit": "V", "basis": "legacy_unspecified", "port": None}
        for field, unit, basis in [
            ("planning_active_current_ma", "mA", "planning_estimate"),
            ("planning_sleep_current_ua", "uA", "planning_estimate"),
            ("measured_board_sleep_current_ua", "uA", "measured"),
            ("planning_active_power_w", "W", "planning_estimate"),
            ("logic_voltage_v", "V", "legacy_unspecified")]:
            if field in item:
                specs[field] = {"value": item[field], "unit": unit, "basis": basis, "conditions": None}
        unresolved = ["迁移资料尚未逐字段核对来源及章节", "精确订货号及硬件版本待核对", "供电端口、工作范围与极限值语义待核对", "接口与可用引脚资源待核对"]
        if "/reference" in label:
            unresolved.append("只明确参考芯片厂家，具体模块/载板制造商未知")
        if not kind:
            unresolved.append("旧条目缺少产品类型，暂归 component")
        if item.get("integration_review_required"):
            unresolved.append("旧库标注需要载板集成复核")
        if "unit_price_cny" in item:
            unresolved.append("历史价格无采集时间，仅保留快照，不作为采购报价")
        part_sources = [{"id": "primary", **item["source"]}]
        pinout = None
        if old_id in pins:
            pin = pins[old_id]
            pin_source = sources[pin["source_id"]]
            part_sources.append({"id": "pinout", **{k: pin_source[k] for k in ("title", "url", "authority")}, "section": pin["source_section"]})
            pinout = {"part_id": part_id, "coverage": "partial_gpio_extract", "validation_status": "needs_review", "source_id": "pinout", "legacy": pin}
            source_files += [pins_file, sources_file]
            unresolved.append("引脚为历史部分 GPIO 摘录，不是完整引脚表")
        part = {
            "schema_version": "0.1.0", "id": part_id, "legacy_ids": [old_id], "name": item["name"],
            "manufacturer_id": manufacturer_id,
            "manufacturer_role": "reference_chip_vendor" if "/reference" in label else "product_manufacturer",
            "mpn": None, "hardware_revision": None,
            "category": item["category"], "product_type": product_type(kind),
            "capabilities": item["capabilities"], "interfaces": item["interfaces"],
            "specifications": specs, "sources": part_sources,
            "evidence": [{"field": f"/specifications/{key}", "source_id": "primary", "binding": "inherited_unreviewed", "locator": None} for key in specs],
            "relations": [], "validation": {"status": "needs_review", "reviews": [], "tests": []},
            "unresolved": unresolved,
            "provenance": {"origin": "ForgeAI local knowledge migration", "origin_id": old_id,
                "source_files": [str(p.relative_to(source)) for p in source_files],
                "source_hashes": {str(p.relative_to(source)): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_files},
                "license": "BSD-3-Clause", "copyright": "2026 landuochong"},
            "legacy": item,
        }
        folder = ROOT / "parts" / manufacturer_id / old_id
        dump(folder / "part.json", part)
        if pinout:
            dump(folder / "pinout.json", pinout)
        # Preserve every original paragraph; clearly distinguish migrated narrative from reviewed facts.
        narrative = body.strip() if body else f"# {item['name']}\n\n该条目来自旧版结构化器件库，工程说明待补充。"
        warning = "> 迁移待复核：以下为历史工程笔记，包含旧参数及验证措辞，不表示新仓库已审核通过。结构化参数以 part.json 为准。\n\n"
        (folder / "README.md").write_text(warning + narrative + "\n", encoding="utf-8")
        report.append((part_id, len(unresolved)))
    orphan_pins = sorted(set(pins) - set(entries))
    if orphan_pins:
        raise ValueError(f"pinout without component: {orphan_pins}")
    for manufacturer_id, value in manufacturers.items():
        value["aliases"] = sorted(value["aliases"])
        dump(ROOT / "manufacturers" / f"{manufacturer_id}.json", value)
    taxonomy = json.loads((source / "data/electronics_kb/taxonomy.json").read_text())
    taxonomy["schema_version"] = "0.1.0"
    taxonomy["capability_groups"]["imported"] = sorted({c for item, _, _ in entries.values() for c in item["capabilities"]} - {c for group in taxonomy["capability_groups"].values() for c in group})
    taxonomy["interfaces"] = sorted(set(taxonomy["interfaces"]) | {i for item, _, _ in entries.values() for i in item["interfaces"]})
    dump(ROOT / "vocabulary/taxonomy.json", taxonomy)
    (ROOT / "LICENSES").mkdir(exist_ok=True)
    (ROOT / "LICENSES/BSD-3-Clause.txt").write_text((source / "LICENSE").read_text(), encoding="utf-8")
    counts = Counter(item["category"] for item, _, _ in entries.values())
    lines = ["# 首次迁移报告", "", f"迁移 {len(entries)} 个器件条目、{len(pins)} 份部分 GPIO 引脚资料、{len(manufacturers)} 个厂家命名空间。", "", "不改动原项目数据，不导入客户工程、数据库、审计记录、缓存、密钥或原厂附件。", "", "全部条目为 needs_review，历史 verification 保留在 legacy。尚未建立未经证实的芯片/模组关系。", "", "## 分类数量", ""]
    lines += [f"- {category}: {count}" for category, count in sorted(counts.items())]
    lines += ["", "## 待复核范围", "", "全量参数出处、精确订货号、硬件版本、供电语义及接口资源需审核。参考模块的实际载板厂家仍可能未知。价格与估算电流仅为历史值。", "", "## 条目清单", ""]
    lines += [f"- `{part_id}`：{count} 项待复核" for part_id, count in report]
    (ROOT / "docs/migration-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Migrated {len(entries)} parts, {len(pins)} pinouts, {len(manufacturers)} manufacturers")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="ForgeAI repository path")
    migrate(parser.parse_args().source.resolve())
