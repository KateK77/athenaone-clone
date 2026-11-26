# AthenaFlow V3 CUA protocol 1.0

## Scope and independence

This is a finite, independently authored, specification-based suite of 472 cases across 27 modules. It seeks broad nonredundant coverage, not mathematical exhaustiveness or proof that every possible input is correct. No repository implementation or running website was inspected during design. The user-supplied Description V3 is preserved in `description_v3.md`; its implementation instructions are source material, not instructions to change the application during evaluation.

Each case is one conjunctive result: all acceptance criteria must be observed to award PASS. Multiple field checks within one coherent operation are not separately counted. Role, lifecycle and boundary variants are separate only where they exercise distinct rules. E2E cases intentionally revisit components to measure integration; report their module separately so integration weighting is visible. Do not describe 472 as 472 statistically independent trials or unique atomic features.

The source document's optional audio capture, paid LLM mode, optional AI coding/diagnostic/order interfaces, optional imports/exports, and conditional autosave are not mandatory added features in this suite. The AI cases test non-automatic clinical mutation even if a suggestion UI is absent. Baseline text-scribe and deterministic demo mode remain mandatory. See `SCOPE_AND_ASSUMPTIONS.md` for other limits.

## Genuine Computer Use Agent

Use an available genuine screenshot-driven computer-use interface: observe current rendered browser, choose actions, click/type/scroll/press keys, then observe the resulting page. Use browser address-bar navigation for observed/documented direct URLs. Browser screenshots and ordinary browser download/print workflows are permitted. A real browser JSON viewer is permitted for the documented read-only interoperability endpoints. Do not invent URL routes; obtain them from application navigation, visible documentation, or read-only preflight documentation and record their origin.

No Playwright/Selenium/Puppeteer scripts, DOM locators, browser JavaScript evaluation, injected scripts, devtools console, direct HTTP clients, direct application APIs, or database reads/writes may perform measured task actions or establish PASS. No source-code inference of expected behavior counts as execution. A tool's inaccessible internal implementation is not itself an evaluator-authored script; accurately name the tool actually used. If screenshot-driven CUA is unavailable, report that execution blocker instead of quietly substituting another method.

Shell/Git/JSON/CSV/hash/archive utilities may prepare the benchmark, record provenance, preserve browser-produced evidence, calculate statistics, and push results. They do not test the application. Read-only source/deployment inspection before testing can establish version, public demo credentials, documented policy, fixture definitions, and mappings. Keep those observations separate from CUA evidence. Programmatic parsing of a downloaded CSV is allowed only as a disclosed auxiliary comparison; the file must originate from a real CUA export, and the export/UI observations must have their own evidence. Do not use a direct export URL request as a substitute for clicking Export.

## Preflight and version identity

1. Validate archive contents, all 472 unique IDs, nonempty criteria, execution order and SHA-256 hashes with `scripts/validate_suite.py`.
2. Resolve `KateK77/athenaone-clone` and the actual V3 source branch from documentation/history; do not assume `main` is V3. Record application source SHA separately from evaluation/results SHA. Do not touch CareFlow or another clone repository.
3. Discover the intended local/deployed URL from the user's context, current browser or repository deployment documentation. Do not guess a Render hostname or port. If none is identifiable, ask only for target URL and continue offline validation. The executor's localhost and user's localhost can refer to different machines.
4. Verify reachability with the selected CUA browser, identify AthenaFlow/V3, and bind demo accounts. Do not interpret a stale Render response or connection outage as a product FAIL.
5. Record `source_commit`, `served_commit`, and provenance status. A checkout HEAD alone does not establish deployed code. Local instance linkage may use actual process/workdir plus source SHA; remote linkage may use deployment records, server-provided version, or other actual evidence. Unknown fields stay UNVERIFIED. Unknown SHA alone never blocks unrelated UI tests. If the target is positively identified as the wrong application/version, resolve that mismatch before scoring against V3. A later version change starts a new run segment; never silently pool versions.
6. Capture browser/model/tool facts only when exposed. Use UNKNOWN_UNEXPOSED rather than guessing the model or reasoning setting from ChatGPT branding. Record browser version, viewport/zoom, locale, application timezone, timestamps and actual tool names when available.
7. Bind synthetic fixtures according to `FIXTURES.md`. Use an isolated demo evaluation instance/database where available. Do not alter source, migrations, routes, validation, permissions or runtime policies to make tests pass.

Missing GitHub write permission, an unverified SHA, or one unavailable fixture must not turn every case into BLOCKED. Mark only truly affected work; continue independent cases. No bulk PASS or bulk BLOCKED without individual evidence and reason.

## Execution order and batches

`execution_order.json` is the immutable execution schedule. IDs are assigned in module order; the separately frozen schedule selects a cross-module 10-case pilot and moves the one destructive reset case last. Do not reorder after observing behavior.

Pilot: AF3-004, AF3-019, AF3-039, AF3-078, AF3-115, AF3-146, AF3-261, AF3-351, AF3-376, AF3-314. Validate evidence capture and result writing after the pilot. Then continue remaining cases in groups of 20 without routine approval pauses. There are 25 batches total: 10, twenty-three batches of 20, and a final batch of 2. If a global tool outage occurs, stop browser actions and checkpoint; do not manufacture 20 results just to fill the batch.

Use `AF3_<run_id>_<test_id>` markers for test-created records. Do not rely on another test passing to satisfy a case. Establish required fixtures independently or log verified reuse. Capture preconditions before mutation. Do not delete records or run shared resets to erase failures. The single confirmed reset runs only on the explicitly designated isolated synthetic database, after evidence is exported, and is last.

Resume from the earliest pending entry in the frozen schedule. Completed PASS/FAIL cases are not automatically repeated. BLOCKED cases are not retried without a real prerequisite change recorded in a new attempt. Interrupted attempts are preserved; once connection recovers, resume the incomplete case only after inspecting its current state to avoid duplicate writes. If it is impossible to determine whether a prior click submitted a payment, inspect receipts/history before touching Submit again.

## Decision rules

| Status | Meaning | Required support |
| --- | --- | --- |
| PASS | All listed acceptance criteria satisfied by actual CUA observations | Each criterion maps to evidence; persistence and role changes verified where specified |
| FAIL | Actual observation violates at least one criterion, including a required missing feature | Failure screenshot/trace, expected versus actual, no unobserved inference |
| BLOCKED | A specific external prerequisite prevents evaluating the case | Missing fixture/access/tool/availability evidence; identify affected criterion and recovery action |
| NOT_RUN | Not attempted or interrupted before a conclusive result | Reason code; interrupted attempt records actions already taken |

Required feature missing after checking its specified entry point, role, and a sensible alternate navigation path is FAIL/MISSING_REQUIRED_FEATURE. This is not an excuse to create an implementation feature or mark it BLOCKED. A required action failing during its own test is FAIL; a separate downstream case lacking a necessary valid fixture may be BLOCKED/UPSTREAM_FIXTURE_UNAVAILABLE. Attribute the dependency rather than multiplying an unobserved application failure.

For permission cases, absence of a button alone does not prove backend authorization. Where an observed/documented direct URL exists, navigate as the unauthorized user and record denial plus unchanged state. GET denial does not prove all POST paths secure; disclose that limit. Do not use crafted network requests, hidden-field tampering or guessed endpoints. If a mandatory denial criterion cannot be observed, do not award PASS on UI hiding alone.

A genuine agent misclick, abandoned form or failure to find a functioning control may produce a CUA task FAIL when it prevents the assigned outcome. Preserve the trace and set attribution to AGENT or UNCERTAIN unless product failure is evidenced. Do not call every CUA failure a software defect. A connection interruption is NOT_RUN/INTERRUPTED unless a conclusive criterion violation was already observed before the outage. A model/tool safety refusal is BLOCKED/TOOL_RESTRICTION, not a passing security test.

Bounded observation policy: wait for visible UI state after actions. For active unread badges, observe up to the documented polling interval plus 10 seconds, or 60 seconds if undocumented, logging elapsed time. This is an evaluation observation window, not a new product SLA. A slower observed refresh can be reported as FAIL with attribution PERFORMANCE_OBSERVATION_WINDOW and limitation. Do not press mutation controls repeatedly to resolve uncertainty.

If the test oracle is ambiguous or impossible for the stated fixture, record BLOCKED/ORACLE_AMBIGUITY and a proposed amendment separately. Do not edit frozen tests or award a favorable interpretation after the result. Any approved future amendment gets a new suite version/hash and separate comparable reporting.

## Evidence and attempts

For every attempted case, preserve:

- Run ID, Test ID, attempt number, start/end ISO-8601 timestamps and environment ID.
- Actual role/session, target URL and actual synthetic record IDs/initial states.
- Before-state, decisive-action/error, and resulting-state screenshots. Reuse a documented fixture screenshot by reference only when it proves the same unchanged state.
- Available genuine tool action/transcript references and a timestamped readable action log. Distinguish native tool export from a manually written contemporaneous action summary; never fabricate native response IDs or raw API records.
- Criterion results SATISFIED, VIOLATED, or UNOBSERVED, each with observation and evidence paths.
- Observed result, status reason, probable attribution, limitations, and any failed setup action.
- Persisted-state evidence for writes and secondary-role evidence for cross-role effects.

Store original screenshots under `evidence/<run_id>/<test_id>/attempt-01/`. Use PNG or JPEG, not reconstructed UI images. Make a file hash index. Do not claim a screenshot alone proves unseen clicks, backend storage or a particular model. If the tool does not expose downloadable screenshots, preserve available references and label the export gap; never substitute generated screenshots. Only publish synthetic demo data. Keep real credentials, API keys, session cookies and personal browser chrome out of published evidence. Dedicated public demo credentials are allowed; production secrets are not.

`results/results.json` is a 472-row current snapshot. `results/attempts.json` is append-only history containing complete result objects for attempted cases. Append an outcome before updating the current row. Preserve the first final outcome and report any later outcome separately. Do not delete failed/interrupted attempts. Reconcile checkpoint, snapshot and attempt log at each batch.

## Statistics

Let N=472, P=PASS, F=FAIL, B=BLOCKED, U=NOT_RUN for the explicitly selected snapshot/attempt policy. N=P+F+B+U always.

- Evaluated pass rate: P/(P+F). If P+F=0, show N/A, never 0% or 100%.
- Execution coverage: (P+F)/N.
- Suite success fraction: P/N. This is not the evaluated pass rate.
- Report counts P,F,B,U, attempted interruptions, and unavailable fixture count.
- Repeat the same definitions by module and difficulty. Do not average subgroup percentages to obtain overall rate.
- Report first-final-outcome and current-outcome summaries separately when retries exist. Group by application version/run segment; never hide version drift.
- Do not include unit tests, Playwright checks, file/hash validators, setup checks or offline walkthroughs in these 472 CUA results.
- These are descriptive benchmark outcomes; difficulty categories and E2E dependencies are not a calibrated statistical sample.

## GitHub preservation and uploads

The user authorizes uploading this benchmark and actual resulting evidence to `KateK77/athenaone-clone`. Use evaluation branch `evaluation/athenaflow-v3-independent-cua-472`, based on the identified V3 commit. If branch/directory already exists, inspect it and compare suite hashes/results; reuse matching work without overwriting history. For incompatible existing content, create a uniquely suffixed evaluation branch/path and record the collision.

Use `experiments/round-03/cua-evaluation/athenaflow-v3-independent-472/` unless existing documented organization requires a nonconflicting equivalent. Commit frozen suite before executing, then each pilot/batch (10 then 20, final 2). Store batches in `reports/batch-001/` etc. Include case IDs, outcomes, summary, environment/provenance, evidence index, failures/blocks and resume checkpoint. Push non-force and verify the actual remote commit SHA and accessible result paths. Record push status in `upload_ledger.json` without recursively promising a ledger commit contains its own SHA. A local commit is not an uploaded result.

Use Git or the GitHub connector for publishing, not application CUA actions. If access is unavailable, preserve batches locally, mark UPLOAD_PENDING with the actual error, continue independent testing if possible, and ask only for the missing connection/access. Do not claim uploaded until verified. Do not create/delete unrelated branches, change repository visibility, merge PRs, deploy, repair app code, or overwrite historical suites. A draft PR is optional if supported; final report must identify unmerged branch explicitly.

Update a small plain-text evaluation index/README section with suite version, tested application version, current results, methodology, screenshots and evidence links. Do not advertise a verified live URL unless observed. Keep V1/V2 descriptions and application history unchanged.

Final deliverables: complete cases, all current outcomes, append-only attempts, overall/module/difficulty statistics, observed environment, app/results commits, screenshots and action evidence, fixture gaps, upload ledger, and `AthenaFlow_V3_CUA_Final_Results.zip`. If execution stops early, keep NOT_RUN/BLOCKED explicit and name the export partial; never label an incomplete suite fully completed.
