# Coverage limits and predeclared interpretations

This file prevents a broad CUA pass rate from being misrepresented as full specification, security, clinical, accessibility, or FHIR certification. `coverage_matrix.csv` maps each case to source sections and distinct scenario; those rows are evaluation requirement keys, not verbatim numbered requirements from the original document.

## Section-level scope

| Description sections | Evaluation treatment |
| --- | --- |
| 1-2 | Product identity and research purpose guide the suite; no separate inflated navigation count |
| 3 | Stack, package versions, database compatibility and architecture are not measured by browser CUA |
| 4 | UI readability, keyboard access, menus, responsive layouts, actions and validation covered; exact computed CSS sizes/contrast ratios excluded |
| 5-6 | Role workflows, observed direct-URL denials and dashboard consistency covered; not a complete backend penetration test |
| 7-10 | Registration/chart, scheduling, check-in and intake covered, including V3 selectors and unit behavior |
| 11-14 | Note states/signatures/addenda, diagnoses, prescriptions, orders and results covered |
| 15-20 | Insurance, claims, denials, authorizations, payments and portal covered |
| 21 | Mandatory deterministic text AI workflows and approval boundaries covered; optional paid LLM/audio/AI billing modes excluded |
| 22-23 | Inbox, per-user unread state, tasks, cohort definitions, filters and CSV parity covered |
| 24 | Documented JSON representations inspected in browser; not formal FHIR conformance or HTTP-method security testing |
| 25 | User-visible relational consistency sampled; schema normalization, transactions and database internals excluded |
| 26 | Fourteen integrated workflow cases plus targeted persistence/cross-role checks |
| 27-28 | Synthetic fixture plausibility and nine role logins; exact seed counts are preflight inventory, not nine dozen extra CUA tests |
| 29 | Reset cancellation, role restriction and isolated confirmed reset; production gating/configuration excluded |
| 30 | Existing unit/Playwright regression suites are separate methods, never mixed into CUA denominator |
| 31 | User-visible histories, states and evidence covered; hidden structured metadata and database assertions excluded |
| 32 | Visible authentication, role/patient boundaries and safe rendering sampled; CSRF, ORM injection, password hashing and secret-storage internals excluded |
| 33-34 | Correct repo, version/deployment provenance and evidence publishing are execution obligations, not fabricated application PASS cases |
| 35-39 | Development strategy/completion requirements are source context; do not implement/fix software during evaluation |

## Limits that need explicit disclosure

1. Screenshots can establish visible readability, cropping, label clarity and focus. They cannot precisely certify CSS font sizes 16/14/20/28px, 44px hit targets, color contrast ratios or full accessibility conformance. Record observed responsive behavior, not exact compliance claims.
2. Height/weight tests establish UI conversion, edits, error retention, save/reload and BMI consistency. They do not prove exact eight-decimal database storage or rejection of forged hidden canonical metadata/unsupported units. Those require a separate backend/automated test method. The suite deliberately does not ask a CUA to inject hidden fields.
3. Normal browser navigation can test access to a known page/JSON resource and visible actions. It cannot establish every HTTP method, CSRF behavior, session-token invalidation property, caching header or server-side idempotency path. Payment replay cases use actual refresh/back/two-tab user workflows, not crafted duplicate requests.
4. Account/database reset has a real destructive effect. Only an isolated designated synthetic evaluation DB is in scope. An unsafe shared deployment is an individual reset blocker, not a reason to skip other tests.
5. Browser read-only JSON checks compare to the application's documented FHIR-inspired mapping. They do not require a complete official FHIR implementation or claim certification.
6. Deterministic simulator scenarios must be documented and reproducible. No real payer/pharmacy/payment/clinical services are used. No paid LLM key is required; optional provider failure/timeouts/malformed LLM-output tests remain separate supplemental work.
7. The base suite does not require every optional feature. It does require explicit human action before a generation workflow creates clinical records or signs notes. Suggestions can be absent without failing the non-mutation cases; if shown, they must be distinguished from approved facts.
8. Exact report rate denominators, aging origin, assignment scope, cancellation policy, macro catalog and scheduling exceptions must be bound from existing specification/application documentation before the relevant attempt. Use source V3 where explicit. Do not redefine a denominator, overlap permission or acceptance state to match an observed incorrect result. Ambiguity that affects verdict is BLOCKED/ORACLE_AMBIGUITY with a separately proposed amendment.
9. Inverted coverage dates and nonpositive ordinary charges/units are predeclared operational validation probes derived from proper field formatting/validation and ordinary billing semantics, not verbatim V3 acceptance sentences. Refund/credit workflows, if explicitly labeled and documented, are different from the ordinary charge/payment path being tested.
10. Multiple tab/session tests require genuine distinct sessions for different users; two tabs sharing cookies are not independent users. Same-user stale-payment tests intentionally share a session. If the tool cannot support isolated staff/patient sessions, block only the affected concurrency/read-state cases.
11. Badge polling is observed within documented interval plus 10 seconds or an undisclosed-policy window of 60 seconds. Report actual latency and the observation limit. This threshold is an evaluation convention, not a quoted V3 SLA.
12. CUA failures can reflect navigation/model limitations. Preserve AGENT/APPLICATION/ENVIRONMENT/DATA/ORACLE/UNCERTAIN attribution separately from outcome. This suite measures task completion and observed conformance, not pure source-code correctness.
13. A missing fixture is not the same as a missing feature. If normal UI should create the required record and fails, its creation test is FAIL. If a downstream negative scenario needs a pre-seeded malformed/historical state normal UI intentionally cannot create, that case is BLOCKED until an existing authorized fixture is available.
14. Missing downloadable action/screenshot exports must be disclosed. Authentic observations can still be described, but absent evidence is never fabricated. Claims of independently reproducible results must reflect actual evidence coverage.
15. Duplicate titles/IDs are prohibited. Generic login variants cover the nine explicitly required accounts. Boundary/state/role cases are not a full Cartesian product, and integration cases are intentionally analyzed separately. No fixed Easy/Medium/Hard/Expert percentage was imposed; difficulty follows case mechanics.
