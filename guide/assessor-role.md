---
tags:
  - FedRAMP
  - Independent Assessors
  - Guidance
  - 20x
audience: FedRAMP reviewers
type: Guidance
reviewed_against: 2026.11.02.01
rules:
  - FRD-ASR
  - FRD-ANA
  - FRD-FRA
  - FRD-IFA
  - FRC-CSO-MRA
  - FRC-CLA-ASF
  - FRC-CLA-EAM
  - FRC-CLA-IVV
  - FRC-APP-FIA
  - FRC-APP-USA
  - FRC-APP-NTP
  - IVV-CSO-FIA
  - IVV-CSX-AIA
  - IVV-CSO-SEI
  - IVV-CSO-SEE
  - IVV-CSO-STE
  - IVV-CSO-ICP
  - IVV-CSO-DUS
  - IVV-IAS-VIM
  - IVV-IAS-VEF
  - IVV-IAS-SUM
  - IVV-IAS-OSA
  - IVV-IAS-VIP
  - IVV-IAS-EPX
  - CPO-CSO-OSA
  - SDR-CSO-FRR
  - REC-FRP-RAO
  - REC-IAS-SEP
  - REC-IAS-PST
  - REC-IAS-CAP
sources:
  - assessors/fedramp-assessments/index.md
  - assessors/fedramp-assessments/20x.md
  - responsibilities/assessors.md
  - responsibilities/fedramp.md
---

# The Assessor's Role in a 20x Review

This page explains who assesses what when FedRAMP reviews a FedRAMP 20x Certification Package, and how to check the independent assessor's work. It's for FedRAMP reviewers working Class A, B, and C reviews.

## Several Parties Assess; FedRAMP Decides

| Party | Role in the review | Basis |
| --- | --- | --- |
| Independent assessment service | Performs the bulk of verification and validation, on behalf of FedRAMP, under contract to the provider. Must be FedRAMP Recognized. | FRD-FRA (FedRAMP Recognized); [Independent Assessment Service Responsibilities](https://www.fedramp.gov/2026/responsibilities/assessors/){ data-preview } |
| FedRAMP | The final assessor for FedRAMP Certification and one of all necessary assessors. Makes the Certification decision. | FRD-ASR (Assessor); FRD-ANA (All Necessary Assessors); FRD-IFA (Initial FedRAMP Assessment) |
| Alternative framework auditor (Class A only) | Issues the SOC 2 Type II report or equivalent that Class A relies on. This is framework evidence, not a FedRAMP independent assessment. | FRC-CLA-ASF (Approved Alternative Security Frameworks); FRC-CLA-EAM (External Assessment Materials) |
| Provider | Remains responsible for the accuracy and completeness of everything in the package, including content an assessor supplied. | FRC-CSO-MRA (Maintain Responsibility and Accountability) |
| Agencies | Decide whether the certified offering fits their use. | [FedRAMP's Responsibilities](https://www.fedramp.gov/2026/responsibilities/fedramp/){ data-preview } |

!!! warning "Do not record a framework auditor as the independent assessor!"
    A SOC 2 report is issued in the auditor role, even when the audit firm is also FedRAMP Recognized. For Class A, a FedRAMP independent assessment is a separate, optional engagement under FRC-CLA-IVV (Optional Independent Verification and Validation).

## What the Assessor Delivers

1. **Verification:** the assessor checks that the measures in place match the measures the provider documented, at a technical level (IVV-IAS-VIM (Verify Implementation)).
2. **Validation:** the assessor checks that those measures produce the intended outcome (IVV-IAS-VEF (Validate Effectiveness)). Both rules note that reviewing documentation or screenshots alone isn't enough.
3. **A summary for each FedRAMP practice,** which the provider places in the Security Decision Record (IVV-IAS-SUM (Assessment Summary)). FedRAMP doesn't require a separate Security Assessment Plan or Security Assessment Report.
4. **An overall summary,** including failures and areas of dispute, which the provider places in the Certification Package Overview (IVV-IAS-OSA (Overall Summary of Assessment); CPO-CSO-OSA (Overall Summary of Assessment in Certification Package)).
5. **Confirmation that the provider didn't change the meaning** of the assessment when adding it to the package (IVV-IAS-VIP (Verify Inclusion in Certification Package); IVV-CSO-ICP (Inclusion in Certification Package)).
6. **Deliverables that meet FedRAMP performance standards:** complete on first submission, clear, correctly formatted, on time, accurately tested, independent, and with chain of custody preserved (REC-IAS-PST (Performance Standards)).

## How the Assessor's Role Changes by Class

| Topic | Class A | Class B | Class C |
| --- | --- | --- | --- |
| Independent assessment at application | Optional (FRC-CLA-IVV); a framework assessment from the past 12 months is required (FRC-CLA-ASF) | Required, completed within the previous 3 months (FRC-APP-FIA) | Required, completed within the previous 3 months (FRC-APP-FIA) |
| Stale assessment | Applies only if optional IV&V was performed | May be refreshed by a change review unless it's more than 9 months old (FRC-APP-USA) | Same as Class B |
| Ongoing assessment | Meets the framework's own expectations (IVV-CSX-AIA) | All applicable rules each year (IVV-CSO-FIA); all KSIs each year (IVV-CSX-AIA) | Same as Class B |
| Overall summary in the CPO | Optional | Required | Required |

## Check the Assessor Before You Read the Assessment

1. **Recognition.** Confirm the assessor named in the CPO (`assessor.name`, `assessor.assessorID`) is listed as FedRAMP Recognized in the FedRAMP Marketplace. FedRAMP can't accept attestations from assessors who aren't Recognized (REC-FRP-RAO (Recognized Assessors Only)).
2. **Independence.** Check the CPO `advisors` list. An assessor can't assess an offering it advised on in the past 2 years (REC-IAS-SEP (Advisory Separation)). The provider, not the assessor, must have applied (FRC-APP-NTP (No Third-Party Applicants)).
3. **Freshness.** For Class B and C, confirm the assessment finished within 3 months of the application (FRC-APP-FIA).
4. **Coverage.** Confirm there's an assessment summary for every applicable rule and KSI. FedRAMP's assessor guidance states that each applicable rule must be assessed.

## Read Each Summary as an Argument

For each rule and KSI, the summary should tell you what was examined and how, what evidence supported the result, what population and period it covered, what counted as failure, where the implementation failed or remains disputed, and what risks matter to a customer.

1. Look for technical testing: queries, configuration data, code review, live demonstrations. A summary built only on policies or screenshots doesn't meet IVV-IAS-VIM.
2. Treat "Pass" as a label, not a finding. Read the method and scope behind it.
3. Separate a sound process that found a real weakness from an unsound process that produced an unreliable answer. The first is useful evidence.
4. Where the assessor sampled, confirm the provider explained the sample (IVV-CSO-DUS (Document Use of Representative Samples)).
5. Keep the assessor's findings and the provider's responses apart. SDR-CSO-FRR (FedRAMP Rules) expects both, recorded separately.

!!! tip "Start with the CPO overall summary"
    It lists failures and disputes in one place. Check that each one appears, with the same meaning, in the matching SDR entry.

## When You Disagree With the Assessor

1. **Your determination governs.** FedRAMP is the final assessor, so an assessor's "Pass" doesn't bind the review.
2. **Record both views.** In the review sheet, note the assessor's conclusion and your basis in column O, then set Next Steps by the rule's force.
3. **Ask for the evidence directly.** Because FedRAMP is one of all necessary assessors, providers must supply evidence of implementation and effectiveness to FedRAMP as well (IVV-CSO-SEI (Supply Evidence of Implementation); IVV-CSO-SEE (Supply Evidence of Effectiveness)), and should supply technical explanations and demonstrations (IVV-CSO-STE (Supply Technical Explanations)).
4. **Send package fixes to the provider.** The provider stays accountable even when the assessor wrote the content (FRC-CSO-MRA).
5. **Raise assessment quality separately.** Missing coverage, no technical testing, or unclear deliverables are performance-standards issues under REC-IAS-PST, and FedRAMP can require a corrective action plan (REC-IAS-CAP (Corrective Action Plan)). Route these through Internal Escalation.

!!! info "Assessor touchpoints for Class B and C"
    The assessor joins the provider walkthrough at the start of the review. Plan for the assessor at the collaborative review when questions turn on how a test was performed.

The assessor's work is evidence you weigh, not a conclusion you inherit.
