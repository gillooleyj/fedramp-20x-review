# Keeping the Guide and Tool Current

This page explains how upstream FedRAMP changes reach the tool and the guide, and what a person must review. It is for whoever maintains this repository.

## What Is Watched

| Source | What changes | Effect here |
| --- | --- | --- |
| FedRAMP/rules | Rules, KSIs, definitions, class variants, Class A overlay, force | Tool data regenerated; logic bindings and guide pages flagged |
| FedRAMP/schemas | SDR, CPO, OCR, and other package schemas (versioned inside each file; filenames keep the 2026-06-24 date) | Validators updated; schema changes listed |
| FedRAMP/2026-markdown | Narrative pages the guide cites (`sources:` in each page's front matter) | Guide pages flagged |

FedRAMP moved to a monthly rules release after 2026.11.02.01, usually in the first week of each month. The check runs daily so fixes between releases are also caught.

## How a Change Flows

1. **Detect.** `check_updates.py` compares each upstream HEAD (from `git ls-remote`) with `sources.lock.json`.
2. **Validate.** A new rules dataset must pass `schemas/fedramp-consolidated-rules.schema.json`. If it fails, the run stops and the workflow fails.
3. **Diff by content.** `diff_rules.py` compares entries field by field. It does not trust the `updated` arrays; the 2026.11.02.01 changelog records changes to IEC-CSO-IIR, IEC-CSO-OIR, and IEC-CSO-FIR that have no `updated` entry.
4. **Regenerate data.** `data/rules-extract.json` is rebuilt and validated. This part is automatic.
5. **Flag logic.** Each rule in `data/logic-bindings.json` carries a content hash. A changed hash means the tool's coded logic may be wrong. Review the logic, fix it if needed, then run `python tools/check_updates.py --accept-bindings`.
6. **Flag guide pages.** Any page that cites a high or medium change, or whose cited narrative source changed, is listed. Edit the page, then set `reviewed_against` to the new version.
7. **Open a pull request.** The workflow opens or updates one pull request labeled `rules-update`, plus `needs-logic-review` or `needs-guide-review` as applicable.

> [!WARNING]
> **Do not merge a rules update with an open logic or guide checklist!**
> Regenerated data with stale logic produces confident wrong results. Clear both checklists first.

## Severity

| Severity | Examples |
| --- | --- |
| High | Rule added or removed; force changed; class variant added or removed; **Optional:** prefix changed; subset applicability or effective dates changed; Class A overlay list changed |
| Medium | Statement wording; `following_information`; artifacts; timeframes; definitions; notification metadata |
| Low | Controls, terms, related, notes, examples |

## One-Time Setup

Done when the repository was created: public repository, GitHub Pages set to deploy from GitHub Actions, Actions allowed to create pull requests, and the three labels created.

Remaining step. Remote file tools can't write `.github/workflows/` or `mkdocs.yml`, so these three files are added by hand once:

1. Save `mkdocs.yml` (supplied separately) in the repository root.
2. From the repository folder, run:

```sh
mkdir -p .github/workflows && git mv setup/rules-update.yml setup/pages.yml .github/workflows/ && git add mkdocs.yml && git commit -m "Add workflows and site config" && git push
```

The push publishes the site at https://gillooleyj.github.io/fedramp-20x-review/. Then run **Check FedRAMP upstream updates** once from the Actions tab to confirm it reports "No upstream changes."

Data updates are automatic; changes to meaning always pass through a person.
