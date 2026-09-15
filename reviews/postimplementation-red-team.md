# Generative Cinema AI — Postimplementation Red-Team Review

**Review date:** 2026-09-15  
**Repository base commit:** `993344a2801bab95c27896c548f0927afea2826e` with uncommitted implementation files inspected  
**Scope:** packaged source, API, CLI, configuration, Dockerfile, CI, tests, README claims, and targeted failure/security behavior. This review does not certify third-party providers, a hosted environment, or enterprise controls that have not been implemented.

## Release classification

**PROTOTYPE — acceptable for local demonstrations with owned, synthetic, licensed, or public-domain text. NO-GO for deployment as a network-accessible service, real confidential screenplays, external pilots, MVP claims, or enterprise licensing.**

The new code materially improves the original repository: it installs, builds a wheel, passes its tests, passes lint and strict type checking, parses a narrow screenplay subset, returns scene-specific deterministic recommendations, and clearly disclaims missing enterprise capabilities. It does not meet the repository's own MVP definition because editing/approval, export, persistence, privacy controls, authentication, authorization, tenant isolation, and pilot acceptance evidence are absent.

## Verification record

| ID | Command or targeted case | Result | Confidence / caveat |
|---|---|---|---|
| POST-EV-001 | `python -m pytest -q` | 11 tests passed; two dependency deprecation warnings | High; suite is narrow and mostly happy-path |
| POST-EV-002 | `python -m ruff check .` | Passed | High for configured Ruff rules |
| POST-EV-003 | `python -m mypy` | Passed in strict mode for 7 packaged source files | High for statically covered package; tests are not included in configured package target |
| POST-EV-004 | `python -m pip check` | No broken requirements | High for active environment, not a clean locked install |
| POST-EV-005 | `python -m pip wheel . --no-deps -w /tmp/gca-wheel-test` | Wheel built successfully | High for buildability; build isolation resolved dependencies dynamically |
| POST-EV-006 | `python -m build` | Failed because the `build` package is not declared/installed | High; this command is not documented or used by CI, so it is not itself a product failure |
| POST-EV-007 | Blank, extra-field, and 500,001-character API requests | All rejected with HTTP 422 | High; oversized validation response echoed the full submitted text |
| POST-EV-008 | Prompt-injection-like screenplay text | Returned ordinary deterministic output; no tool or model execution occurred | High for current rule provider only; says nothing about future LLM adapters |
| POST-EV-009 | Nil and caller-selected tenant/project UUIDs | Accepted with HTTP 200 and reflected in response | High; README explicitly says IDs are trace-only |
| POST-EV-010 | Explicit `input_format="plain_text"` containing `INT. ...` | Parsed as Fountain scene despite explicit format | High; `input_format` does not control parser selection |
| POST-EV-011 | Fountain title-page preamble before first scene | Warning emitted, but preamble omitted from normalized output | High; behavior is disclosed only in runtime warning |

## Critical findings

| ID | Finding | Evidence and impact | Proposed fix | Owner | Release-blocking |
|---|---|---|---|---|---|
| POST-C-01 | **Validation errors disclose and amplify confidential screenplay content.** | POST-EV-007: sending 500,001 characters produces a 422 response of approximately 500 KB because FastAPI/Pydantic includes the rejected `screenplay_text` in the error detail. A malformed request can therefore echo unpublished script content to clients, proxies, APM/error capture, and logs; it also enables response-amplification/resource pressure. | Add an application-level request-body limit before JSON/Pydantic parsing. Install a custom validation-error handler that redacts input values for sensitive fields and caps error size. Configure proxy/server limits and prevent request/response bodies from observability capture. Test oversize, malformed JSON, invalid UUID, blank text, and extra fields for bounded non-content-bearing errors. | Technical Specialist + Security | Yes for any network deployment |
| POST-C-02 | **The HTTP API has no authentication, authorization, or tenant isolation.** | POST-EV-009 and source inspection: any caller may supply any valid `tenant_id` and `project_id`; the endpoint processes it. The README correctly disclaims isolation, but the Docker image binds to `0.0.0.0`, making accidental exposure easy. | Until identity is implemented, make the API explicitly local/development-only: fail startup outside development, bind localhost by default, disable/restrict docs, and add a conspicuous warning. Before external use, authenticate callers, derive tenant context from membership rather than request data, enforce authorization centrally, and add cross-tenant negative tests. | Technical Specialist + Security | Yes for network service, confidential content, and external pilot |

## Major findings

| ID | Finding | Evidence and impact | Proposed fix | Owner | Release-blocking |
|---|---|---|---|---|---|
| POST-M-01 | **`input_format` is semantically ignored.** | POST-EV-010: `PLAIN_TEXT` still invokes heading recognition; `AUTO` and `FOUNTAIN` also share the same parsing path except for one warning. The API presents a strict enum that implies behavior it does not provide. | Implement explicit adapters/dispatch semantics, or remove the parameter until modes differ. Define: `plain_text` always one scene (or documented heuristic); `fountain` validates Fountain subset and reports unsupported constructs; `auto` detects with confidence. Add contract tests. | Technical Specialist | Yes for a claimed format contract |
| POST-M-02 | **Source preservation is incomplete.** | POST-EV-011: title page/preamble content is discarded from normalized output. Scene trailing whitespace is also normalized away. This conflicts with the planned lossless provenance principle and can remove titles, author information, notes, or nonstandard scene content from the domain record. | Preserve an immutable original asset and represent unparsed spans explicitly; never drop content merely because it is outside recognized scenes. Return parser diagnostics with source ranges. Distinguish normalized view from source record. | Technical Specialist | Yes before calling parsing lossless or processing real scripts |
| POST-M-03 | **Evaluation tests prove rule execution, not cinematic usefulness.** | Four keyword fixtures assert the expected label and evidence containment. They do not assess false positives, ties, negation, dialogue attribution, continuity, feasibility, diversity, bias, source-span precision at corpus scale, or professional usefulness. For example, isolated words such as “dark” decide the entire scene treatment. | Rename current suite “deterministic regression tests.” Implement the previously specified evaluation protocol with rights-cleared corpus, non-trigger/negation/adversarial cases, baseline comparisons, blinded film-professional review, agreement/adjudication, severe-error gates, and approved thresholds. | AI Evaluation Lead + Film SMEs | Yes for MVP/usefulness claims and external pilot |
| POST-M-04 | **Recommendation provenance is insufficient for reproducibility.** | Results include provider name/version but not rule/prompt/configuration hash, code revision, input hash, timestamp, parameters, policy version, or per-recommendation rule/evidence decision. `run_id` is random, so an output cannot be independently reconstructed from its record. | Add a versioned generation manifest: source hash/version, provider/model/rule version, code/build revision, configuration/policy/schema version, parameters, timestamp, deterministic seed where applicable, and output hash. Keep sensitive raw content out of logs. | Technical Specialist | Yes for auditability or enterprise claim |
| POST-M-05 | **Dependency and CI supply chain is not reproducible.** | `pyproject.toml` uses broad version ranges without a resolved lock; CI upgrades pip and resolves newest matching packages; GitHub Actions use mutable major tags. A future install can differ despite unchanged source. No SCA/SBOM/signature step exists. | Commit a reviewed lock/constraints file with hashes for deployable environments, test lowest/supported versions as appropriate, pin CI actions to commit SHAs, generate SBOM, scan dependencies/container, and define update cadence. | Platform/Security | Yes for externally distributed image or enterprise pilot |
| POST-M-06 | **Container hardening and build-context controls are incomplete.** | Positive: non-root runtime and narrow `COPY` directives. Missing: `.dockerignore`, digest-pinned base, read-only filesystem guidance, dropped capabilities, resource limits, vulnerability scan, SBOM, and verified health behavior. The Docker build itself was not executed in this environment. | Add `.dockerignore`; pin/automate trusted base updates; scan image; publish SBOM; configure read-only root filesystem/tmpfs, no-new-privileges, dropped capabilities, memory/CPU/PID limits, and deployment health/readiness checks. Verify the built image in CI. | Platform/Security | Yes for hosted pilot, not local prototype |
| POST-M-07 | **No bounded execution/capacity controls beyond a character field constraint.** | The 500k validation limit occurs after request parsing; every scene produces five recommendations repeating evidence. No request timeout, concurrency limit, rate limit, scene limit, line limit, or output-size bound exists. Synchronous work occupies the API worker. | Enforce body limit upstream and in ASGI middleware; set scene/line/output limits; estimate work before processing; rate-limit; set server timeouts/concurrency; move costly work to bounded jobs before model integrations; return a stable problem response. Add load and soak tests. | Technical Specialist + Platform | Yes for network deployment |
| POST-M-08 | **API error and operational contracts are absent.** | No request/correlation ID, RFC 9457 problem schema, controlled exception mapping, structured logs, metrics, readiness check, or shutdown/provider health semantics. `/health` only proves the process responds. | Add separate liveness/readiness endpoints, bounded typed errors, request IDs, safe structured telemetry, startup checks, and exception tests. Define what health means for provider-dependent modes. | Platform + Technical Specialist | Yes for private beta |
| POST-M-09 | **The current provider protocol is too weak for the planned third-party boundary.** | `analyze_scene(scene)` has no tenant policy, timeout/cancellation, privacy classification, request ID/idempotency, model parameters, usage/cost, refusal/policy result, or async job state. A later adapter would either bypass controls or break the interface. | Introduce a request context and typed provider result/failure taxonomy before adding an external API. Keep secrets and tenant policy in the gateway, not domain input. Add adapter contract tests for timeout, refusal, malformed structured output, retryability, and policy-ineligible fallback. | AI Platform + Technical Specialist | Yes before any third-party API integration |
| POST-M-10 | **The default evidence citation can be misleading.** | For neutral scenes, the heading is cited as support while rationale states that the “neutral signal is supported by the cited screenplay text.” A heading may establish no neutral cinematic signal. For triggered scenes, a single keyword is cited even when the count and context determined the rule. | Distinguish `trigger_evidence`, `context`, and `fallback/no-evidence`. For default recommendations, say no classified signal was found and label the proposal heuristic. Cite all material triggers with bounded context and add negation/polysemy tests. | Technical Specialist + Film-domain SME | Yes before explainability claims beyond prototype |
| POST-M-11 | **No persistence, editing, approval, export, or deletion workflow exists.** | Source and README explicitly acknowledge these omissions. This is not a regression, but it blocks the declared user outcome and every maturity level above prototype. | Implement the narrow vertical slice in release-gate order: immutable source/project storage, secure identity/authorization, editable recommendation/shot state, approval history, one human-readable and one machine-readable export, and verified deletion. | Product + Technical Specialist | Yes for MVP |

## Minor findings

| ID | Finding | Evidence and impact | Proposed fix | Owner | Release-blocking |
|---|---|---|---|---|---|
| POST-m-01 | **Test tooling emits deprecation warnings.** | POST-EV-001 reports Starlette/TestClient-related deprecations. This may become a future compatibility failure. | Resolve compatible dependency versions and add a controlled warning policy so new warnings fail CI while known temporary warnings are tracked. | Technical Specialist | No |
| POST-m-02 | **Build verification is not a named developer/CI check.** | POST-EV-006 failed locally because `build` is absent; wheel creation via pip succeeds. CI does not build/install/test the produced wheel. | Add `build` to release tooling or standardize on `pip wheel`; CI should install the built wheel in a clean environment and smoke-test CLI/API imports. | Platform | No for prototype; Yes for package release |
| POST-m-03 | **Nil UUIDs are accepted as trace identifiers.** | POST-EV-009. This is not currently an authorization flaw because IDs are expressly non-security trace fields, but nil IDs weaken trace quality and could become a sentinel-confusion bug. | Reject nil UUIDs and generate IDs server-side where possible. Never use caller-provided IDs as authorization evidence. | Technical Specialist | No |
| POST-m-04 | **Legacy modules remain and create two product surfaces.** | README calls root modules unsupported; the compatibility `main.py` uses the package, but five hard-coded root modules and `script_parser.py` remain importable. Users may accidentally depend on stale behavior. | Move historical code to a tagged commit/archive or delete after confirming no compatibility requirement. Add tests that documented imports/entry points are the only supported surface. | Technical Specialist | No |
| POST-m-05 | **API documentation and schema endpoints are enabled by default.** | FastAPI defaults expose `/docs`, `/redoc`, and `/openapi.json`. Fine for local development, but unsafe as an accidental production default alongside unauthenticated processing. | Make docs environment-configurable and protected/disabled in hosted production. | Technical Specialist | Yes only if deployed externally before authentication |
| POST-m-06 | **README “strict typed request/response contracts” is slightly broader than demonstrated.** | Pydantic models forbid extras and mypy passes, but semantic format behavior is incorrect (POST-M-01), several IDs are unconstrained strings, and no external provider contract exists. | Say “strict Pydantic schemas for the current local analysis request/result” until semantic and provider contracts are tested. | Writer + Technical Specialist | No |

## Targeted tests that should be added immediately

1. Validation responses never contain screenplay text and remain below a fixed size.
2. Server/proxy rejects bodies above the configured byte limit before JSON parsing.
3. Explicit input-format dispatch behaves distinctly and predictably.
4. Every source byte/character belongs to either a parsed node or an explicit unparsed span.
5. Heading offsets remain correct for CRLF, Unicode, indentation, title pages, and trailing whitespace.
6. False-trigger cases: negation, quoted dialogue, substrings, polysemy, competing/tied signals, repeated terms, and non-English text.
7. Provider exceptions, timeouts, invalid results, cancellations, refusals, and non-retryable policy decisions map to safe bounded errors.
8. Local-only startup guard prevents accidental non-development exposure until authentication exists.
9. Built wheel and container run as non-root in clean CI and expose only intended files/endpoints.

## Release decision

**Proceed with technical correction as a local prototype; do not release externally.** The implementation is a credible foundation demonstration, but the two Critical defects must be closed before any network deployment, and the Major product/security/evaluation gaps must be closed according to the target maturity gate. Even after code correction, real confidential screenplay use requires verified privacy, retention/deletion, provider-contract, and legal controls that are not present in this repository.

## What remains uncertain

- The staged capability interpretation still needs explicit user confirmation if not separately recorded.
- No clean container execution, vulnerability scan, SBOM, or hosted-environment test was available in this review.
- No external provider exists yet, so privacy, retention, output-rights, refusal, latency, cost, and model-quality behavior remain untested.
- No human cinematic evaluation or customer workflow validation has occurred.
- The initial design-partner segment, input/export formats, deployment region, retention window, and contractual controls remain undecided.

## Remediation verification and final dispositions — 2026-09-15

### Re-verification results

| Check | Final result |
|---|---|
| Automated tests | **20 passed**; two known dependency deprecation warnings remain |
| Ruff | Passed |
| Strict mypy | Passed for 8 packaged source files |
| Dependency consistency | `pip check` passed |
| Package build | `python -m build` passed; sdist and wheel created |
| Wheel build | `pip wheel --no-deps` passed |
| Oversized request | HTTP 413, 68-byte response, confidential marker absent |
| Invalid-model request | HTTP 422, bounded response, confidential marker absent |
| Malformed JSON | HTTP 422, bounded response, confidential marker absent |
| Non-loopback request under default settings | HTTP 403 |
| Non-development startup without explicit override | Failed closed as designed |
| Explicit plain-text parsing | Verified by test to remain one plain-text scene |
| Preamble/trailing text preservation | Verified across CRLF, Unicode, and trailing whitespace fixture |

### Finding dispositions

| Finding | Final disposition | Verification / residual boundary |
|---|---|---|
| POST-C-01 — screenplay echo and request amplification | **Fixed for declared local prototype** | Pre-validation byte cap and redacted/bounded validation handler are implemented and covered by oversized, invalid, and malformed-request tests. A production reverse proxy and body-free telemetry policy remain required before network use. |
| POST-C-02 — no authentication, authorization, or tenant isolation | **Mitigated for declared local prototype; remains Critical for any network/external scope** | Default non-loopback requests receive 403; Docker and README bind to `127.0.0.1`; non-development import fails closed without explicit override. `ALLOW_NETWORK_API=true` intentionally bypasses only the exposure guard and supplies no identity or isolation. |
| POST-M-01 — ignored format semantics | **Fixed for prototype contract** | Explicit `plain_text` no longer detects headings; Fountain/auto behavior and tests are documented. Full Fountain conformance remains out of scope. |
| POST-M-02 — source preservation | **Fixed for supported prototype path** | Preamble becomes an explicit context scene; exact input including trailing whitespace is represented and tested. Durable immutable storage is still absent. |
| POST-M-03 — evaluation insufficient for usefulness | **Open** | Current 20-test suite is engineering/regression evidence only, not cinematic or customer validation. |
| POST-M-04 — reproducibility provenance incomplete | **Open** | Provider/version remain present, but source/config/build hashes, timestamps, policy versions, and durable manifests are absent. |
| POST-M-05 — supply-chain reproducibility | **Open** | Package build is now tested; dependency lock/hashes, action SHA pins, SCA, SBOM, and signed artifacts remain absent. |
| POST-M-06 — container hardening | **Partially fixed** | `.dockerignore` and loopback binding added; image execution/scanning, digest pinning, read-only runtime, dropped capabilities, and resource limits remain open. |
| POST-M-07 — capacity controls | **Partially fixed** | ASGI body cap is implemented and tested; rate, concurrency, scene/output, CPU/time, and deployment-layer limits remain absent. Acceptable only for bounded local use. |
| POST-M-08 — operational contracts | **Open** | Safe validation responses improved; request IDs, telemetry, readiness, exception taxonomy, and production health remain absent. |
| POST-M-09 — external provider contract | **Open** | No third-party provider is implemented; must be corrected before such integration. |
| POST-M-10 — misleading neutral evidence | **Fixed for prototype** | Evidence now distinguishes `trigger` from `context`; neutral rationale explicitly says no signal was classified. Broader semantic/negation evaluation remains open. |
| POST-M-11 — no MVP workflow | **Open** | Persistence, identity, editing, approval, export, and verified deletion remain absent. |
| POST-m-01 — deprecation warnings | **Open** | Test run still reports two dependency warnings. |
| POST-m-02 — build check | **Fixed** | `build` is a dev dependency; CI builds, reinstalls, and smoke-tests the artifact; local build passed. |
| POST-m-03 — nil UUIDs | **Open** | No evidence of remediation; trace-only status limits impact locally. |
| POST-m-04 — legacy surfaces | **Open** | README disclaims them, but stale root modules remain. |
| POST-m-05 — docs exposure | **Fixed for local prototype** | Docs/OpenAPI are development-only and protected by the loopback guard. Authentication remains required before network exposure. |
| POST-m-06 — schema wording | **Fixed** | README now narrows the claim to current Pydantic request/result schemas. |

### Final classification

**LOCAL PROTOTYPE — GO for local demonstration with owned, licensed, public-domain, or synthetic screenplay text.**

**No Critical finding remains for that narrowly declared local-only scope.** The formerly Critical content-echo defect is fixed, and unauthenticated network exposure is fail-closed and loopback-restricted by default. The explicit network override is not a security control and must never be interpreted as authorization for external deployment.

**NETWORK / EXTERNAL PILOT / CONFIDENTIAL PRODUCTION CONTENT / ENTERPRISE — NO-GO.** POST-C-02 immediately returns to open Critical status if non-loopback access is enabled. Authentication, authorization, real tenant isolation, persistence/deletion, provider governance, operational hardening, professional creative evaluation, and legal/privacy controls remain mandatory for higher maturity classifications.
