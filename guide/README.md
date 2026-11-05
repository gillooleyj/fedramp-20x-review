# Guide Page Conventions

Every guide page starts with front matter that the update check reads:

```yaml
---
tags:
  - FedRAMP
  - Guidance
audience: FedRAMP reviewers
type: Guidance
reviewed_against: 2026.11.02.01   # rules version the page was last checked against
rules:                            # every rule, KSI, and definition ID the page relies on
  - SDR-CSO-FRR
sources:                          # 2026-markdown pages the page relies on, as repo paths
  - assessors/fedramp-assessments/20x.md
---
```

1. List every ID the page relies on under `rules`. The check also scans the body for IDs.
2. List cited narrative pages under `sources` and add their hashes to `sources.lock.json` under `markdown.pages`.
3. Cite rules as `ID (Name)` using the dataset name exactly.
4. After editing a page for a rules update, set `reviewed_against` to the new version.
5. Write in the FedRAMP narrative register and run the fedramp-voice self-check before committing.

## Pages

| Page | Status |
| --- | --- |
| `assessor-role.md` | Draft, reviewed against 2026.11.02.01 |
