"""Check FedRAMP upstream sources for changes and report what they affect.

What it does:
1. Compares the upstream HEAD of FedRAMP/rules, FedRAMP/schemas, and
   FedRAMP/2026-markdown with sources.lock.json (git ls-remote; no API calls).
2. On change: pulls the new files, validates the rules dataset against its
   schema, runs the semantic diff, regenerates data/rules-extract.json, and
   updates vendor/ and the lock.
3. Checks data/logic-bindings.json: any rule the tool's logic depends on whose
   content changed is listed as "logic review required".
4. Checks guide pages: any page that cites a changed rule, or a narrative
   source page that changed, is listed as "guide review required".
5. Writes reports/update-<date>.md and .json.

It never edits guide prose or tool logic. A person reviews the report.

Usage: python tools/check_updates.py [--force] [--offline-new-rules PATH]
Sets GitHub Actions outputs: changed, version, logic_review, guide_review.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import jsonschema

sys.path.insert(0, str(Path(__file__).parent))
import build_extract  # noqa: E402
import diff_rules  # noqa: E402
import fr_rules  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
LOCK = ROOT / "sources.lock.json"
BINDINGS = ROOT / "data/logic-bindings.json"
GUIDE = ROOT / "guide"
# Fields that never change tool logic; excluded from binding hashes.
BINDING_IGNORE = {"updated", "controls", "terms", "related", "reference", "reference_url", "alts", "tag"}
ID_RE = re.compile(r"\b(?:KSI-[A-Z]{3}-[A-Z0-9]{3}|FRD-[A-Z]{3}|[A-Z]{3}-[A-Z]{3}-[A-Z0-9]{3})\b")


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def remote_head(url: str) -> str:
    out = subprocess.run(["git", "ls-remote", url, "HEAD"], capture_output=True, text=True, check=True).stdout
    return out.split()[0]


def clone(url: str, dest: Path) -> str:
    subprocess.run(["git", "clone", "--depth", "1", "-q", url, str(dest)], check=True)
    return subprocess.run(["git", "-C", str(dest), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()


def binding_hash(data: dict, rid: str) -> str | None:
    """Hash of the content a binding depends on (excludes BINDING_IGNORE fields)."""
    flat = diff_rules.flatten(data)
    if rid not in flat:
        return None
    e = {k: v for k, v in flat[rid]["entry"].items() if k not in BINDING_IGNORE}
    if flat[rid]["kind"] == "FRR":
        e["_applicability"] = flat[rid].get("applicability")
    return fr_rules.sha256_text(fr_rules.canon(e))


def check_bindings(data: dict) -> list[dict]:
    if not BINDINGS.exists():
        return []
    b = json.loads(BINDINGS.read_text())
    out = []
    for item in b["bindings"]:
        h = binding_hash(data, item["id"])
        if h != item.get("content_sha256"):
            out.append({"id": item["id"], "used_for": item["used_for"],
                        "status": "removed" if h is None else "changed"})
    return out


def refresh_bindings(data: dict, version: str) -> None:
    """Re-stamp binding hashes. Run only after a person has reviewed the logic."""
    b = json.loads(BINDINGS.read_text())
    for item in b["bindings"]:
        item["content_sha256"] = binding_hash(data, item["id"])
    b["reviewed_against"] = version
    BINDINGS.write_text(json.dumps(b, indent=1) + "\n")


def front_matter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    fm = {"rules": [], "sources": [], "reviewed_against": None}
    if not m:
        return fm
    cur = None
    for line in m.group(1).splitlines():
        if re.match(r"^\w[\w_]*:", line):
            key, _, val = line.partition(":")
            cur = key.strip()
            if val.strip():
                fm[cur] = val.strip().strip('"')
            else:
                fm.setdefault(cur, [])
        elif line.strip().startswith("- ") and cur:
            if not isinstance(fm.get(cur), list):
                fm[cur] = []
            fm[cur].append(line.strip()[2:].strip())
    return fm


def guide_impact(changed_ids: set[str], changed_sources: set[str], new_version: str) -> list[dict]:
    out = []
    for page in sorted(GUIDE.glob("*.md")):
        if page.name == "README.md":
            continue
        text = page.read_text(encoding="utf-8")
        fm = front_matter(text)
        cited = set(fm.get("rules") or []) | set(ID_RE.findall(text))
        hits = sorted(cited & changed_ids)
        src_hits = sorted(set(fm.get("sources") or []) & changed_sources)
        if hits or src_hits:
            out.append({"page": str(page.relative_to(ROOT)), "rules": hits, "sources": src_hits,
                        "reviewed_against": fm.get("reviewed_against"), "new_version": new_version})
    return out


def set_output(**kw) -> None:
    path = os.environ.get("GITHUB_OUTPUT")
    if path:
        with open(path, "a") as fh:
            for k, v in kw.items():
                fh.write(f"{k}={v}\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="re-pull even if HEADs match the lock")
    ap.add_argument("--accept-bindings", action="store_true",
                    help="re-stamp logic-binding hashes after a person reviewed the tool logic")
    args = ap.parse_args()
    lock = json.loads(LOCK.read_text())

    if args.accept_bindings:
        data = fr_rules.load(ROOT / "vendor/rules/fedramp-consolidated-rules.json")
        refresh_bindings(data, data["info"]["version"])
        print("Logic bindings re-stamped against", data["info"]["version"])
        return 0

    heads = {k: remote_head(v["repo"]) for k, v in lock["sources"].items()}
    changed_repos = [k for k, h in heads.items() if h != lock["sources"][k]["commit"]]
    if not changed_repos and not args.force:
        print("No upstream changes:", ", ".join(f"{k}@{h[:7]}" for k, h in heads.items()))
        set_output(changed="false")
        return 0

    today = dt.date.today().isoformat()
    report = {"date": today, "repos": {}, "rules": None, "schemas": {}, "narrative": [],
              "logic_review": [], "guide_review": []}
    changed_ids: set[str] = set()
    changed_sources: set[str] = set()
    new_version = lock["sources"]["rules"].get("version")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for key in (changed_repos if not args.force else list(lock["sources"])):
            src = lock["sources"][key]
            dest = tmp / key
            commit = clone(src["repo"], dest)
            report["repos"][key] = {"old": src["commit"], "new": commit}

            if key == "rules":
                new_rules = dest / "fedramp-consolidated-rules.json"
                new_schema = dest / "schemas/fedramp-consolidated-rules.schema.json"
                new_data = fr_rules.load(new_rules)
                errs = list(jsonschema.Draft202012Validator(fr_rules.load(new_schema)).iter_errors(new_data))
                if errs:
                    report["rules"] = {"error": f"New dataset failed its schema: {errs[0].message}"}
                    break
                old_path = ROOT / "vendor/rules/fedramp-consolidated-rules.json"
                if sha256_file(new_rules) != sha256_file(old_path) or args.force:
                    d = diff_rules.diff(fr_rules.load(old_path), new_data)
                    report["rules"] = {"old_version": d["old_version"], "new_version": d["new_version"],
                                       "summary": d["summary"], "applicability": d["applicability"]}
                    changed_ids |= {e["id"] for e in d["entries"]
                                    if any(x["severity"] in ("high", "medium") for x in e["changes"])}
                    md = diff_rules.to_markdown(d)
                    (ROOT / f"reports/rules-diff-{d['new_version']}.md").write_text(md)
                    shutil.copy(new_rules, old_path)
                    shutil.copy(new_schema, ROOT / "vendor/rules/fedramp-consolidated-rules.schema.json")
                    new_version = new_data["info"]["version"]
                    src.update(version=new_version, last_updated=new_data["info"]["last_updated"],
                               sha256=sha256_file(new_rules))
                    report["logic_review"] = check_bindings(new_data)
                src["commit"] = commit

            elif key == "schemas":
                for f in sorted(dest.glob("fedramp-*-schema-*.json")):
                    old = ROOT / "vendor/schemas" / f.name
                    if not old.exists():
                        report["schemas"][f.name] = {"status": "added", "new_version": fr_rules.load(f).get("$schemaVersion")}
                    elif sha256_file(old) != sha256_file(f):
                        report["schemas"][f.name] = diff_rules.schema_diff(fr_rules.load(old), fr_rules.load(f))
                    else:
                        continue
                    shutil.copy(f, old)
                for old in (ROOT / "vendor/schemas").glob("*.json"):
                    if not (dest / old.name).exists():
                        report["schemas"][old.name] = {"status": "removed upstream (kept locally)"}
                src["files"] = {p.name: {"version": fr_rules.load(p).get("$schemaVersion"), "sha256": sha256_file(p)}
                                for p in sorted((ROOT / "vendor/schemas").glob("*.json"))}
                src["commit"] = commit

            elif key == "markdown":
                for rel, old_hash in sorted(src.get("pages", {}).items()):
                    p = dest / rel
                    new_hash = sha256_file(p) if p.exists() else None
                    if new_hash != old_hash:
                        report["narrative"].append({"page": rel, "status": "removed" if new_hash is None else "changed"})
                        changed_sources.add(rel)
                        src["pages"][rel] = new_hash
                src["commit"] = commit

    if report["rules"] and "error" not in report["rules"]:
        extract = build_extract.build(ROOT / "vendor/rules/fedramp-consolidated-rules.json",
                                      ROOT / "vendor/rules/fedramp-consolidated-rules.schema.json", lock)
        jsonschema.Draft202012Validator(fr_rules.load(ROOT / "data/rules-extract.schema.json")).validate(extract)
        (ROOT / "data/rules-extract.json").write_text(json.dumps(extract, indent=1, ensure_ascii=False) + "\n")

    report["guide_review"] = guide_impact(changed_ids, changed_sources, new_version)
    LOCK.write_text(json.dumps(lock, indent=1) + "\n")
    stem = f"update-{today}"
    (ROOT / f"reports/{stem}.json").write_text(json.dumps(report, indent=1) + "\n")
    (ROOT / f"reports/{stem}.md").write_text(render(report))
    print(render(report))
    set_output(changed="true", version=new_version or "",
               logic_review=str(bool(report["logic_review"])).lower(),
               guide_review=str(bool(report["guide_review"])).lower(), report=f"reports/{stem}.md")
    return 1 if report["rules"] and "error" in report["rules"] else 0


def render(r: dict) -> str:
    L = [f"# Upstream Update Check: {r['date']}", ""]
    L += ["## Sources", "", "| Source | Old | New |", "| --- | --- | --- |"]
    L += [f"| {k} | `{v['old'][:7]}` | `{v['new'][:7]}` |" for k, v in r["repos"].items()] + [""]
    if r["rules"]:
        if "error" in r["rules"]:
            L += ["!!! danger \"The new rules dataset failed schema validation!\"", f"    {r['rules']['error']}", ""]
        else:
            ru = r["rules"]
            L += [f"## Rules: {ru['old_version']} to {ru['new_version']}", ""]
            L += [f"- High: {', '.join(ru['summary']['high']) or 'None'}",
                  f"- Medium: {', '.join(ru['summary']['medium']) or 'None'}",
                  f"- Low: {len(ru['summary']['low'])} entries (controls, terms, notes)", ""]
            L += ["| Class | Added | Removed | Force changed |", "| --- | --- | --- | --- |"]
            for c, a in ru["applicability"].items():
                fc = ", ".join(f"{x['id']} ({x['old']} to {x['new']})" for x in a["force_changed"]) or "None"
                L.append(f"| {c.upper()} | {', '.join(a['added']) or 'None'} | {', '.join(a['removed']) or 'None'} | {fc} |")
            L += ["", f"Full diff: `reports/rules-diff-{ru['new_version']}.md`. Tool data regenerated: `data/rules-extract.json`.", ""]
    if r["schemas"]:
        L += ["## Package Schemas", ""]
        for name, s in r["schemas"].items():
            if "status" in s:
                L.append(f"- `{name}`: {s['status']}")
            else:
                L.append(f"- `{name}`: {s['old_version']} to {s['new_version']}; required changed {len(s['required_changed'])}, "
                         f"enums changed {len(s['enum_changed'])}, properties +{len(s['properties_added'])}/-{len(s['properties_removed'])}")
        L.append("")
    L += ["## Logic Review Required", ""]
    L += [f"- [ ] `{b['id']}` ({b['status']}): {b['used_for']}" for b in r["logic_review"]] or ["- None"]
    L += ["", "After review, run `python tools/check_updates.py --accept-bindings`.", "", "## Guide Review Required", ""]
    L += [f"- [ ] `{g['page']}`: rules {', '.join(g['rules']) or 'none'}; sources {', '.join(g['sources']) or 'none'}; "
          f"reviewed against {g['reviewed_against']}" for g in r["guide_review"]] or ["- None"]
    if r["narrative"]:
        L += ["", "## Narrative Pages Changed", ""] + [f"- `{n['page']}`: {n['status']}" for n in r["narrative"]]
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
