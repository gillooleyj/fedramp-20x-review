"""Semantic diff of two FedRAMP Consolidated Rules datasets, plus package schema diffs.

Compares content, not the `updated` arrays: the 2026.11.02.01 changelog records
changes that were made without an `updated` entry (IEC-CSO-IIR, IEC-CSO-OIR,
IEC-CSO-FIR), so `updated` alone misses real changes.

Usage:
  python tools/diff_rules.py OLD.json NEW.json [--md out.md] [--json out.json]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import fr_rules  # noqa: E402

HIGH = {"added", "removed", "force", "class_variants", "applicability", "effective", "overlay", "statement_optional"}
MEDIUM = {"statement", "following_information", "artifacts", "timeframe", "definition", "moved", "affects", "notification"}
# everything else (notes, terms, related, controls, references, examples) is LOW
IGNORED = {"updated"}


def flatten(data: dict) -> dict[str, dict]:
    """ID -> {kind, path, entry, subset_applicability} for FRR (incl. rev5), KSI, FRD."""
    out = {}
    for proc, bucket, subset, rid, entry, info in fr_rules.iter_frr(data, include_rev5=True):
        meta = fr_rules.subset_meta(info, bucket, subset)
        out[rid] = {"kind": "FRR", "path": f"FRR.{proc}.data.{bucket}.{subset}.{rid}", "entry": entry,
                    "applicability": meta.get("applicability", {}), "effective": fr_rules.effective(info),
                    "process_status": info.get("status")}
    for theme, kid, k, tv in fr_rules.iter_ksi(data):
        out[kid] = {"kind": "KSI", "path": f"KSI.{theme}.indicators.{kid}", "entry": k,
                    "theme_status": tv.get("status")}
    for bucket, defs in data["FRD"]["data"].items():
        for did, dv in defs.items():
            out[did] = {"kind": "FRD", "path": f"FRD.data.{bucket}.{did}", "entry": dv}
    return out


def _forces(entry: dict) -> dict:
    if "varies_by_class" in entry:
        return {c: v.get("force") for c, v in entry["varies_by_class"].items()}
    return {"*": entry.get("force")}


def _statements(entry: dict) -> dict:
    if "varies_by_class" in entry:
        return {c: v.get("statement") for c, v in entry["varies_by_class"].items()}
    return {"*": entry.get("statement")}


def entry_changes(old: dict, new: dict) -> list[dict]:
    o, n = old["entry"], new["entry"]
    ch = []
    if old["path"] != new["path"]:
        ch.append({"field": "moved", "old": old["path"], "new": new["path"]})
    if old["kind"] == "FRD":
        for f in ("term", "definition"):
            if o.get(f) != n.get(f):
                ch.append({"field": "definition" if f == "definition" else "term", "old": o.get(f), "new": n.get(f)})
    else:
        ov, nv = set(o.get("varies_by_class", {})), set(n.get("varies_by_class", {}))
        if ov != nv:
            ch.append({"field": "class_variants", "old": sorted(ov), "new": sorted(nv)})
        if old["kind"] == "FRR" and _forces(o) != _forces(n):
            ch.append({"field": "force", "old": _forces(o), "new": _forces(n)})
        so, sn = _statements(o), _statements(n)
        if so != sn:
            opt_o = {c: (s or "").startswith(fr_rules.OPTIONAL_PREFIX) for c, s in so.items()}
            opt_n = {c: (s or "").startswith(fr_rules.OPTIONAL_PREFIX) for c, s in sn.items()}
            if opt_o != opt_n:
                ch.append({"field": "statement_optional", "old": opt_o, "new": opt_n})
            ch.append({"field": "statement", "old": so, "new": sn})
        for f in ("following_information", "artifacts", "affects", "notification", "timeframe_type", "timeframe_num"):
            if fr_rules.canon(o.get(f)) != fr_rules.canon(n.get(f)):
                ch.append({"field": "timeframe" if f.startswith("timeframe") else f, "old": o.get(f), "new": n.get(f)})
        # class-variant subfields other than statement/force
        for c in ov & nv:
            vo = {k: v for k, v in o["varies_by_class"][c].items() if k not in ("statement", "force")}
            vn = {k: v for k, v in n["varies_by_class"][c].items() if k not in ("statement", "force")}
            if fr_rules.canon(vo) != fr_rules.canon(vn):
                ch.append({"field": "following_information", "class": c, "old": vo, "new": vn})
        if old.get("applicability") != new.get("applicability"):
            ch.append({"field": "applicability", "old": old.get("applicability"), "new": new.get("applicability")})
        if old.get("effective") != new.get("effective"):
            ch.append({"field": "effective", "old": old.get("effective"), "new": new.get("effective")})
    handled = {"varies_by_class", "statement", "force", "following_information", "artifacts", "affects",
               "notification", "timeframe_type", "timeframe_num", "term", "definition"} | IGNORED
    for f in sorted(set(o) | set(n)):
        if f in handled:
            continue
        if fr_rules.canon(o.get(f)) != fr_rules.canon(n.get(f)):
            ch.append({"field": f, "old": o.get(f), "new": n.get(f)})
    upd_changed = fr_rules.canon(o.get("updated")) != fr_rules.canon(n.get("updated"))
    for c in ch:
        f = c["field"]
        c["severity"] = "high" if f in HIGH else "medium" if f in MEDIUM else "low"
    if ch and not upd_changed:
        ch.append({"field": "updated_not_recorded", "severity": "low",
                   "note": "Content changed but the entry's `updated` array did not."})
    return ch


def applicability_diff(old_data: dict, new_data: dict) -> dict:
    out = {}
    for c in fr_rules.CLASSES:
        o, n = fr_rules.resolve(old_data, c), fr_rules.resolve(new_data, c)
        oi = {r["id"]: r for r in o["rules"] + o["ksis"]}
        ni = {r["id"]: r for r in n["rules"] + n["ksis"]}
        out[c] = {
            "added": sorted(set(ni) - set(oi)),
            "removed": sorted(set(oi) - set(ni)),
            "force_changed": [
                {"id": i, "old": oi[i].get("force"), "new": ni[i].get("force")}
                for i in sorted(set(oi) & set(ni)) if oi[i].get("force") != ni[i].get("force")
            ],
            "optional_changed": sorted(i for i in set(oi) & set(ni) if oi[i].get("optional") != ni[i].get("optional")),
            "statement_changed": sorted(i for i in set(oi) & set(ni) if oi[i]["statement_sha256"] != ni[i]["statement_sha256"]),
            "counts": {"old": o["counts"], "new": n["counts"]},
            "conflicts_new": [x for x in n["conflicts"] if x not in o["conflicts"]],
        }
    return out


def diff(old_data: dict, new_data: dict) -> dict:
    fo, fn = flatten(old_data), flatten(new_data)
    changes = []
    for i in sorted(set(fo) | set(fn)):
        if i not in fn:
            changes.append({"id": i, "kind": fo[i]["kind"], "path": fo[i]["path"],
                            "changes": [{"field": "removed", "severity": "high"}]})
        elif i not in fo:
            changes.append({"id": i, "kind": fn[i]["kind"], "path": fn[i]["path"],
                            "changes": [{"field": "added", "severity": "high"}]})
        else:
            ch = entry_changes(fo[i], fn[i])
            if i in fr_rules.OVERLAY:  # Class A overlay lists change Class A applicability
                for x in ch:
                    if x["field"] == "following_information":
                        x["field"], x["severity"] = "overlay", "high"
            if ch:
                changes.append({"id": i, "kind": fn[i]["kind"], "path": fn[i]["path"], "changes": ch})
    info_changes = {k: {"old": old_data["info"].get(k), "new": new_data["info"].get(k)}
                    for k in set(old_data["info"]) | set(new_data["info"])
                    if fr_rules.canon(old_data["info"].get(k)) != fr_rules.canon(new_data["info"].get(k))}
    return {
        "old_version": old_data["info"].get("version"),
        "new_version": new_data["info"].get("version"),
        "info_changes": info_changes,
        "applicability": applicability_diff(old_data, new_data),
        "entries": changes,
        "summary": {
            sev: sorted({c["id"] for c in changes for x in c["changes"] if x["severity"] == sev})
            for sev in ("high", "medium", "low")
        },
    }


def _walk_schema(s, path=""):
    """Yield (path, required, enum, type) facts for a JSON Schema."""
    if not isinstance(s, dict):
        return
    yield path, tuple(sorted(s.get("required", []))), tuple(map(str, s.get("enum", []))), str(s.get("type"))
    for k, v in (s.get("properties") or {}).items():
        yield from _walk_schema(v, f"{path}/properties/{k}")
    if isinstance(s.get("items"), dict):
        yield from _walk_schema(s["items"], f"{path}/items")
    for k, v in (s.get("$defs") or {}).items():
        yield from _walk_schema(v, f"{path}/$defs/{k}")


def schema_diff(old: dict, new: dict) -> dict:
    o = {p: (r, e, t) for p, r, e, t in _walk_schema(old)}
    n = {p: (r, e, t) for p, r, e, t in _walk_schema(new)}
    return {
        "old_version": old.get("$schemaVersion"),
        "new_version": new.get("$schemaVersion"),
        "properties_added": sorted(set(n) - set(o)),
        "properties_removed": sorted(set(o) - set(n)),
        "required_changed": sorted(p for p in set(o) & set(n) if o[p][0] != n[p][0]),
        "enum_changed": sorted(p for p in set(o) & set(n) if o[p][1] != n[p][1]),
        "type_changed": sorted(p for p in set(o) & set(n) if o[p][2] != n[p][2]),
    }


def to_markdown(d: dict) -> str:
    lines = [f"# Rules Change Report: {d['old_version']} to {d['new_version']}", ""]
    lines += ["## Applicability by Class", "", "| Class | Rules (old to new) | KSIs (old to new) | Added | Removed | Force changed | Statement changed |",
              "| --- | --- | --- | --- | --- | --- | --- |"]
    for c, a in d["applicability"].items():
        co, cn = a["counts"]["old"], a["counts"]["new"]
        fc = ", ".join(f"{x['id']} ({x['old']} to {x['new']})" for x in a["force_changed"]) or "None"
        lines.append(f"| {c.upper()} | {co['rules']} to {cn['rules']} | {co['ksis']} to {cn['ksis']} | "
                     f"{', '.join(a['added']) or 'None'} | {', '.join(a['removed']) or 'None'} | {fc} | "
                     f"{', '.join(a['statement_changed']) or 'None'} |")
    lines.append("")
    for sev in ("high", "medium", "low"):
        ids = d["summary"][sev]
        lines += [f"## {sev.title()} Severity ({len(ids)})", ""]
        for e in d["entries"]:
            fields = [x for x in e["changes"] if x["severity"] == sev]
            if e["id"] in ids and fields:
                lines.append(f"- `{e['id']}` ({e['kind']}, `{e['path']}`): " + ", ".join(x["field"] for x in fields))
        lines.append("")
    if d["info_changes"]:
        lines += ["## Dataset Info", ""] + [f"- `{k}` changed" for k in sorted(d["info_changes"])] + [""]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("old")
    ap.add_argument("new")
    ap.add_argument("--md")
    ap.add_argument("--json")
    a = ap.parse_args()
    d = diff(fr_rules.load(a.old), fr_rules.load(a.new))
    if a.json:
        Path(a.json).write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n")
    md = to_markdown(d)
    if a.md:
        Path(a.md).write_text(md)
    else:
        print(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
