"""Read the FedRAMP Consolidated Rules dataset and resolve what applies to a
FedRAMP 20x Program Certification for Class A, B, or C.

Read-only. Never edits the dataset. Follows rules/AGENTS.md:
- shared content lives in the `all` bucket; 20x content in `20x`
- subset applicability comes from info.subsets plus info.20x.subsets
- class variants are used as written; missing variants are never invented
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

TYPE = "20x"
PATH = "Program"
CLASSES = ("a", "b", "c")
OPTIONAL_PREFIX = "**Optional:**"
OVERLAY = {"FRC-CLA-MFR": "MUST", "FRC-CLA-RFR": "SHOULD", "FRC-CLA-OFR": "MAY"}
REF_BASE = "https://www.fedramp.gov/2026/reference"  # class-agnostic pages exist for every ruleset


def load(path: str | Path) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def slug(text: str) -> str:
    text = text.lower().replace("&", "and")
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    return re.sub(r"[\s-]+", "-", text).strip("-")


def subset_meta(proc_info: dict, bucket: str, subset: str) -> dict:
    common = proc_info.get("subsets", {})
    if bucket == "all":
        return common.get(subset, {})
    return {**common, **proc_info.get(bucket, {}).get("subsets", {})}.get(subset, {})


def effective(proc_info: dict) -> dict:
    return proc_info.get("effective") or proc_info.get(TYPE, {}).get("effective") or {}


def iter_frr(data: dict, include_rev5: bool = False):
    """Yield (process, bucket, subset, rule_id, entry, process_info)."""
    for proc, pv in data["FRR"].items():
        for bucket, subsets in pv["data"].items():
            if bucket == "rev5" and not include_rev5:
                continue
            for subset, entries in subsets.items():
                for rid, entry in entries.items():
                    yield proc, bucket, subset, rid, entry, pv["info"]


def iter_ksi(data: dict):
    for theme, tv in data["KSI"].items():
        for kid, k in tv["indicators"].items():
            yield theme, kid, k, tv


def index(data: dict) -> dict:
    """Map every FRR, KSI, and FRD ID to its location."""
    idx = {}
    for proc, bucket, subset, rid, entry, info in iter_frr(data, include_rev5=True):
        idx[rid] = {"kind": "FRR", "process": proc, "bucket": bucket, "subset": subset,
                    "json_path": f"FRR.{proc}.data.{bucket}.{subset}.{rid}"}
    for theme, kid, k, tv in iter_ksi(data):
        idx[kid] = {"kind": "KSI", "theme": theme, "json_path": f"KSI.{theme}.indicators.{kid}"}
    for bucket, defs in data["FRD"]["data"].items():
        for did in defs:
            idx[did] = {"kind": "FRD", "bucket": bucket, "json_path": f"FRD.data.{bucket}.{did}"}
    return idx


def variant(entry: dict, cls: str):
    """Return (statement, force, variant_dict, has_variants). None statement = no variant for class."""
    if "varies_by_class" in entry:
        v = entry["varies_by_class"].get(cls)
        if not v:
            return None, None, None, True
        return v.get("statement"), v.get("force"), v, True
    return entry.get("statement"), entry.get("force"), None, False


def artifacts(entry: dict, v: dict | None) -> list[str]:
    out = []
    for src in (entry.get("artifacts") or {}, (v or {}).get("artifacts") or {}):
        for bucket in ("all", TYPE):
            out.extend(src.get(bucket, []))
    return out


def latest_update(entry: dict) -> dict | None:
    upd = entry.get("updated") or []
    return upd[0] if upd else None


def overlay_ids(data: dict) -> dict[str, str]:
    """Class A overlay: referenced ID -> overlay rule ID (MFR, RFR, OFR)."""
    cla = data["FRR"]["FRC"]["data"]["all"].get("CLA", {})
    out = {}
    for rule_id in OVERLAY:
        for item in cla.get(rule_id, {}).get("following_information", []):
            m = re.search(r":\s*([A-Z]{3}-[A-Z]{3}-[A-Z0-9]{3})\b", item)
            if m:
                out[m.group(1)] = rule_id
    return out


def _frr_record(proc, bucket, subset, rid, entry, info, cls, statement, force, v, basis):
    return {
        "id": rid,
        "kind": "FRR",
        "name": entry.get("name"),
        "process": proc,
        "process_name": info.get("name"),
        "subset": subset,
        "json_path": f"FRR.{proc}.data.{bucket}.{subset}.{rid}" + (f".varies_by_class.{cls}" if v else ""),
        "reference_url": f"{REF_BASE}/{info.get('web_name', '')}/#{slug(entry.get('name', ''))}",
        "statement": statement,
        "following_information": (v or {}).get("following_information") or entry.get("following_information") or [],
        "force": force,
        "affects": entry.get("affects") or [],
        "notes": entry.get("notes") or ([entry["note"]] if entry.get("note") else []),
        "artifacts": artifacts(entry, v),
        "timeframe": {k: (v or entry).get(k) for k in ("timeframe_type", "timeframe_num") if (v or entry).get(k) is not None},
        "terms": entry.get("terms") or [],
        "related": entry.get("related") or [],
        "schema": entry.get("schema"),
        "basis": basis,
        "process_status": info.get("status"),
        "effective": effective(info).get("is"),
        "updated": latest_update(entry),
        "statement_sha256": sha256_text(statement or ""),
    }


def resolve(data: dict, cls: str) -> dict:
    """Resolve the 20x Program applicability set for one class."""
    assert cls in CLASSES
    idx = index(data)
    ovl = overlay_ids(data) if cls == "a" else {}
    rules, others, conflicts, seen = [], [], [], set()

    for proc, bucket, subset, rid, entry, info in iter_frr(data):
        ap = subset_meta(info, bucket, subset).get("applicability", {})
        types, paths, classes = ap.get("types", []), ap.get("paths", []), ap.get("classes", [])
        statement, force, v, has_var = variant(entry, cls)
        affects = entry.get("affects") or ap.get("affects") or []
        by_subset = TYPE in types and PATH in paths and cls.upper() in classes
        unscoped = not types and not classes
        if has_var and statement is None:
            if rid in ovl:
                conflicts.append({"id": rid, "issue": f"Listed in {ovl[rid]} but has no class '{cls}' variant."})
            continue
        if by_subset or (rid in ovl):
            basis = []
            if by_subset:
                basis.append("subset")
            if rid in ovl:
                basis.append(ovl[rid])
            rec = _frr_record(proc, bucket, subset, rid, entry, info, cls, statement, force, v, basis)
            if rid in ovl:
                # The overlay sets the obligation to address the rule; the rule's own
                # force sets what addressing it means. Class A force is the weaker of
                # the two, keeping the rule's polarity (MUST NOT stays negative).
                ovf = OVERLAY[ovl[rid]]
                rec["overlay_force"] = ovf
                rec["statement_force"] = force
                if v and force != ovf and not (ovf == "MUST"):
                    conflicts.append({"id": rid, "issue": f"Class a variant force {force} differs from {ovl[rid]} ({ovf})."})
                if not v:
                    negative = (force or "").endswith("NOT")
                    if ovf == "SHOULD":
                        rec["force"] = "SHOULD NOT" if negative else "SHOULD"
                    elif ovf == "MAY":
                        rec["force"] = "MAY"
            if "Providers" in affects:
                rules.append(rec)
            else:
                others.append(rec)
            seen.add(rid)
        elif unscoped and set(affects) & {"Assessors", "FedRAMP"}:
            rec = _frr_record(proc, bucket, subset, rid, entry, info, cls, statement, force, v, ["unscoped"])
            others.append(rec)
        elif cls == "a" and has_var and "a" in entry["varies_by_class"] and "A" not in classes:
            conflicts.append({"id": rid, "issue": "Has a class 'a' variant, but subset applicability excludes Class A and no overlay rule lists it."})

    ksis = []
    for theme, kid, k, tv in iter_ksi(data):
        if cls == "a" and kid not in ovl:
            continue
        statement, _, v, has_var = variant(k, cls)
        if statement is None:
            if kid in ovl:
                conflicts.append({"id": kid, "issue": f"Listed in {ovl[kid]} but has no class '{cls}' variant."})
            continue
        optional = statement.startswith(OPTIONAL_PREFIX)
        ksis.append({
            "id": kid,
            "kind": "KSI",
            "name": k.get("name"),
            "theme": theme,
            "theme_name": tv.get("name"),
            "json_path": f"KSI.{theme}.indicators.{kid}" + (f".varies_by_class.{cls}" if v else ""),
            "reference_url": f"{REF_BASE}/key-security-indicators/#{slug(k.get('name', ''))}",
            "statement": statement,
            "optional": optional,
            "basis": [ovl[kid]] if kid in ovl else ["theme"],
            "overlay_force": OVERLAY[ovl[kid]] if kid in ovl else None,
            "controls": k.get("controls") or [],
            "terms": k.get("terms") or [],
            "theme_status": tv.get("status"),
            "updated": latest_update(k),
            "statement_sha256": sha256_text(statement),
        })

    for ref in ovl:
        if ref not in idx:
            conflicts.append({"id": ref, "issue": "Listed in the Class A overlay but not present in the dataset."})
        elif idx[ref].get("bucket") == "rev5":
            conflicts.append({"id": ref, "issue": "Listed in the Class A overlay but exists only in the Rev5 bucket."})

    rules.sort(key=lambda r: r["id"])
    ksis.sort(key=lambda r: r["id"])
    others.sort(key=lambda r: r["id"])

    # Rules pulled in by reference (e.g. FRC-CSO-PKG -> SDR-CSO-FRR) that are not
    # themselves in the set for this class. Reviewers still check them through
    # the referencing rule.
    listed = {r["id"] for r in rules} | {k["id"] for k in ksis}
    referenced = {}
    for r in rules:
        for item in r["following_information"]:
            for ref in re.findall(r"\b(?:KSI-[A-Z]{3}-[A-Z0-9]{3}|[A-Z]{3}-[A-Z]{3}-[A-Z0-9]{3})\b", item):
                if ref not in listed and ref != r["id"] and idx.get(ref, {}).get("kind") in ("FRR", "KSI"):
                    referenced.setdefault(ref, set()).add(r["id"])
    by_force = {}
    for r in rules:
        by_force[r["force"]] = by_force.get(r["force"], 0) + 1
    return {
        "class": cls,
        "counts": {
            "rules": len(rules),
            "rules_by_force": dict(sorted(by_force.items())),
            "ksis": len(ksis),
            "ksis_optional": sum(1 for k in ksis if k["optional"]),
            "other_actor_rules": len(others),
            "conflicts": len(conflicts),
        },
        "rules": rules,
        "ksis": ksis,
        "referenced_rules": [
            {"id": ref, "json_path": idx[ref]["json_path"], "via": sorted(via)}
            for ref, via in sorted(referenced.items())
        ],
        "other_actor_rules": others,
        "conflicts": conflicts,
    }
