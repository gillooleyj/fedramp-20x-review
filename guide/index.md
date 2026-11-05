---
tags:
  - FedRAMP
  - Guidance
  - 20x
audience: FedRAMP reviewers
type: Guidance
reviewed_against: 2026.11.02.01
rules:
  - FRD-CRP
  - FRD-CCL
  - FRD-ANA
  - FRD-MST
  - FRD-SHD
  - FRD-MAY
sources:
  - responsibilities/fedramp.md
  - agencies/use/classes.md
---

# FedRAMP 20x Review Guide

This guide helps FedRAMP reviewers assess FedRAMP 20x Certification Packages for Class A, B, and C. It explains what a review decides, who assesses what, and which rules and Key Security Indicators (KSIs) apply to each class.

!!! warning "This is not an official FedRAMP or GSA product!"
    It's a personal working guide maintained by a FedRAMP team member. It doesn't set FedRAMP policy or make Certification decisions. The [FedRAMP Consolidated Rules for 2026](https://www.fedramp.gov/2026/) govern.

## What a Review Decides

1. **FedRAMP doesn't decide whether a service is "secure enough."** A FedRAMP Certification supplies sufficient information, following FedRAMP rules, for agencies to make their own decisions ([FedRAMP's Responsibilities](https://www.fedramp.gov/2026/responsibilities/fedramp/)).
2. **The package is the essential information an agency uses to decide** whether to authorize the service (FRD-CRP (Certification Package)).
3. **A Certification Class measures assurance information, not security** (FRD-CCL (Certification Class); [Certification Classes](https://www.fedramp.gov/2026/agencies/use/classes/)).
4. **FedRAMP is one of all necessary assessors** (FRD-ANA (All Necessary Assessors)), so providers owe reviewers evidence directly.
5. **Force sets the consequence.** A MUST failure is a vulnerability likely requiring corrective action or denial (FRD-MST (MUST)). A SHOULD departure is allowed only when the decision is documented (FRD-SHD (SHOULD)). A MAY rule is optional, and the decision should still be explained (FRD-MAY (MAY)).

For every rule and KSI, ask whether the package gives an agency accurate, current, and sufficient information under the class rules, and whether the evidence supports the claim.

## Pages

| Page | What it covers |
| --- | --- |
| [The Assessor's Role](assessor-role.md) | Who assesses what, what the independent assessor delivers, and how to check the assessor's work |
| [Class A](reference/class-a.md), [Class B](reference/class-b.md), [Class C](reference/class-c.md) | Every rule and KSI that applies to the class, with force and the official link |
| [Differences by Class](reference/class-differences.md) | Rules and KSIs whose force or inclusion changes between classes |

!!! info "How this site stays current"
    A daily check compares this site's pinned data with FedRAMP/rules, FedRAMP/schemas, and FedRAMP/2026-markdown. The Rules by Class pages regenerate from the dataset when an update is merged. Guide pages show the rules version they were last reviewed against.

The review tests whether each claim is supported for an agency's decision.
