# Generative Cinema AI — Product Narrative

## Product vision

Generative Cinema AI is intended to become a licensable enterprise platform that helps creative teams translate screenplay language into an editable visual-production plan. It is designed for individual filmmakers, professional production teams, film schools, and studios, with workflows that can scale from a single creator exploring a scene to an organization governing multiple projects and collaborators.

The platform vision is staged deliberately:

1. **Screenplay intelligence:** analyze screenplay material and organize it into scenes, characters, locations, actions, emotional beats, and narrative transitions. [PLANNED]
2. **Cinematic planning:** propose editable framing, lighting, color, lens, camera-movement, and visual-texture choices, together with an explanation for each recommendation. [PLANNED]
3. **Storyboard development:** turn approved scene and shot decisions into reviewable storyboard assets while preserving their relationship to the source scene. [PLANNED]
4. **Video previsualization:** generate or coordinate short previsualization clips from approved storyboards and shot specifications through third-party services. [PLANNED]

The product should support creative judgment, not replace it. Recommendations are starting points that users can inspect, revise, approve, reject, and regenerate. The system should preserve the provenance of important outputs so teams can understand what screenplay material, user choices, and model operations contributed to a result. [PLANNED]

## What exists today

The current repository is an early Python concept organized around six functions:

- reading screenplay text from a file;
- selecting a cinematic frame;
- suggesting lighting and color;
- suggesting a lens treatment;
- suggesting camera movement; and
- suggesting visual texture.

The existing cinematic functions currently return fixed text and do not vary their output according to screenplay content. The orchestration file also imports `modules` and `utils` package paths that are not present in the visible repository structure. The repository therefore establishes the creative vocabulary and intended processing sequence, but it is not yet a working AI product or enterprise platform.

## The product promise

**From screenplay to a governed, editable cinematic blueprint.** [PLANNED]

Generative Cinema AI will give creators a shared workspace in which written scenes can become structured visual decisions. A writer should be able to explore how a scene could look. A director or cinematographer should be able to refine the proposed visual language. A production team should be able to review decisions and export usable planning artifacts. A studio or school should be able to configure access, approved providers, retention, and governance. [PLANNED]

The platform is not positioned as an automatic director or as proof that one visual interpretation is objectively correct. Its value is in accelerating exploration, making creative rationale visible, and improving continuity between screenplay analysis, shot planning, storyboard review, and previsualization. [PLANNED]

## Intended users

### Individual filmmakers and writers

Use the platform to explore a screenplay visually, compare alternative treatments, and prepare a structured starting point for collaboration. [PLANNED]

### Directors, cinematographers, and production teams

Use shared scene and shot records to refine visual intent, review alternatives, preserve decisions, and export production-planning materials. [PLANNED]

### Film schools and educators

Use explainable recommendations and controlled comparisons to teach how framing, lens, lighting, color, movement, and texture alter interpretation. [PLANNED]

### Studios and enterprise licensees

Use governed workspaces, configurable model providers, role-based access, project isolation, audit history, and administrative policies across multiple productions. [PLANNED]

## Core workflow

### 1. Create a governed workspace

An authorized user creates or joins an organization, selects a production workspace, and starts a project. Organization administrators can configure membership, permissions, approved AI providers, retention, and usage policies. [PLANNED]

### 2. Add screenplay material

The user uploads or pastes screenplay content and confirms that they are authorized to process it. Before submission, the interface identifies the selected third-party provider, applicable retention setting, and whether content may leave the organization’s controlled environment. [PLANNED]

Supported file formats, maximum project size, languages, and screenplay-format compatibility remain [VERIFY].

### 3. Review screenplay structure

The platform proposes a structured breakdown of scenes, characters, locations, actions, emotional beats, and transitions. Users correct or approve the breakdown before downstream generation. [PLANNED]

### 4. Build the cinematic plan

For each approved scene or beat, the platform proposes framing, lighting, color, lens, movement, and texture. Every proposal is presented as an editable recommendation with rationale, source references, model/provider provenance, and version history. [PLANNED]

### 5. Compare and approve alternatives

Users can request alternative visual treatments, compare them, preserve selected decisions, and record human approval. Team comments, review states, and formal approval roles are [PLANNED]; the exact approval model is [VERIFY].

### 6. Generate storyboards

Approved shot specifications can be sent to configured third-party image-generation services to create storyboard candidates. Users review, replace, regenerate, or approve each frame without losing its link to the screenplay scene and shot record. [PLANNED]

### 7. Create video previsualization

Approved storyboard and shot data can be submitted to configured third-party video-generation services for short previsualization clips. Generation availability, duration, resolution, pricing, provider rights, and content restrictions will depend on the selected service and require provider-specific verification. [PLANNED] [VERIFY]

### 8. Export and hand off

Teams can export approved project data as a shot list, scene breakdown, visual-treatment package, storyboard package, or integration-ready structured data. [PLANNED] Exact export formats and compatibility with production tools are [VERIFY].

## Onboarding flow

### Screen 1 — Choose how you work

**Prompt:** “What would you like to create?”

- Explore a screenplay
- Build a shot plan
- Create storyboards
- Prepare video previsualization
- Set up an organization

Storyboard and video selections should explain that these stages depend on an approved screenplay analysis and cinematic plan. [PLANNED]

### Screen 2 — Select workspace type

**Prompt:** “Who are you creating with?”

- Just me
- Production team
- Class or film program
- Studio or enterprise organization

The selection changes onboarding guidance and default collaboration settings, without preventing any user category from accessing the core workflow. [PLANNED]

### Screen 3 — Configure content handling

**Prompt:** “Choose how this project may use AI services.”

Display approved providers, content-routing implications, retention options, and organization restrictions before screenplay upload. Require acknowledgment that the user has authority to process the material. [PLANNED]

### Screen 4 — Start the project

**Prompt:** “Add your screenplay or begin with a sample.”

The product should offer a rights-cleared sample so a user can understand the workflow without uploading confidential material. [PLANNED]

### Screen 5 — Confirm the analysis

Show the proposed scene breakdown first. Explain that the user’s corrections improve the working project record and that generated creative recommendations remain suggestions. [PLANNED]

### Screen 6 — Enter the creative workspace

Guide the user to the first unresolved scene, present the recommendation and rationale together, and make **Edit**, **Compare**, **Approve**, and **Regenerate** the primary actions. [PLANNED]

## Enterprise positioning

Generative Cinema AI is intended to be licensed as a configurable creative-intelligence platform rather than sold as a single opaque generation model. [PLANNED] The enterprise value proposition rests on four capabilities:

- **Creative continuity:** retain the connection between script evidence, cinematic decisions, storyboard assets, and previsualization outputs. [PLANNED]
- **Human control:** keep creative professionals responsible for approval and preserve their revisions. [PLANNED]
- **Provider flexibility:** integrate approved third-party analysis, image, and video APIs behind replaceable provider interfaces. [PLANNED]
- **Governance:** support organizational access, project isolation, audit history, retention policy, and accountable content routing. [PLANNED]

Deployment models, licensing units, identity-provider support, regional hosting, service-level objectives, compliance targets, and customer-support tiers are [VERIFY]. They must not be promised until architecture, legal, security, and commercial review are complete.

## Product language guardrails

Approved positioning should use phrases such as:

- “AI-assisted cinematic planning”
- “editable visual recommendations”
- “screenplay-to-shot-plan workflow”
- “human-reviewed storyboard and previsualization pipeline”
- “configurable third-party AI providers”

Avoid claims such as:

- “directs your film automatically”
- “creates the perfect shot”
- “understands narrative exactly as a filmmaker does”
- “production-ready” before the relevant acceptance gates pass
- “secure,” “private,” or “compliant” without defined controls and verification

## Trust, rights, and transparency

Screenplays and production materials should be treated as confidential by default. [PLANNED] Before enterprise release, the product requires:

- explicit content-routing and retention disclosures;
- encryption and tenant isolation requirements;
- access, audit, deletion, and export controls;
- provider-specific terms and data-use review;
- documented handling of generated-asset rights and provenance;
- human approval before downstream generation or export; and
- qualified legal review of copyright, privacy, licensing, and provider terms.

The exact legal and compliance commitments remain [VERIFY].

## Proposed initial release boundary

The recommended first release is the foundation for the larger vision:

- screenplay ingestion and structural review; [PLANNED]
- scene-level cinematic recommendations that respond to source content; [PLANNED]
- editable rationale, alternatives, provenance, and approval state; [PLANNED]
- project persistence and controlled export; [PLANNED]
- provider-independent third-party API integration; [PLANNED]
- baseline organization, privacy, logging, and administrative controls. [PLANNED]

Storyboard generation should follow once the structured scene and shot contracts are stable. Video previsualization should follow storyboard validation, provider evaluation, cost controls, and rights review. [PLANNED]

## What remains uncertain

- Which screenplay formats, languages, and maximum project sizes must be supported first.
- Whether a single installation must serve every audience or whether individual, education, production, and studio editions are needed.
- Which analysis, image, and video providers meet the required quality, privacy, rights, latency, and cost thresholds.
- Whether enterprise customers require single-tenant deployment, private networking, customer-managed keys, or regional data residency.
- Which production tools and export formats should receive first-class integration.
- How licensing will be measured: users, organizations, productions, usage, generated assets, or a hybrid model.
- What evidence and human evaluation thresholds will define acceptable cinematic recommendation quality.

