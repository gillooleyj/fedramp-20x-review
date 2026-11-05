# Status: fedramp-20x-review

Last updated: 2026-11-05
Status: Active
Goal: Reviewer guide and companion tool for FedRAMP 20x Class A, B, and C packages, driven by the rules dataset
Depends on: FedRAMP/rules, FedRAMP/schemas, FedRAMP/2026-markdown

## Current State
- Milestone 1 done: rules engine (`data/rules-extract.json`) for 2026.11.02.01. Class A 51 rules and 7 KSIs; Class B 154 rules and 46 KSIs (5 optional); Class C 154 rules and 46 KSIs.
- Upstream update check built and tested against real history (2026.10.05.01 to 2026.11.02.01).
- First guide page drafted: `guide/assessor-role.md`.

## Next Step
- Add `mkdocs.yml` and move `setup/*.yml` into `.github/workflows/` (docs/update-process.md), which publishes the site and starts the daily update check.
- Milestone 2: package intake (load SDR, CPO, OCR; schema validation; coverage both ways).

## Blockers
- None

## Recent Changes
- 2026-11-05: Repository created from research and plan.
- 2026-11-05: Public repository gillooleyj/fedramp-20x-review created; Pages set to GitHub Actions; labels created; Actions allowed to open pull requests. Sample-derived findings removed from docs/plan.md.
