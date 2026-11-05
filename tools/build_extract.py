"""Build data/rules-extract.json: the 20x Program applicability set for Classes A, B, and C.

Usage: python tools/build_extract.py [--rules vendor/rules/fedramp-consolidated-rules.json]
Validates the dataset against its official schema first, then validates the
extract against data/rules-extract.schema.json. Exits non-zero on any failure.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

import jsonschema

sys.path.insert(0, str(Path(__file__).parent))
import fr_rules  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def build(rules_path: Path, schema_path: Path, lock: dict | None = None) -> dict:
    data = fr_rules.load(rules_path)
    schema = fr_rules.load(schema_path)
    errors = list(jsonschema.Draft202012Validator(schema).iter_errors(data))
    if errors:
        raise SystemExit(f"Rules dataset failed schema validation: {len(errors)} errors; first: {errors[0].message}")
    raw = rules_path.read_bytes()
    src = {
        "dataset": "FedRAMP Consolidated Rules for 2026",
        "version": data["info"]["version"],
        "last_updated": data["info"]["last_updated"],
        "sha256": __import__("hashlib").sha256(raw).hexdigest(),
        "schema_validated": True,
        "commit": (lock or {}).get("sources", {}).get("rules", {}).get("commit"),
    }
    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "source": src,
        "profile": {"type": fr_rules.TYPE, "path": fr_rules.PATH},
        "default_artifacts": data["info"].get("default_artifacts", {}),
        "classes": {c: fr_rules.resolve(data, c) for c in fr_rules.CLASSES},
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rules", default=str(ROOT / "vendor/rules/fedramp-consolidated-rules.json"))
    ap.add_argument("--schema", default=str(ROOT / "vendor/rules/fedramp-consolidated-rules.schema.json"))
    ap.add_argument("--out", default=str(ROOT / "data/rules-extract.json"))
    args = ap.parse_args()
    lock_path = ROOT / "sources.lock.json"
    lock = json.loads(lock_path.read_text()) if lock_path.exists() else None
    extract = build(Path(args.rules), Path(args.schema), lock)
    out_schema = fr_rules.load(ROOT / "data/rules-extract.schema.json")
    jsonschema.Draft202012Validator(out_schema).validate(extract)
    Path(args.out).write_text(json.dumps(extract, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    for c, r in extract["classes"].items():
        print(f"Class {c.upper()}: {r['counts']}")
    print(f"Wrote {args.out} from rules {extract['source']['version']} (schema-valid; extract-valid)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
