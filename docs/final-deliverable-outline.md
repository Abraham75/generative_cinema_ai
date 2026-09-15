# Final Deliverable and Release-Evidence Standard

## Purpose

This document defines how Generative Cinema AI will be evaluated, classified, and presented at each release gate. It is a synthesis standard, not evidence that the product has been implemented. As of this review, the repository is a conceptual Python prototype: its recommendation functions return fixed text, `main.py` imports package paths that are not present, and the README describes files and directories that are absent.

## Approved working interpretation

The following is the **Approved Working Interpretation** for planning and the first implementation increment. It is approved as the team's operative scope, but it is not represented as an unambiguous verbatim user selection or as market validation. It may be revisited through a recorded product decision without rewriting the historical evidence.

- Capability delivery is staged: screenplay intelligence and shot-plan/visual-treatment foundations first; storyboard imagery second; video previsualization third. This is an approved planning interpretation of the user's direction, not a `[Verified]` statement that every sequencing detail was explicitly selected.
- It will serve individual filmmakers, professional production teams, film schools, and studios through role-appropriate workflows.
- Third-party model and media APIs are permitted behind provider-independent interfaces.
- Hosted processing and retention are permitted, subject to explicit privacy, security, consent, retention, and deletion controls.
- The commercial destination is a licensable enterprise platform.
- Wave 1 accepts English-language, digitally born TXT and Fountain input only. FDX, PDF, DOCX, OCR, and multilingual ingestion are later, separately gated adapters.
- The first implementation increment is a narrow internal foundation, not the full Phase 1 product: repair execution/package structure; add versioned domain schemas; ingest TXT/Fountain; produce scene-specific structured recommendations through a deterministic fake/provider interface; validate output; expose human edit/approve behavior; export one machine-readable format; and establish baseline tests, content minimization, and safe configuration.
- No release date has been committed; progression is controlled by evidence-based gates rather than calendar claims.

### Capability phases are not maturity stages

Capability and release maturity are independent axes. A capability phase says **what the system can do**; a maturity stage says **how much evidence exists that it can be used dependably**. Finishing capability code never automatically advances maturity.

| Capability phase | Scope | Initial boundary |
|---|---|---|
| C1 — Screenplay intelligence and planning | Parse, structure, recommend, review, and export shot-plan/visual-treatment data | Wave 1 is TXT/Fountain and a narrow internal vertical slice |
| C2 — Storyboards | Generate and govern images from approved C1 artifacts | Begins only after C1 contracts, rights, quality, and cost gates pass |
| C3 — Video previsualization | Generate and govern clips from approved shots/boards | Begins only after C2 continuity, rights, safety, and unit-economics gates pass |

The maturity labels in the Release classifications section apply separately to C1, C2, and C3. For example, C1 may reach private beta while C2 remains a prototype and C3 remains a concept.

## Evidence traceability

Every decision-driving claim in the final package must carry one of these labels:

| Label | Meaning | Minimum support |
|---|---|---|
| `[Verified]` | Directly demonstrated or supported by an authoritative source | Evidence ID, source/version/date, and reproducible observation or citation |
| `[Inferred]` | Reasoned conclusion from verified evidence | Evidence IDs plus explicit reasoning |
| `[Assumed]` | Working premise used because evidence is missing | Named owner, validation method, and review date/gate |
| `[Opinion]` | Strategic or creative judgment | Decision owner, rationale, and alternatives considered |

### Required evidence record

Each evidence item must record:

| Field | Requirement |
|---|---|
| Evidence ID | Globally unique, namespaced identifier such as `RES-EV-001`, `AUD-EV-001`, `RED-EV-001`, `RED-XR-001`, or `USR-DEC-001` |
| Claim | One atomic proposition |
| Classification | Verified, Inferred, Assumed, or Opinion |
| Source | File/commit/test/source URL/interview identifier |
| Source date and access date | Dates in ISO 8601 format |
| Method | Inspection, automated test, benchmark, interview, or research review |
| Result | Concise finding with units where applicable |
| Confidence | High, Medium, or Low, with rationale |
| Caveat | Known limitation or boundary |
| Owner | Role responsible for maintenance |

Repository claims must identify a commit SHA. Test claims must identify the command, environment, fixture or dataset, and machine-readable result. Market claims must cite current primary sources where available. User-demand claims require interviews, observed behavior, pilots, or usage data; internal preference alone is not demand validation.

Legacy IDs in source artifacts must be interpreted only through an explicit crosswalk and must not be copied into the final package unqualified:

- `research/evidence-register.md` `E-*` becomes `RES-EV-*`.
- `docs/current-state-audit.md` `AUD-*` becomes `AUD-EV-*`.
- `reviews/preimplementation-red-team.md` first-pass `E-*`, Critical/Major/Minor issue IDs, and cross-review `XR-*` become `RED-EV-*`, `RED-C-*`, `RED-M-*`, `RED-m-*`, and `RED-XR-*`, respectively.
- User decisions and approved working interpretations use `USR-DEC-*`; the record must distinguish an explicit answer from an orchestrator interpretation.

The source documents remain historical records. Before final publication, references must either be rewritten to the canonical IDs or resolved through a checked crosswalk with no collisions or dangling references.

### Traceability chain

The final package must preserve this chain:

`evidence ID -> finding -> product or architecture decision -> requirement -> acceptance test -> test result -> release gate`

No capability may appear in product copy unless it maps to an implemented requirement and passing evidence. Unsupported future capabilities must be labeled `planned`, not described in the present tense.

## Release classifications

Release classification is determined by the weakest unmet mandatory criterion, not by aspiration or percentage completion.

| Classification | Permitted meaning | Mandatory evidence |
|---|---|---|
| Concept | Product thesis and proposed workflows only | Problem statement, assumptions, and research plan |
| Prototype | Demonstrates selected technical or UX ideas; not dependable for real work | Reproducible demo, known limitations, and no production claim |
| MVP | End-to-end workflow delivers a narrow user outcome to pilot users | Real screenplay input, scene-specific structured output, editing/approval, export, tests, privacy disclosure, and pilot acceptance criteria |
| Private beta | Limited external use under controlled support and monitoring | Auth, tenant isolation, error handling, telemetry, backups, incident path, documented support limits, and resolved Critical findings |
| Enterprise pilot | Contract-bound use by a named organization in a scoped environment | SSO/RBAC as required, tenant/data controls, DPA and vendor review, audit events, service objectives, admin controls, and pilot success metrics |
| Production-ready enterprise release | Supported commercial service suitable for licensed deployment within its documented boundaries | Security review, operational readiness, disaster recovery evidence, tested upgrades/rollback, accessibility target, compliance mapping, support/SLA process, cost/capacity evidence, and no unaccepted release-blocking risks |

Passing functional tests alone does not establish enterprise readiness. Storyboard or video-provider integration does not establish creative quality, rights clearance, reliability, or commercial fitness.

**Current classification:** Concept demonstrator. The repository records intended modules and a hard-coded demonstration, but it is not presently a reproducibly runnable prototype under its documented structure. The approved working interpretation authorizes a narrow foundation increment; it does not advance the maturity classification.

## Final package criteria

The Editor may issue a decision-ready final package only when the following artifacts exist, are internally consistent, and identify their evidence status.

### 1. Executive decision brief

- Objective, approved audience, and commercial model
- Current release classification and evidence for it
- Recommended decision: proceed, proceed with conditions, pause, or stop
- Material disagreements and unresolved risks
- Next funded milestone and its exit criteria

### 2. Product definition

- Reconciled PRD with long-term persona-specific workflows for individual filmmakers, production teams, film schools, and studios, while identifying launch audiences as unvalidated
- Separate capability roadmap (C1–C3) and maturity path, with no use of “Phase 1 MVP” as a combined label
- Wave-1 boundary limited to TXT/Fountain and the narrow internal foundation; other input adapters remain separately gated
- Measurable user outcomes, KPIs, pilot criteria, and out-of-scope items
- Accessibility and human creative-control requirements

### 3. Evidence and research appendix

- Evidence register in the required schema
- Competitor, workflow, provider, privacy, and licensing findings; dated pricing and unit-cost evidence is required only for providers shortlisted for paid beta
- Clear separation of verified demand from hypotheses
- Source dates and caveats for time-sensitive claims

### 4. Technical package

- Reproducible current-state audit tied to a commit SHA
- Target architecture and accepted architecture decision records
- Versioned screenplay, scene, beat, shot, recommendation, provenance, and export schemas
- Provider-independent interfaces for text, image, and video services
- Threat model, data-flow diagram, tenant isolation design, retention/deletion model, and vendor-risk inventory
- API specification, deployment/runbook material, migration/rollback approach, and cost model

### 5. Implementation evidence

- End-to-end runnable product for the declared release scope
- Automated unit, integration, contract, security, and representative workflow tests
- Evaluation corpus with permission/provenance records
- Quality evaluation covering relevance, consistency, controllability, explanation quality, and creative-professional review
- Test commands, environment, results, limitations, and failure cases
- CI evidence and dependency/security scan results

### 6. User and commercial package

- Accurate README, onboarding, interface copy, demonstration, and sample exports
- Enterprise packaging assumptions, licensing boundaries, support model, and procurement/security materials appropriate to the release class
- Privacy notice, acceptable-use boundaries, model/provider disclosure, and content-rights responsibilities
- No marketing claim broader than verified product behavior

### 7. Assurance package

- Red-team report with Critical/Major/Minor severities and proposed fixes
- Issue dispositions and residual-risk acceptances
- Release-gate checklist signed by accountable owners
- Final change log
- “What remains uncertain” section

## Change-log format

The change log must be append-only for review cycles and use this format:

| Change ID | Date | Issue raised | Evidence ID(s) | Severity | Agent/owner | Correction made | Verification performed | Residual risk | Status |
|---|---|---|---|---|---|---|---|---|---|
| `CHG-001` | YYYY-MM-DD | Concise issue statement | `TECH-EV-001` | Critical/Major/Minor | Role or named owner | Exact artifact/change | Test or review evidence | Remaining limitation | Open/Fixed/Accepted/Deferred |

Rules:

- `Fixed` requires independent verification, not only an author assertion.
- `Accepted` requires a named risk owner and rationale.
- `Deferred` requires a target milestone and must not conceal a release blocker.
- Changes to scope, architecture, privacy posture, or product claims require a linked decision record.

## Disagreements that must be preserved

The final synthesis must retain meaningful disagreement rather than averaging it away. At minimum, it must explicitly resolve or preserve:

1. **Breadth versus focus:** one platform for all four customer groups versus a narrow first workflow and beachhead buyer.
2. **Product scope:** analysis and shot planning first versus early storyboard and video generation.
3. **Creative authority:** deterministic film-language rules versus model-generated suggestions and how users override both.
4. **Enterprise ambition versus evidence:** intended licensable platform versus the maturity actually demonstrated.
5. **Cloud convenience versus screenplay confidentiality:** hosted third-party processing versus local/private or zero-retention options.
6. **Provider flexibility versus operational complexity:** multi-provider abstraction versus a smaller validated provider set.
7. **Standardization versus artistic diversity:** consistency and evaluability versus avoiding prescriptive claims about a single “correct” cinematic treatment.
8. **Commercial protection versus open-source posture:** repository openness, intellectual property, model licenses, customer data rights, and enterprise licensing.

For each disagreement, record the competing positions, evidence, decision owner, chosen position, rationale, dissent or caveat, and revisit trigger.

## Final synthesis order

The final decision-ready report must use this sequence:

1. Executive summary
2. Objective and scope
3. Current release classification
4. Key verified findings
5. Analysis and options
6. Recommendation and proposed solution
7. Implementation plan and release gates
8. Risks, assumptions, disagreements, and unresolved questions
9. Evidence appendix
10. Change log

## Publication gate

The Editor must not approve publication or describe the platform as an MVP, beta, enterprise pilot, or production-ready unless all mandatory evidence for that class is present. If evidence is incomplete, the package must use the lower defensible classification and enumerate the exact missing criteria. Any legal conclusion concerning copyright, privacy, contractual terms, training rights, or generated-media ownership must be marked for qualified counsel rather than presented as settled fact.

## Uncertainties intentionally left open

- Initial design-partner segment and willingness to pay; all four stated audiences are addressable, not validated launch markets.
- Provider shortlist, current prices, contractual retention/training terms, semantic portability, and acceptable unit economics.
- Cinematic-quality rubric, rights-cleared evaluation corpus, reviewer panel, agreement method, and release thresholds.
- Data-class lifecycle, deletion verification, backup expiry, legal-hold precedence, and provider-side erasure limits.
- Copyright, contractual allocation, likeness/voice/reference rights, disputes, takedown process, education/student obligations, and jurisdiction-specific requirements; qualified counsel review remains mandatory.
- Studio pilot identity/governance requirements, deployment regions, residency, private deployment, SLOs, support levels, and compliance targets.
