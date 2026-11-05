# FedRAMP 20x Package Review: Research Findings and Build Plan

PRE-DECISIONAL: Sections 2 and 3 propose a review standard that requires approval before team use.

Research findings and a build plan for a reviewer guide and a companion review tool for FedRAMP 20x Class A, B, and C packages. Written for the FedRAMP review team and the program owner who approves the review standard.

**Bottom line**

1. CR26 contains no rule that tells FedRAMP how to review a package. The review standard has to be derived from what providers and assessors must supply, the force definitions, and FedRAMP's stated purpose. The guide becomes the first written version of that standard, so the program owner must approve it before the tool encodes it.
2. An earlier Review Companion (guide plus local JSON tool) was built November 4, 2026 on a September 14 rules snapshot plus selected live-page checks. It was built without a research foundation, so the new build starts from the rules dataset instead (Section 10).
3. Review Sheet v1.08 trails rules release 2026.11.02.01 in seven places (Section 6).

## Sources and versions

| Source | Version | Notes |
| --- | --- | --- |
| `FedRAMP/rules` | commit `64fa769`, 2026-11-02 | `info.version` 2026.11.02.01; `info.last_updated` 2026-11-02. Validated against `schemas/fedramp-consolidated-rules.schema.json`: 0 errors. |
| `FedRAMP/2026-markdown` | commit `888be03`, 2026-11-03 | `_sources.json` shows it was built from rules `64fa769`, so narrative and rules match. |
| SDR, CPO, OCR schemas | SDR 1.1.1, CPO 0.2.0, OCR 0.2.1 (2026-06-24 files) | Pinned in `vendor/schemas/` from FedRAMP/schemas commit `8fe79fa` (2026-10-27). Versions live inside each file; filenames keep the 2026-06-24 date. |
| Internal SOP | Draft v0.1 (revision history to 0.03, 2026-10-15) | Phase 2 states it does not tell a reviewer how to analyze a package or interpret Rules and KSIs. |
| Review Sheet | Starter All Classes v1.08 | Class A 40 rows, Class B 188, Class C 189. |
| Official communications | Blogs 2026-07-30, 2026-10-08, 2026-11-02; help article on "see the SOC 2 report"; NTC-0007 | None describe review steps. They explain intent and rollout. |

## 1. What the review is for

1. FedRAMP does not decide whether a service is "secure enough." A certification supplies sufficient information, following FedRAMP rules, for agencies to make their own decisions (`responsibilities/fedramp.md`, "Limitations on FedRAMP's Responsibilities").
2. The Certification Package is "the essential information that can be used by an agency to determine whether to authorize" (FRD-CRP, `FRD.data.all.FRD-CRP`).
3. A Certification Class measures the assurance information a provider commits to supply, not how secure the service is (FRD-CCL; `agencies/use/classes.md`).
4. FedRAMP is one of All Necessary Assessors (FRD-ANA). IVV-CSO-SEI (Supply Evidence of Implementation), IVV-CSO-SEE (Supply Evidence of Effectiveness), and IVV-CSO-STE (Supply Technical Explanations) therefore give reviewers the basis to request evidence and explanations directly.
5. Force sets the consequence. MUST and MUST NOT failures are "a vulnerability likely requiring corrective action and/or the denial" of certification (FRD-MST, FRD-MNT). SHOULD and SHOULD NOT allow justified departures, but parties MUST document the decision (FRD-SHD, FRD-SNT). MAY is optional; parties SHOULD explain the decision (FRD-MAY).
6. Assessors verify and validate at a technical level, not from documentation or screenshots (IVV-IAS-VIM, IVV-IAS-VEF). FedRAMP makes the certification decision. Agencies decide fit (`assessors/fedramp-assessments/20x.md`).
7. The published review flow is: cursory completeness scan, team assignment, CPO review, deep dive on CPO and SDR, final assessment. The clock stops while FedRAMP waits on the provider (`providers/implement/get-certified.md`). The SOP supplies the internal workflow for these steps.

The reviewer's question for every rule and KSI: does the package give an agency accurate, current, and sufficient information under the applicable class rules, and does the evidence support the claim?

## 2. The evidence chain

The chain for each entry comes from the elements SDR-CSO-FRR (FedRAMP Rules) and SDR-CSX-KSI (Key Security Indicators) require. Several required elements have no field in SDR schema 1.1.1, so providers place them inconsistently or omit them.

### FedRAMP rules (FRR)

| # | Required element | Rule basis | SDR 1.1.1 field | Schema gap |
| --- | --- | --- | --- | --- |
| 1 | How the rule is followed, or the reason and resulting customer risk | SDR-CSO-FRR | `frrImplementation` | None |
| 2 | Provider verification that the implementation is appropriate, or senior-official acceptance | SDR-CSO-FRR, IVV-CSO-SEI | `frrValidation` (shared) | No separate verification field; no acceptance field |
| 3 | Provider validation that it is in place and working | SDR-CSO-FRR, IVV-CSO-SEE | `frrValidation` | None |
| 4 | Independent verification | SDR-CSO-FRR, IVV-IAS-VIM, IVV-IAS-SUM | `frrAssessment` (free text) | Not structured |
| 5 | Independent validation | SDR-CSO-FRR, IVV-IAS-VEF | `frrAssessment` | Shares a field with 4 |
| 6 | Responses to independent assessment comments | SDR-CSO-FRR | None | Providers add `frrRemarks` |
| 7 | Rule-specific artifacts | SDR-CSO-FRR; rule `artifacts` in the rules dataset | None for FRRs | 60 of 233 non-Rev5 FRR entries list expected artifacts the tool can check against |

### Key Security Indicators (KSI)

| # | Required element | Rule basis | SDR 1.1.1 field | Schema gap |
| --- | --- | --- | --- | --- |
| 1 | Measures and objectives, or the reason and customer risk | SDR-CSX-KSI | `ksiImplementation` | None |
| 2 | Cycle for persistent measures | SDR-CSX-KSI, FRD-PER | None | No field |
| 3 | Verification that the measures demonstrate the KSI | SDR-CSX-KSI | `ksiValidation` | None |
| 4 | Verification that automation is accurate and sufficient | SDR-CSX-KSI, FRC-CSX-VVK | None | `ksiTests` lists tests, not automation adequacy |
| 5 | Validation that measures are accurately produced and working | SDR-CSX-KSI | `ksiTests`, `ksiEvidence` | Required keys can be empty arrays |
| 6 | Historical metrics | SDR-CSX-KMT | None | No field |
| 7 | Independent assessment of all KSIs each year | IVV-CSX-AIA | `ksiAssessment` | Free text |

### Class A variant

Class A replaces elements 4 and 5 with the alternative security framework. Check that the framework assessment completed within the past 12 months (FRC-CLA-ASF), that the required external materials are supplied (FRC-CLA-EAM), and that each entry cites the specific framework control and location with an artifact. FRC-CLA-MFR notes that "see SOC 2 report" is not helpful; the FedRAMP help article on SOC 2 responses says the same.

### Proposed chain states

Each element gets one state. The entry takes the state of its weakest required element for the class.

| State | Meaning |
| --- | --- |
| Absent | Field missing or empty |
| Placeholder | "None.", "N/A", "TBD", or a bare status label |
| Asserted | Narrative claim with no reference |
| Cited | Names an artifact, control, or location that is not supplied |
| Supplied | The cited artifact is present and relevant to the claim |
| Corroborated | An assessor or framework auditor tested it, with method, population, period, and result stated |

## 3. Disposition by force (proposal for approval)

No published rule sets when an issue is a pre-certification action versus post-certification feedback. This table applies the force definitions to the Review Sheet Next Steps (column Q). It needs program-owner approval before the guide or tool uses it.

| Force | Met and documented | Not met, departure documented | Not met or not addressed |
| --- | --- | --- | --- |
| MUST / MUST NOT | OK | Pre-cert action or Internal Escalation | Pre-cert action or Internal Escalation |
| SHOULD / SHOULD NOT | OK | OK, or post-cert feedback if the rationale is weak | Pre-cert action (documentation is required by FRD-SHD) |
| MAY | OK | OK | Post-cert feedback (FRD-MAY asks for an explanation) |

## 4. Class lenses

| Topic | Class A | Class B | Class C |
| --- | --- | --- | --- |
| Basis | Framework assessment within 12 months plus overlay (FRC-CLA-ASF, FRC-CLA-MFR) | All applicable rules | All applicable rules |
| Fresh independent assessment at application | MAY (FRC-APP-FIA) | MUST, within 3 months | MUST, within 3 months |
| Annual independent assessment | Framework expectations (IVV-CSX-AIA) | All KSIs (IVV-CSX-AIA) | All KSIs (IVV-CSX-AIA) |
| CPO overall assessment summary | MAY (CPO-CSO-OSA) | MUST | MUST |
| KSIs | 7 named in FRC-CLA-MFR | 46; KSI-CNA-EIS, KSI-MLA-ALA, KSI-SVC-PRR, KSI-SVC-RUD, KSI-SVC-VCM optional | 46 |
| Automated KSI verification and validation | MAY (FRC-CSX-VVK) | SHOULD, at least 1 method per KSI | MUST, at least 2 methods per KSI |
| KSI historical metrics | MAY (SDR-CSX-KMT) | SHOULD: 30-day and up-to-1-year summaries | MUST: summaries plus daily data and persistent-validation status |
| Package maintenance | SHOULD, every 3 months (CPO-CSX-CPM) | MUST, monthly | MUST, every 2 weeks |
| Quarterly Review | MAY (CCM-QTR-MTG) | SHOULD | MUST |
| Machine-based resource verification and validation | SHOULD, monthly (VDR-TFR-MVX) | MUST, every 7 days | MUST, every 3 days |
| Provider walkthrough and collaborative review (SOP) | No | Yes | Yes |

## 5. Patterns to Design For

These patterns came from reading sample packages. No package or provider is identified, and no package content is reproduced.

1. **Schema-complete, chain-incomplete.** An SDR can carry every required key, including `ksiTests` and `ksiEvidence` as empty arrays, while provider validation is blank and only assessor narratives are filled. A field-presence score rates this highly. The tool checks content, not keys.
2. **Strong Class A citations.** The best Class A entries name the framework control, report pages, auditor test, result, and a trust center link. This is the pattern FRC-CLA-MFR asks for.
3. **Explicit absence.** "None." in an assessment field states that no FedRAMP independent assessment occurred, which Class A allows (FRC-CLA-IVV). It is a placeholder, not a failure.
4. **Named but not linked.** Artifacts are often named in prose with no link or file.
5. **Restated claims.** Review notes that restate the provider's implementation leave the next reviewer nothing to act on. Notes record what the reviewer observed, the gap, and what would close it.

## 6. Review Sheet v1.08 against rules 2026.11.02.01

| # | Finding | Location | Basis | Action |
| --- | --- | --- | --- | --- |
| 1 | Removed rule still listed: FRC-CSX-MOT | Review Sheet rows 99 (B), 286 (C) | Removed in 2026.10.08.01 as duplicative of SDR-CSX-KMT | Remove rows |
| 2 | Class B SDR-CSX-KMT shows MUST | Row 197 | Changed to SHOULD for Class B (`updated` 2026-10-08) | Change force and text |
| 3 | SDR-CSX-KSI missing for Class A | No row | Added to FRC-CLA-MFR (`updated` 2026-10-31; release 2026.11.02.01) | Add row |
| 4 | Class A has no row and no removal record for AFC-CSO-INB, CDS-CSO-PUB, FRC-CSO-PKG, FRC-CSO-JSN, FRC-CSO-POP, or the FRC-CLA rules | No rows | FRC-CLA-MFR; FRC-CLA subset | Add rows, or add a Class A removal record like the "Class B & C Removed" tab |
| 5 | Duplicate KSI-SVC-VRI | Rows 421–422 (C) | None | Remove one |
| 6 | MKT-IIP-DCP and MKT-IIP-DLA kept; MKT-IIP-AGU marked intake-only | Rows 169–170 (B), 310–311 (C) | Initial Implementation listing rules | Confirm intent |
| 7 | Column D paraphrases rule text; 134 of 371 matched B/C rows differ from current statements, including pre-release wording of KSI-SCR-MIT | Column D | Rules dataset is authoritative | Load statements from the rules dataset |

The B/C omissions recorded in the "Class B & C Removed" tab (intake-only and Rev5 rules) are deliberate and are not findings.

## 7. Existing tools

| Tool | Does | Does not |
| --- | --- | --- |
| FedRAMP Document Viewer (`preview.fedramp.gov/JSONViewer`) | Renders 10 FedRAMP JSON document types as readable documents; detects type; loads schemas from `fedramp/schemas` and force from the consolidated rules; shows force and status badges; flags rules not present in the SDR | Validate against schema; apply class applicability; assess evidence; write to the Review Sheet |
| Review Companion (built 2026-11-04) | Guide, SOP and workbook map, class lenses, scorecard, local JSON reader, offline schema validation, F–P export to a workbook copy, notes export | Pin the current rules dataset (it uses a September 14 snapshot plus selected live-page checks); compute an applicable-rule denominator; rate each chain element; use rule-listed artifacts; follow house style |

**Warning: the Review Companion's internal workflow analysis is public.** The guide and an analysis of the draft internal SOP are published on a personal GitHub Pages site. The new build replaces it, so unpublish it (Section 11).

## 8. Proposed guide outline

1. What a review decides, and what it does not (Section 1).
2. Before you start: pin the rules version, class, certification type, and path; confirm controlling file versions.
3. Read the CPO first: identity, scope, third parties, assessor, overall assessment summary.
4. Review one rule: walk the seven FRR elements.
5. Review one KSI: walk the seven KSI elements.
6. Class A: read the framework report, check dates and exceptions, test each citation.
7. Class B and C: read the assessor's method, population, period, and result; check automation counts.
8. Decide by force (Section 3) and write the column O note: observation, requirement, gap, request, closure condition.
9. Package-wide checks: CPO, SDR, and OCR consistency; freshness (FRC-APP-FCP, FRC-APP-FIA); OCR period.
10. Bring it to the Conclave.

Callouts: warning for "do not treat schema-valid as complete"; tip for "start with the CPO"; info for rules-version dates.

## 9. Proposed tool specification

1. Load SDR, CPO, and OCR JSON, the class, and optionally the Review Sheet `.xlsx`. All processing stays in the browser.
2. Pin and display the rules version, schema versions, and file hashes.
3. Validate each file against its schema.
4. Resolve applicable rules and KSIs for the class from the rules dataset (type 20x, Program path). This is the denominator.
5. Check coverage both ways: applicable IDs missing from the SDR, and SDR IDs missing from the sheet.
6. Assign a chain state to each element with deterministic, explainable detectors: placeholder phrases, empty arrays, link and file-name detection, framework citations (for example `CC6.1`, page references), dates.
7. Compare each FRR against its rule-listed `artifacts`.
8. Rate each entry by its weakest required element; show the force beside it.
9. Run package checks: CPO URI match, assessor named in CPO and SDR, framework date within 12 months, package freshness, OCR period.
10. Generate reviewer questions from the failing element.
11. Write suggested I and J values and a draft O note to a copy of the sheet. Never set column N.

The tool never scores security effectiveness, never fails a rule over field naming, and never treats a populated field as proof.

### Required elements by class

Element numbers refer to the tables in Section 2.

| Entry | Class A | Class B | Class C |
| --- | --- | --- | --- |
| FRR | 1–3; 4–5 through the framework assessment (IVV-CSX-AIA) unless optional IV&V was performed (FRC-CLA-IVV); 7 as an artifact or framework citation (FRC-CLA-MFR) | 1–5; 6 when the assessor commented; 7 when the rule lists artifacts | Same as Class B |
| KSI | 1–5 (SDR-CSX-KSI through FRC-CLA-MFR); 2 only for persistent measures; 4 may state that automation is not necessary; 7 through the framework assessment | 1–5 and 7; 4 expects at least 1 automated method (SHOULD); 6 is SHOULD | 1–7; 4 requires at least 2 automated methods (FRC-CSX-VVK) |

### Rollup metrics

The tool reports two counts side by side. The tool count describes the evidence chain. The reviewer count describes the decision. The tool never merges them.

| Tool status | Rule |
| --- | --- |
| Chain complete | Every required element for the class is Supplied or Corroborated |
| Evidence gap | Every required element is present; at least one is only Asserted or Cited |
| Documentation gap | At least one required element is Absent or Placeholder |
| Not adopted, explained | Optional entry (MAY, or a KSI marked **Optional:** for the class) with a stated decision |
| Not adopted, unexplained | Optional entry with no stated decision (FRD-MAY) |
| Missing | Applicable ID not present in the SDR |

Reviewer status comes from Review Sheet column N (OK or Concern) and column Q (Next Steps).

1. Show each count by force (MUST, SHOULD, MAY) and by type (FRR, KSI).
2. For Class C, show the number of KSIs with at least 2 automated methods (column J).
3. Flag two conflicts for a second look: reviewer OK on a MUST entry with a documentation gap, and reviewer Concern with no note in column O.
4. Show no single score. An average hides MUST failures that FRD-MST treats as grounds for denial.

### Build milestones

1. Rules engine: pin the rules release; resolve applicable rules and KSIs, force, and listed artifacts for each class; export the result as JSON.
2. Package intake: load SDR, CPO, and OCR; validate against schemas; check coverage both ways.
3. Evidence chain: element detectors, entry status, rollup.
4. Review Sheet: read columns F–U; write suggested I and J values and a draft O note to a copy.
5. Guide: write to the Section 8 outline and link each step to the tool view.

## 10. Decisions

| # | Decision | Outcome (2026-11-05) |
| --- | --- | --- |
| 1 | Build approach | New build driven by the rules dataset. The existing companion is not the base. |
| 2 | Source and hosting | Public GitHub repository `gillooleyj/fedramp-20x-review`, published with GitHub Pages. Content is not sensitive to FedRAMP; provider packages and package-derived findings never enter the repository. |
| 3 | Audience and approval | Personal use first; Pete approves the chain states and disposition table before team use |
| 4 | Overall score | None. Rollup counts by status (Section 9) |
| 5 | Review Sheet fixes | Vanguard Team Lead (Section 6) |
| 6 | Upstream changes | Data updates automatically; tool logic and guide pages are flagged for a person (Section 13) |

## 11. Next steps

1. Complete the one-time setup in `docs/update-process.md`.
2. Send the Section 6 findings to the Vanguard Team Lead.
3. Build milestones 2–3 (Section 9).
4. Test locally against sample packages; commit only fictional test packages, one per class.
5. Build milestones 4–5.
6. Retire the earlier companion site once the new one is live, so reviewers find one guide.
7. Bring the chain states (Section 2) and disposition table (Section 3) to Pete before team use.

## 12. The assessor's role

Full guide page: `guide/assessor-role.md`.

1. FedRAMP is the final assessor for FedRAMP Certification (FRD-ASR) and one of all necessary assessors (FRD-ANA). FedRAMP Recognized assessors perform assessment activities on behalf of FedRAMP (FRD-FRA).
2. The assessor verifies implementation and validates effectiveness at a technical level (IVV-IAS-VIM, IVV-IAS-VEF), writes a summary per practice for the SDR (IVV-IAS-SUM) and an overall summary with failures and disputes for the CPO (IVV-IAS-OSA), and confirms the provider kept its meaning (IVV-IAS-VIP).
3. A Class A framework auditor (SOC 2 Type II or equivalent) is not a FedRAMP assessor. Class A FedRAMP independent assessment is optional (FRC-CLA-IVV). Classes B and C require an assessment completed within 3 months of application (FRC-APP-FIA).
4. Reviewers check the assessor before the assessment: Recognition (REC-FRP-RAO), advisory separation (REC-IAS-SEP), freshness (FRC-APP-FIA), and coverage of every applicable rule and KSI (IVV-IAS-SUM, IVV-CSX-AIA).
5. When a reviewer disagrees with the assessor, the reviewer's determination governs. Package fixes go to the provider (FRC-CSO-MRA); assessment-quality problems are performance-standards issues (REC-IAS-PST, REC-IAS-CAP) routed through Internal Escalation. The internal workflow does not yet define who handles assessor performance issues.

## 13. Rule-update mechanism

Full process: `docs/update-process.md`.

1. A daily GitHub Action compares FedRAMP/rules, FedRAMP/schemas, and FedRAMP/2026-markdown with `sources.lock.json`.
2. On change, it validates the new rules dataset, diffs it by content (not by `updated` arrays), regenerates `data/rules-extract.json`, and opens one pull request.
3. The pull request lists two checklists: rules whose meaning is coded into the tool (`data/logic-bindings.json`, 42 entries) and guide pages that cite a changed rule or narrative page.
4. Tested against real history: run on the 2026.10.05.01 dataset, it reported every rules change in the 2026.10.08.01 and 2026.11.02.01 changelogs, including the IEC notification changes that have no `updated` entry. It also flagged that the 2026.10.05.01 Class A overlay listed CPO-CSF-CPM, a Rev5-only rule, which FedRAMP removed on October 31.
5. Current dataset conflicts to report upstream: CPO-CSO-OSA, FRC-CSX-VVK, and FRC-CSX-VVR have Class A variants, but no subset or Class A overlay rule applies them to Class A.

Principle: the review tests whether each claim is supported for an agency's decision; the tool shows where the chain breaks and leaves the judgment to the reviewer.
