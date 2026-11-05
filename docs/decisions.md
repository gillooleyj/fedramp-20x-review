# Decisions: fedramp-20x-review

Append-only. Newest at the bottom.

## 2026-11-05: New build driven by the rules dataset
- Why: The earlier Review Companion was built with ChatGPT without a research foundation and used hand-written class lenses on a 2026-09-14 snapshot.
- Rejected: Rebasing the earlier Review Companion.
- Surface: chat

## 2026-11-05: Private personal GitHub repository, hosted as a static site
- Why: Personal use first; content is not sensitive to FedRAMP. Provider packages never enter the repository.
- Rejected: Public repository; local-only file.
- Surface: chat

## 2026-11-05: No single score; rollup of tool status beside reviewer status
- Why: An average hides MUST failures that FRD-MST treats as grounds for denial. Tool status describes the evidence chain; reviewer status describes the decision.
- Rejected: Overall quality percentage; a single "favorable" count.
- Surface: chat

## 2026-11-05: Upstream changes update data automatically and flag meaning for a person
- Why: Rules changes can alter force, applicability, and class variants. Auto-editing guide prose or tool logic would let an upstream change silently alter the review standard.
- Rejected: Fully automatic guide and logic updates; manual checking only.
- Surface: chat

## 2026-11-05: Review Sheet fixes go to the Vanguard Team Lead
- Why: The team lead owns the shared workbook.
- Rejected: Maintaining a private corrected copy.
- Surface: chat

## 2026-11-05: Public GitHub repository and GitHub Pages
- Why: Supersedes the private-repository decision. Content is not sensitive to FedRAMP, and a public repository gets GitHub Pages without a paid plan.
- Conditions: Provider packages and package-derived findings stay out of the repository; the site and README state that this is not an official FedRAMP or GSA product; no FedRAMP branding.
- Rejected: Private repository with GitHub Pro; Vercel.
- Surface: chat
