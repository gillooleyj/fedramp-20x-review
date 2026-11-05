"""Generate the Rules by Class pages for the site from data/rules-extract.json.

Writes guide/reference/class-a.md, class-b.md, class-c.md, and class-differences.md.
These pages are generated at build time and are not committed.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "guide/reference"
BASIS = {
    "subset": "Applies to this class",
    "FRC-CLA-MFR": "Mandatory overlay (FRC-CLA-MFR)",
    "FRC-CLA-RFR": "Recommended overlay (FRC-CLA-RFR)",
    "FRC-CLA-OFR": "Optional overlay (FRC-CLA-OFR)",
    "unscoped": "Applies regardless of class",
    "theme": "Included",
}
FORCE_ORDER = ["MUST", "MUST NOT", "SHOULD", "SHOULD NOT", "MAY"]


def cell(text: str) -> str:
    return (text or "").replace("|", "\\|").replace("\n", " ")


def link(r: dict) -> str:
    return f"[{r['id']}]({r['reference_url']})"


def class_page(x: dict, c: str) -> str:
    src, cs = x["source"], x["classes"][c]
    C = c.upper()
    L = ["---", "tags:", "  - FedRAMP", "  - Rules", "  - 20x", "---", "",
         f"Generated reference · Rules {src['version']}", "{: .fr-eyebrow }", "",
         f"# Class {C} Rules and Key Security Indicators", "",
         f"This page lists the FedRAMP rules and Key Security Indicators (KSIs) that apply to a FedRAMP 20x Program "
         f"Certification at Class {C}. It is generated from the FedRAMP Consolidated Rules for 2026 dataset.", "",
         f'!!! info "Rules version {src["version"]} ({src["last_updated"]})"',
         f"    Generated from FedRAMP/rules commit `{(src.get('commit') or '')[:7]}`. Each ID links to the official rule on "
         "fedramp.gov, which governs.", ""]
    counts = cs["counts"]
    L += ["## Summary", "", "| Type | Count |", "| --- | ---: |", f"| Rules | {counts['rules']} |"]
    L += [f"| Rules with {f} | {counts['rules_by_force'][f]} |" for f in FORCE_ORDER if f in counts["rules_by_force"]]
    L += [f"| KSIs | {counts['ksis']} ({counts['ksis_optional']} optional) |", ""]

    L += ["## Rules", "", "| ID | Name | Force | How it applies |", "| --- | --- | --- | --- |"]
    for r in cs["rules"]:
        how = "; ".join(BASIS.get(b, b) for b in r["basis"])
        force = r["force"] + (f" (rule text: {r['statement_force']})" if r.get("statement_force") and r["statement_force"] != r["force"] else "")
        L.append(f"| {link(r)} | {cell(r['name'])} | {force} | {how} |")
    L += ["", "## Key Security Indicators", "", "| ID | Name | Theme | Status |", "| --- | --- | --- | --- |"]
    for k in cs["ksis"]:
        status = "Optional" if k["optional"] else BASIS.get(k["basis"][0], k["basis"][0])
        L.append(f"| {link(k)} | {cell(k['name'])} | {cell(k['theme_name'])} | {status} |")
    L.append("")

    if cs.get("referenced_rules"):
        L += ["## Rules Applied by Reference", "",
              "These rules are not listed for this class directly, but a listed rule requires their content.", ""]
        L += [f"- `{r['id']}` through {', '.join(r['via'])}" for r in cs["referenced_rules"]] + [""]

    others = [r for r in cs["other_actor_rules"] if set(r["affects"]) & {"Assessors", "FedRAMP"}]
    if others:
        L += ["## Rules for Assessors and FedRAMP", "", "| ID | Name | Actor | Force |", "| --- | --- | --- | --- |"]
        L += [f"| {link(r)} | {cell(r['name'])} | {', '.join(r['affects'])} | {r['force']} |" for r in others] + [""]

    if cs["conflicts"]:
        L += ['!!! warning "Dataset inconsistencies found!"', "    These were found while resolving applicability. The rules dataset may change to fix them.", ""]
        L += [f"    - `{x_['id']}`: {x_['issue']}" for x_ in cs["conflicts"]] + [""]

    L += ["## Statements", ""]
    for r in cs["rules"] + cs["ksis"]:
        L += [f"### {r['id']}: {r['name']}", "", f"> {r['statement']}", ""]
        for item in r.get("following_information") or []:
            L.append(f"> - {item}")
        if r.get("following_information"):
            L.append("")
        L += [f"[Official rule]({r['reference_url']}) · `{r['json_path']}`", ""]
    return "\n".join(L) + "\n"


def differences_page(x: dict) -> str:
    rows = {}
    for c in "abc":
        cs = x["classes"][c]
        for r in cs["rules"]:
            tf = r.get("timeframe") or {}
            unit = (tf.get("timeframe_type") or "").rstrip("s") if tf.get("timeframe_num") == 1 else tf.get("timeframe_type")
            when = f" ({tf['timeframe_num']} {unit})" if tf.get("timeframe_num") is not None else ""
            rows.setdefault(r["id"], {"name": r["name"], "url": r["reference_url"]})[c] = r["force"] + when
        for k in cs["ksis"]:
            rows.setdefault(k["id"], {"name": k["name"], "url": k["reference_url"]})[c] = "Optional" if k["optional"] else "Included"
    src = x["source"]

    def table(ids):
        out = ["| ID | Name | Class A | Class B | Class C |", "| --- | --- | --- | --- | --- |"]
        for i in sorted(ids):
            v = rows[i]
            out.append(f"| [{i}]({v['url']}) | {cell(v['name'])} | {v.get('a', 'Not listed')} | "
                       f"{v.get('b', 'Not listed')} | {v.get('c', 'Not listed')} |")
        return out

    b_c = [i for i, v in rows.items() if v.get("b", "Not listed") != v.get("c", "Not listed")]
    a_b = [i for i, v in rows.items() if "a" in v and v.get("b", "Not listed") != v["a"]]
    not_a = sorted(i for i, v in rows.items() if "a" not in v and ("b" in v or "c" in v))
    L = ["---", "tags:", "  - FedRAMP", "  - Rules", "  - 20x", "---", "",
         f"Generated reference · Rules {src['version']}", "{: .fr-eyebrow }", "",
         "# Differences by Class", "",
         "This page shows where the rules and KSIs for a FedRAMP 20x Program Certification change between Class A, B, and C. "
         "Use it to see how expectations change from Class A to Class C.", "",
         f'!!! info "Rules version {src["version"]} ({src["last_updated"]})"',
         "    Generated from the FedRAMP Consolidated Rules for 2026 dataset. Timeframes appear in parentheses. \"Not listed\" means the rule or KSI does not apply to that class.", "",
         "## Class B Compared With Class C", "",
         f"{len(b_c)} rules and KSIs differ between Class B and Class C.", ""] + table(b_c) + ["",
         "## Class A Compared With Class B", "",
         f"{len(a_b)} rules and KSIs listed for Class A differ from Class B.", ""] + table(a_b) + ["",
         "## Not Listed for Class A", "",
         f"{len(not_a)} rules and KSIs that apply to Class B or C are not listed for Class A.", "",
         f'??? note "Show all {len(not_a)} IDs"',
         "    " + ", ".join(f"`{i}`" for i in not_a) + ".", ""]
    return "\n".join(L) + "\n"


def main() -> int:
    x = json.loads((ROOT / "data/rules-extract.json").read_text())
    OUT.mkdir(parents=True, exist_ok=True)
    for c in "abc":
        (OUT / f"class-{c}.md").write_text(class_page(x, c), encoding="utf-8")
    (OUT / "class-differences.md").write_text(differences_page(x), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}/class-a.md, class-b.md, class-c.md, class-differences.md for {x['source']['version']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
