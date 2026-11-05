@../fedramp-hub/RULES.md
@../fedramp-hub/PORTFOLIO.md
@STATUS.md
@docs/origin.md

This repo is the fedramp-20x-review workstream: a reviewer guide and companion review tool for FedRAMP 20x Class A, B, and C packages. Hub rules apply; local rules below override them only where stated.

## Local Rules
- Treat `vendor/rules/fedramp-consolidated-rules.json` as read-only. Update it only through `tools/check_updates.py`.
- Never commit provider packages, review sheets, or review notes. Use fictional or anonymized examples.
- Tool logic that depends on a rule's meaning must have an entry in `data/logic-bindings.json`.
- Guide pages follow `guide/README.md` and the fedramp-voice skill.
- The disposition table (docs/plan.md Section 3) is PRE-DECISIONAL until approved.

## End of Session (Required)
Before ending any session that changed code, plans, or understanding:
1. Update STATUS.md (state, next step, blockers, Last updated).
2. Append to docs/decisions.md: decision, date, why, rejected alternatives.
3. Commit both with the work.
At session start, also read the newest file in docs/handoffs/ if it is newer than STATUS.md.
