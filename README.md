# FedRAMP 20x Review Guide and Tool

A reviewer guide and a companion review tool for FedRAMP 20x Class A, B, and C Certification Packages. The tool runs on the FedRAMP Consolidated Rules for 2026 dataset, so applicability, force, class variants, and expected artifacts come from the source.

> [!WARNING]
> **This is not an official FedRAMP or GSA product!**
> It is a personal working tool maintained by a FedRAMP team member. It does not set FedRAMP policy, does not make Certification decisions, and does not replace the [FedRAMP Consolidated Rules for 2026](https://www.fedramp.gov/2026/). The rules dataset governs.

Site: https://gillooleyj.github.io/fedramp-20x-review/

## Layout

| Path | Contents |
| --- | --- |
| `vendor/rules/` | Pinned `fedramp-consolidated-rules.json` and its schema from FedRAMP/rules |
| `vendor/schemas/` | Pinned package schemas (SDR, CPO, OCR, and others) from FedRAMP/schemas |
| `sources.lock.json` | Upstream commits, versions, and hashes for everything in `vendor/` and the narrative pages the guide cites |
| `data/rules-extract.json` | Generated: rules and KSIs that apply to 20x Program Certification for each class |
| `data/logic-bindings.json` | Rules whose meaning is coded into tool logic or the review standard |
| `tools/` | `build_extract.py`, `diff_rules.py`, `check_updates.py`, `fr_rules.py` |
| `guide/` | Reviewer guide pages and site source (see `guide/README.md`) |
| `mkdocs.yml` | Site configuration |
| `reports/` | Update reports and rules diffs |
| `docs/` | Plan, decisions, update process, handoffs |

## Use

1. Install: `pip install -r requirements.txt`
2. Rebuild the extract: `python tools/build_extract.py`
3. Check for upstream changes: `python tools/check_updates.py`
4. Compare any two rules files: `python tools/diff_rules.py OLD.json NEW.json`
5. Run tests: `python -m unittest discover -s tests`

## Keeping Current

A scheduled GitHub Action (`.github/workflows/rules-update.yml`) runs `check_updates.py` daily. When FedRAMP publishes a change, it opens a pull request with the regenerated data, a change report, and checklists of tool logic and guide pages to review. Nothing merges on its own. See `docs/update-process.md`.

> [!WARNING]
> **Never commit provider packages!**
> Provider SDRs carry confidentiality markings. The tool reads packages in the browser only. Sample-based tests use fictional or anonymized data.

## Site

The guide is built with MkDocs Material from `guide/` and published with GitHub Pages by `.github/workflows/pages.yml` (shipped in `setup/` until moved; see `docs/update-process.md`) on every push to `main`. `tools/build_site_pages.py` generates the Rules by Class pages from `data/rules-extract.json` at build time, so a merged rules update republishes the site with current data.

Build locally: `pip install -r requirements-site.txt && python tools/build_site_pages.py && mkdocs serve`

The tool reports where an evidence chain breaks; the reviewer decides what it means.
