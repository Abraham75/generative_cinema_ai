# Generative Cinema AI — Product Requirements Document

**Status:** Draft for product and architecture approval  
**Product class:** Licensable enterprise creative-intelligence platform  
**Target date:** Not set  
**Release strategy:** Phase 1 shot planning; Phase 2 storyboards; Phase 3 video generation

## 1. Executive Summary

Generative Cinema AI will convert screenplay material into editable, explainable cinematic planning artifacts. The first release will focus on screenplay analysis and shot-plan generation. Storyboard images and generated video clips will be introduced only after the shot-planning workflow reaches defined quality, reliability, security, and user-adoption gates.

The product will serve individual filmmakers, production teams, film schools, and studios through one configurable platform rather than four unrelated products. A common screenplay-to-scene-to-shot data model will support audience-specific workspaces, permissions, workflows, and licensing tiers. Third-party AI APIs are permitted, but provider abstractions, data-processing controls, provenance, and customer-configurable retention are required for enterprise viability. **[Inferred: E-09, E-15, E-16]**

## 2. Evidence Status and Decision Basis

This PRD uses the following labels:

- **[Verified]** Directly supported by the inspected repository or explicit user decision.
- **[Inferred]** Reasoned from verified inputs.
- **[Assumed]** A working premise pending validation.
- **[Opinion]** A strategic recommendation or creative judgment.

### 2.1 Verified inputs

- **[Verified]** The current repository contains a README and seven Python files: an orchestrator, a basic file reader, and five cinematic recommendation modules. **[AUD-003, AUD-006]**
- **[Verified]** The current frame, lighting/color, lens, camera-movement, and texture functions return hard-coded text independent of screenplay content. **[AUD-003]**
- **[Verified]** `main.py` imports `modules.*` and `utils.*`, but the inspected files are not organized in those directories. **[AUD-001]**
- **[Verified]** The README describes `sample_script.txt`, `requirements.txt`, `LICENSE`, `modules/`, and `utils/`; these are absent from the inspected repository state. **[AUD-002, AUD-004, AUD-012]**
- **[Verified]** The user approved an initial shot-planning outcome, followed by storyboard and video capabilities.
- **[Verified]** The user requires the platform to support individual filmmakers, production teams, film schools, and studios.
- **[Verified]** The product may use paid third-party APIs.
- **[Verified]** Hosted processing and retention of uploaded scripts are permitted.
- **[Verified]** The intended commercial form is a licensable enterprise platform with no target release date.

### 2.2 Working interpretation

- **[Inferred]** The repository is a concept prototype, not a deployable product. **[AUD-001–AUD-012]**
- **[Inferred]** A shared core engine with role- and organization-specific experiences is more maintainable than four separate products. This remains a design judgment rather than an externally verified fact.
- **[Assumed]** “Yes” to hosted retention does not mean unlimited retention or permission to train third-party models on customer content.
- **[Assumed]** English-language, digitally born screenplay text is the initial input; OCR and multilingual support are later capabilities.
- **[Opinion]** The defensible product wedge is an auditable screenplay-to-shot-plan workflow, not a claim of autonomous direction or universal creative correctness. **[E-14, E-15]**

## 3. Objective and Scope

### 3.1 Product objective

Enable users to transform screenplay text into coherent, editable, production-useful visual plans while retaining human creative authority and traceability from each recommendation to its source scene, narrative evidence, assumptions, and generation settings.

### 3.2 Phase strategy

| Phase | Product outcome | Included | Entry gate | Exit gate |
|---|---|---|---|---|
| 1 — Shot Planning | Structured screenplay analysis and editable shot plans | Script ingestion, scene/beat extraction, shot suggestions, rationale, collaboration, exports | Approved domain model and privacy design | Acceptance criteria in Section 10 pass |
| 2 — Storyboards | Visual boards grounded in approved shots | Reference management, image generation, continuity controls, annotations, versioning | Stable Phase 1 shot schema and human approval workflow | Visual consistency, rights, cost, and review thresholds pass |
| 3 — Video | Short clips generated from approved boards/shots | Provider routing, clip generation, provenance, iteration, assembly handoff | Stable storyboard identity/continuity controls | Quality, safety, cost, rights, and operational thresholds pass |

### 3.3 Explicitly out of Phase 1

- Finished-film generation
- Unsupervised final creative decisions
- Guaranteed production feasibility or artistic quality
- Automated rights clearance
- Full scheduling, budgeting, casting, or production-management replacement
- Model training on customer scripts without a separate, explicit agreement

## 4. Personas and Jobs to Be Done

| Persona | Primary job | Key needs | Phase 1 value |
|---|---|---|---|
| Individual filmmaker / writer-director | Turn a script into a visual plan quickly | Guided workflow, affordable usage, templates, editable exports | Accelerated first-pass shot planning and treatment creation |
| Production team | Coordinate director, DP, producer, and department decisions | Shared projects, comments, approvals, roles, version history | A common scene/shot record and review workflow |
| Film educator / student | Teach and practice visual storytelling | Assignments, exemplars, instructor review, explainability | Rationale-linked shot alternatives and assessable revisions |
| Studio / enterprise administrator | Govern creative AI across projects and teams | SSO, RBAC, audit, retention, vendor controls, usage reporting | Controlled tenant-wide deployment and oversight |
| Director / cinematographer | Develop an intentional visual language | Lens, framing, movement, lighting, continuity, alternatives | Editable recommendations with evidence and rationale |
| Producer / production executive | Review feasibility and alignment | Status, approvals, exports, risk visibility | Reviewable plans rather than opaque prose outputs |

**[Assumed]** Personas and jobs require direct user interviews and workflow observation before being treated as validated demand.

## 5. Product Principles

1. **Human authorship:** Users approve, reject, edit, lock, and override all material recommendations.
2. **Explainability:** A recommendation includes rationale and the screenplay evidence that informed it.
3. **Structured before generative:** Validated domain objects are the system of record; prose is a presentation layer.
4. **Provider independence:** Business logic and customer data are not bound to a single model vendor.
5. **Progressive generation:** Text plans precede images; approved images precede video.
6. **Enterprise control:** Identity, tenancy, policy, audit, retention, and export are foundational, not post-launch additions.
7. **Creative plurality:** The system offers alternatives and tradeoffs instead of presenting one “correct” cinematic answer.

## 6. Functional Requirements

### 6.1 Ingestion and project management

- **FR-001:** Create a project within a personal or organizational workspace.
- **FR-002:** Import screenplay text and supported document formats defined during technical design.
- **FR-003:** Record file identity, version, ownership, upload time, processing status, and retention policy.
- **FR-004:** Preserve the original source and create immutable script versions.
- **FR-005:** Detect unsupported, malformed, oversized, or encrypted inputs and return actionable errors.

### 6.2 Screenplay understanding

- **FR-010:** Segment a script into scenes with stable scene identifiers.
- **FR-011:** Extract headings, locations, time-of-day indicators, characters, dialogue, action, and transitions where present.
- **FR-012:** Identify candidate narrative beats and emotional/tension attributes while marking model inference.
- **FR-013:** Associate every extracted or inferred element with source spans and confidence/status metadata.
- **FR-014:** Let users correct scene boundaries, entities, and inferred beats before generation.

**Evidence basis:** Screenplays contain typed structural elements, and FDX and Fountain are materially relevant but different input formats; parsing must preserve source order and unknown content rather than treating a screenplay as undifferentiated prose. **[E-01–E-03; AUD-006]**

### 6.3 Shot-plan generation

- **FR-020:** Generate one or more shot-plan alternatives per selected scene.
- **FR-021:** Represent each shot with stable ID, subject/action, framing, angle, lens/focal-length suggestion, movement, lighting, color, texture, duration estimate, transition, rationale, and source references.
- **FR-022:** Validate generated output against a versioned schema and reject or repair invalid responses.
- **FR-023:** Allow regeneration at scene, beat, shot, or attribute level without overwriting approved work.
- **FR-024:** Allow users to edit, reorder, duplicate, lock, approve, reject, and annotate shots.
- **FR-025:** Present alternatives and their creative/production tradeoffs.
- **FR-026:** Maintain visual-language constraints across a project, including user-defined rules and locked choices.
- **FR-027:** Save model/provider, prompt/template version, parameter summary, generation time, and provenance for generated artifacts.

**Evidence basis:** Schema-constrained model output is available, but schema adherence does not establish semantic or creative correctness; domain validation and human review remain necessary. **[E-04; AUD-005, AUD-007, AUD-008]**

### 6.4 Collaboration and workflow

- **FR-030:** Support workspace roles at minimum: owner, administrator, editor, reviewer, and viewer.
- **FR-031:** Support comments, mentions, review status, and approval history on scenes and shots.
- **FR-032:** Provide version comparison and restoration for user and AI changes.
- **FR-033:** Permit organization-defined approval gates before storyboard or video generation.

**Evidence basis:** Collaboration, versioning, approvals, storyboards, and shot lists already appear in adjacent commercial offerings; these are category expectations, not evidence that this implementation is competitive or that customers will buy it. **[E-12–E-14]**

### 6.5 Export and interoperability

- **FR-040:** Export an approved shot list in human-readable and machine-readable formats.
- **FR-041:** Export a visual-treatment document organized by project and scene.
- **FR-042:** Include artifact IDs, script version, approval status, and provenance in exports where applicable.
- **FR-043:** Provide a versioned API for enterprise integration.
- **FR-044:** Define later connectors only after target production-system requirements are validated.

### 6.6 Administration and governance

- **FR-050:** Provide tenant configuration for providers, retention, deletion, regional processing where supported, and content-policy settings.
- **FR-051:** Provide usage, cost, latency, failure, and model/provider reporting.
- **FR-052:** Provide searchable audit events for access, generation, editing, approval, export, and deletion.
- **FR-053:** Support configurable data deletion and an auditable deletion outcome.
- **FR-054:** Prevent customer content from being used for product/model training unless separately and explicitly opted in under appropriate terms.

### 6.7 Phase 2 requirements: storyboards

- Generate storyboard images only from an approved shot or scene plan.
- Preserve links among script version, scene, shot, prompt, references, provider, and generated image.
- Support reference assets, style constraints, character/location continuity, variants, annotations, approvals, and regeneration.
- Expose provider-specific limits, cost, and policy outcomes without corrupting the provider-neutral domain model.

**Evidence basis:** Current image APIs support generation and editing from text and image inputs, but capabilities, costs, and limits are provider-controlled and change over time. **[E-05]**

### 6.8 Phase 3 requirements: video

- Generate clips only from approved shots or boards under organization policy.
- Preserve clip provenance, input artifacts, provider settings, rights declarations, and generation history.
- Support retries, variants, continuity review, approval, and export to downstream editing workflows.
- Require explicit controls for identity/reference use, sensitive content, and provider-specific restrictions.

**Evidence basis:** Current video APIs use asynchronous job lifecycles and expose provider-specific conditioning, limits, and commercial terms; those vendor claims do not establish output quality. **[E-06–E-08]**

## 7. Conceptual Domain Model

| Entity | Purpose | Essential relationships |
|---|---|---|
| Tenant / Workspace | Isolation, licensing, policy, identity | Owns users, projects, policies, usage |
| Project | Creative and administrative container | Contains scripts, visual bible, scenes, exports |
| ScriptVersion | Immutable screenplay state | Source for scenes and generated artifacts |
| Scene | Structured screenplay unit | Contains beats and shots; cites source spans |
| Beat | Narrative/action/emotional unit | Informs one or more shots |
| VisualBible | Project-wide visual constraints | Governs shot, storyboard, and video generations |
| ShotPlanVersion | Reviewable plan state | Contains ordered shots and approvals |
| Shot | Atomic cinematic proposal | References scene/beat and later boards/clips |
| GenerationRun | Reproducibility/provenance record | Captures model, template, parameters, cost, status |
| Review / Approval | Human decision record | Applies to plans, shots, images, and clips |
| StoryboardAsset | Phase 2 visual artifact | Derived from approved shot |
| VideoAsset | Phase 3 moving-image artifact | Derived from approved shot/board |
| AuditEvent | Governance record | Captures security and workflow events |

## 8. Nonfunctional Requirements

Exact numerical service levels remain **[Assumed]** until deployment model, provider contracts, and customer tier are selected.

| Area | Requirement |
|---|---|
| Security | Encryption in transit and at rest; tenant isolation; least privilege; secrets management; dependency and image scanning |
| Identity | Enterprise-ready OIDC/SAML path, MFA compatibility, RBAC, and lifecycle provisioning path |
| Privacy | Declared subprocessors; configurable retention/deletion; data minimization; contractually verified training-use controls; export and deletion controls **[E-09, E-16]** |
| Reliability | Idempotent jobs, retry policies, resumable long-running operations, durable status, and provider-failure handling **[E-06, E-07]** |
| Performance | Asynchronous processing with visible progress; target latency defined per workflow and provider before beta |
| Scalability | Stateless API tier and queued workers; tenant quotas and backpressure; independently scalable generation workloads |
| Portability | Provider adapters and versioned internal schemas; avoid leaking vendor response objects into domain records **[E-05–E-08, E-15]** |
| Observability | Structured logs, traces, metrics, correlation IDs, per-run cost/latency, error classification, and alerting |
| Accessibility | Target WCAG 2.2 AA for primary web workflows **[Assumed]** |
| Maintainability | Typed interfaces, migrations, automated tests, documented ADRs, code ownership, and supported upgrade paths |
| Auditability | Immutable or tamper-evident audit records for material actions and full generation provenance |
| Data integrity | Immutable source versions, optimistic concurrency, explicit artifact status, validated structured outputs |
| Disaster recovery | Backup, restore testing, recovery objectives, and incident procedures set before enterprise GA |
| Internationalization | Data model must not block future languages; initial parsing quality may be English-only **[Assumed]** |

## 9. Options and Tradeoffs

### 9.1 Recommended product sequence

| Option | Advantages | Tradeoffs | Decision |
|---|---|---|---|
| Build shot plans first | Establishes reusable structure, lower media cost, easier review and evaluation | Less visually impressive than immediate video | **Recommended [Opinion; E-14, E-15]** |
| Begin with storyboards | Strong demo value and rapid creative feedback | Identity/style consistency, rights, cost, and evaluation are harder | Phase 2 |
| Begin with video | Highest apparent novelty | Highest cost, latency, policy, continuity, vendor, and quality risk | Defer to Phase 3 |

### 9.2 Platform breadth

| Option | Advantages | Tradeoffs | Decision |
|---|---|---|---|
| Separate product per segment | Highly tailored experiences | Duplicated product/engineering effort and fragmented data | Reject initially |
| One identical UI for all | Simplest delivery | Poor fit for education and enterprise governance | Reject |
| Shared core with configurable experiences | Common engine with segment-specific workflow and controls | Requires careful entitlement and configuration design | **Recommended [Opinion]** |

### 9.3 Model strategy

| Option | Advantages | Tradeoffs | Decision |
|---|---|---|---|
| Single third-party provider | Fastest implementation | Lock-in and weak resilience | Accept only for an early internal spike |
| Provider abstraction with initial default | Balanced speed and portability | Additional interface and evaluation work | **Recommended [Opinion; E-05–E-08, E-15]** |
| Fully self-hosted models initially | Maximum deployment control | Greater infrastructure and quality burden | Optional enterprise path, not default **[E-08]** |

### 9.4 Creative generation strategy

- **[Opinion]** Use a hybrid system: deterministic parsing/validation where reliable, model-assisted inference where ambiguity is inherent, and human approval for creative decisions.
- **[Opinion]** Retrieval or rules may encode filmmaking vocabulary and organizational style guides, but should not masquerade as universal artistic law.
- **[Opinion]** Rank or present diverse alternatives instead of optimizing toward a single opaque “best shot.”

## 10. Phase 1 MVP Acceptance Criteria

Release requires all mandatory criteria below. Numeric quality thresholds are provisional **[Assumed]** and must be calibrated against a reviewed evaluation set.

### 10.1 Functional acceptance

1. A user can create a project, upload a supported screenplay, and see processing state and actionable failures.
2. The system creates stable, editable scenes and preserves source references.
3. A user can correct scene analysis before generation.
4. A user can generate at least two meaningfully differentiated shot-plan alternatives for a selected scene.
5. Each shot contains all required schema fields or an explicit `unknown/not_applicable` state.
6. Each model-generated recommendation includes rationale, source linkage, and generation provenance.
7. A user can edit, reorder, lock, approve, reject, comment on, and version shots without destroying previous versions.
8. Regenerating one scope does not overwrite locked or approved fields outside that scope.
9. Approved plans export successfully in at least one human-readable and one machine-readable format.
10. Workspace roles prevent unauthorized editing, administration, export, and deletion.

### 10.2 Quality and safety acceptance

- 100% of stored model outputs pass the versioned schema or are routed to a visible failure state.
- 100% of generated artifacts record provider/model, template version, source version, time, and run status.
- No known cross-tenant data access defect remains open.
- No Critical security, privacy, data-loss, or rights issue remains open.
- A representative evaluation suite includes varied screenplay structures, ambiguity, malformed inputs, model refusal/failure, concurrency, and provider timeout cases.
- Human reviewers score usefulness, screenplay grounding, internal coherence, editability, and creative diversity using a documented rubric; launch thresholds are approved before external beta.
- Users can delete eligible project data and administrators can verify deletion status under the defined policy.

### 10.3 Operational acceptance

- Documented local and hosted deployment procedures succeed in a clean environment.
- Automated unit, contract, integration, authorization, migration, and end-to-end tests run in CI.
- Service-level indicators cover availability, latency, job failures, provider failures, token/media usage, and cost.
- Quotas, timeouts, retries, cancellation, idempotency, and provider circuit-breaking behavior are tested.
- Backup and restore are tested before an enterprise production designation.

## 11. KPIs and Measurement Plan

Baselines and targets are not yet known. The MVP must instrument the following before pilot use.

### 11.1 North-star candidate

**[Opinion]** Approved, export-ready scenes per active project, paired with a human usefulness threshold. This measures completed creative planning rather than raw generation volume.

### 11.2 Product KPIs

| KPI | Definition | Why it matters |
|---|---|---|
| Time to first useful plan | Time from successful import to first shot plan marked useful or approved | Measures workflow acceleration |
| Scene completion rate | Imported scenes reaching approved/export-ready state | Measures realized value |
| First-pass usefulness | Generated alternatives accepted with minor or no edits under rubric | Measures recommendation utility |
| Edit distance / revision burden | Degree of user change before approval | Diagnoses quality without treating edits as failure |
| Rationale usefulness | Reviewer score for clarity and screenplay grounding | Measures explainability |
| Alternative diversity | Reviewer-scored meaningful variation without contradiction | Guards against superficial variants |
| Collaboration cycle time | Time from review request to resolved approval | Measures team workflow value |
| Export completion | Successful exports divided by initiated exports | Measures final-mile reliability |
| Retained active projects | Projects with meaningful activity across defined periods | Measures sustained adoption; period to be selected |

### 11.3 Enterprise and operational KPIs

- Active licensed seats and meaningful weekly active seats
- Pilot-to-contract conversion and workspace expansion **[Assumed commercial metrics]**
- Per-project and per-approved-scene model cost
- Generation latency percentiles and queue time
- Provider failure, retry, and fallback rates
- Schema-validation and repair rates
- Availability and job completion rate
- Support incidents by severity
- Security/privacy incidents and deletion-request completion
- Audit/export success and policy violations

### 11.4 Evaluation design

- Create a versioned, rights-cleared screenplay test corpus spanning genre, scene length, dialogue/action balance, location complexity, and formatting variance.
- Use blinded human review where practical; include filmmakers, production practitioners, educators, and studio stakeholders.
- Score grounding, cinematic coherence, production usefulness, diversity, editability, and harmful or unsupported inference separately.
- Maintain regression tests for fixed inputs while allowing nondeterministic creative variation.
- Compare provider/model versions under the same schema, rubric, cost, and latency measures.

## 12. Enterprise Licensing and Packaging

### 12.1 Recommended packaging

**[Opinion]** Use a multi-tenant core with contractual and technical options for dedicated infrastructure or customer-controlled model endpoints.

| Package | Intended buyer | Candidate capabilities |
|---|---|---|
| Individual | Filmmakers and students | Personal projects, core shot planning, limited generation/export |
| Team / Education | Production teams and film schools | Shared workspaces, assignments/reviews, collaboration, pooled usage |
| Enterprise / Studio | Studios and institutional customers | SSO/RBAC, audit, policy, retention, provider controls, API, reporting, support and deployment options |

Pricing, quotas, service levels, and contractual commitments remain **[Assumed/TBD]** pending cost modeling and buyer discovery.

### 12.2 Licensing requirements

- Seat, workspace, usage, or hybrid entitlements configurable without branching the codebase.
- Metering at tenant, project, user, provider, model, and media-generation levels.
- Contract-defined retention, deletion, support, availability, and incident obligations.
- Clear ownership and permitted-use terms for customer inputs, generated metadata, images, and clips.
- Subprocessor and provider disclosure, including whether providers retain data or use it for training.
- API versioning, rate limits, usage reporting, and support boundaries.
- Procurement artifacts and security documentation before enterprise general availability.
- Optional dedicated tenant, region, encryption-key, or customer-model endpoint should be evaluated based on validated buyer requirements, not promised in advance.

### 12.3 Intellectual-property and legal review

**[Assumed]** Qualified counsel must review platform terms, third-party provider terms, generated-output rights, likeness/reference use, copyright claims, confidentiality, education-specific requirements, and customer indemnity expectations before commercial release. U.S. Copyright Office guidance emphasizes human-authored expression and fact-specific human control, but does not resolve contractual allocation, publicity rights, or other jurisdictions. **[E-11]** This PRD does not make a legal determination.

## 13. Dependencies

- Approved product positioning and terminology
- Versioned screenplay/scene/beat/shot schemas
- Third-party model/provider selection and data-processing terms
- Authentication, tenant isolation, object storage, database, and job infrastructure
- Rights-cleared evaluation content and qualified reviewers
- Export-format decisions
- Security, privacy, legal, and enterprise procurement review
- UX validation with each primary audience segment

## 14. Risks and Mitigations

| Risk | Priority | Mitigation |
|---|---|---|
| Recommendations are generic or weakly grounded | Critical | Source-linked schema, evaluation corpus, human rubric, alternatives, editable workflow |
| Confidential screenplay exposure | Critical | Encryption, tenant isolation, retention policy, provider controls, audit, no-training default |
| Cross-tenant authorization defect | Critical | Central authorization, negative tests, isolation review, security testing |
| Product claims exceed actual capability | Major | Evidence labels, feature-to-test traceability, marketing review **[AUD-003, AUD-005]** |
| Model/provider lock-in | Major | Internal schemas, provider adapters, evaluation harness, fallback policy **[E-05–E-08, E-15]** |
| Media-generation cost becomes uneconomic | Major | Phase gates, quotas, metering, cost budgets, provider routing |
| Visual/character continuity fails | Major | Approved reference records, identity constraints, continuity review before video |
| “All audiences” dilutes UX | Major | Shared core plus configurable workflows; segment-specific discovery and pilots |
| Creative homogenization or bias | Major | Diverse alternatives, user-defined visual bible, transparent inference, diverse evaluation |
| Generated artifacts create rights disputes | Major | Provenance, declarations, provider-term review, customer controls, counsel review |

## 15. Delivery Plan Without a Fixed Date

Progress will be governed by exit criteria rather than calendar commitments.

1. **Discovery gate:** Interview and observe representatives from all four audience groups; confirm prioritized jobs and buying process.
2. **Foundation gate:** Repair repository execution, establish package structure, schemas, tests, CI, security baseline, and provider contract.
3. **Internal alpha:** Deliver end-to-end screenplay ingestion, analysis, shot-plan alternatives, editing, and export.
4. **Design-partner pilot:** Run controlled pilots across at least the individual/team and institutional segments; measure defined KPIs.
5. **Enterprise beta:** Add collaboration, tenancy, identity, audit, policy, support, and deployment controls.
6. **Phase 2 decision:** Proceed with storyboards only if Phase 1 quality, adoption, cost, privacy, and operational gates pass.
7. **Phase 3 decision:** Proceed with video only if storyboard continuity, rights, safety, cost, and provider resilience gates pass.

## 16. Open Decisions

1. Which screenplay formats are mandatory at first release?
2. Which export formats and production-system integrations are required?
3. Which third-party model providers satisfy quality, cost, privacy, and contractual requirements?
4. Which deployment regions and data-residency commitments are required?
5. What retention defaults and deletion windows should apply by customer tier?
6. What are the approved quality, latency, availability, and cost thresholds?
7. What is the initial pricing metric: seat, project, usage, or hybrid?
8. Which segment supplies the first design partners, despite all segments being supported?

## 17. What Remains Uncertain

- Demand and workflow fit have not yet been validated through primary customer research.
- The evidence register supports category-overlap and vendor-capability claims, but it provides no market-size or willingness-to-pay evidence; competitor capabilities have not been independently benchmarked. **[E-12–E-15]**
- Third-party providers, costs, data terms, and service levels have not been selected.
- Required screenplay and export formats are not yet defined.
- Human-evaluation thresholds and evaluation-corpus composition are not yet approved.
- Enterprise deployment, regional, compliance, and contractual requirements vary by buyer and remain undefined.
- The repository state verifies the prototype gap but not the effort required for a production implementation.

## 18. Evidence Mapping

| PRD decision or requirement | Evidence / audit IDs | Reconciliation and residual uncertainty |
|---|---|---|
| Treat structured screenplay parsing as foundational | E-01–E-03; AUD-006, AUD-007 | FDX and Fountain are relevant; exact MVP formats and round-trip fidelity remain open. |
| Replace fixed strings with grounded, typed recommendations | AUD-003, AUD-005, AUD-007 | The implementation gap is verified; recommendation quality thresholds still require human validation. |
| Use schema-constrained outputs plus validation | E-04; AUD-007, AUD-008 | Structural validity is achievable; it must not be represented as semantic or creative correctness. |
| Preserve the phased shot plan → storyboard → video direction | E-05–E-08, E-14, E-15 | Third-party capability exists; provider claims do not prove quality, affordability, continuity, or demand. |
| Build collaboration, approval, versioning, and export into the professional workflow | E-12–E-14; AUD-010 | Category overlap supports baseline expectations; specific integrations and customer willingness to pay remain unverified. |
| Make provider abstraction and provenance architectural boundaries | E-05–E-10, E-15; AUD-005, AUD-011 | Supported by changing provider capabilities and governance needs; exact providers and contractual terms remain undecided. |
| Treat encrypted storage as only one part of enterprise privacy | E-09, E-10, E-16; AUD-009 | “No training” and “no retention” are not equivalent; each endpoint and contract requires review. |
| Preserve human approval and obtain legal review | E-11; AUD-011 | U.S. copyright guidance supports human-control emphasis but does not settle ownership or other legal regimes. |
| Classify the current repository as concept-only | AUD-001–AUD-012 | Strong audit support; implementation effort and commercial viability are not established by the audit. |
