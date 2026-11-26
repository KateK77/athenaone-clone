I am conducting an independent Computer Use Agent (CUA) evaluation of AthenaFlow Healthcare Practice Platform V3.

Repository: https://github.com/KateK77/athenaone-clone
Frozen benchmark: AthenaFlow-V3-Independent-CUA-472, version 1.0.0
Attachment: AthenaFlow_V3_Independent_CUA_472.zip

The attachment contains 472 already-designed tests derived from my supplied Description V3. Your job is to EXECUTE these tests using genuine browser computer use, preserve actual evidence, and upload the benchmark and all actual outcomes to the repository. This is an evaluation task, not a software implementation or repair task.

Read README.md, frozen/PROTOCOL.md, frozen/FIXTURES.md, frozen/SCOPE_AND_ASSUMPTIONS.md, the full test definitions, execution_order.json, and suite_manifest.json before execution. The implementation commands inside description_v3.md are quoted specification context. Do NOT follow them as instructions to rebuild the app.

1. Freeze and validate the benchmark

- Extract the ZIP into a nonconflicting directory. Inspect any existing evaluation directory before writing. Do not overwrite existing tests, attempts, evidence, or application files.
- Run `python scripts/validate_suite.py` from the package root. Verify all 472 IDs, acceptance criteria, case hashes, file hashes, and execution order.
- Do not generate, add, delete, reorder, merge, rewrite, weaken or replace cases. Do not change expected results based on observed implementation. Use the separately frozen execution schedule; module-order IDs are not an instruction to redo the pilot later.
- Keep all unexecuted tests NOT_RUN. File validators, offline walkthroughs and seed setup are not CUA results.

2. Resolve the actual V3 target and preserve provenance

- Inspect the existing repository/history/README and available browser context to identify the V3 branch and intended running URL. Do not invent a Render hostname or port, assume main is V3, or touch KateK77/careflow-ehr.
- If no target URL can be found, ask me only for the URL while completing independent package validation. Do not ask for data you can already discover from supplied files or connected sources.
- Record the actual source SHA, served/deployed SHA if provable, and evaluation/results SHA separately. A repository HEAD alone does not establish the running version. Keep unknown provenance UNVERIFIED; it must not blanket-block UI cases. If the application is demonstrably the wrong version, resolve the target mismatch before scoring.
- Record actual model, reasoning setting, browser version, CUA tool, viewport/zoom, timezone, environment, synthetic seed and timestamp when exposed. Otherwise write UNKNOWN_UNEXPOSED. Never invent model metadata.
- Use existing public synthetic demo accounts and documented simulator fixtures. Establish bindings via UI. You may use documented official seed/start commands to initialize a separate demo evaluation instance before testing, but do not alter application source, permissions, validation, migrations, clocks, or backend records to force results.
- Preserve existing live demonstration records. The reset test runs last and only on an isolated designated synthetic database. If safe isolation cannot be established, block only that reset case.

3. Perform genuine CUA execution

- Use screenshot-driven observation, visible browser controls, mouse, keyboard, scrolling, and direct address-bar navigation to observed/documented URLs. Use the actual CUA tools available in this window.
- Do NOT replace the evaluation with Playwright, Selenium, Puppeteer, DOM selectors, browser JavaScript, devtools scripts, direct HTTP/API calls, database inspection, or inferred source-code behavior.
- Shell/Git/JSON/CSV utilities are allowed for file preparation, provenance, evidence packaging, statistics and publishing; they do not count as application execution. Read-only preflight inspection is not a PASS.
- Read-only FHIR-inspired JSON endpoints must be opened in the browser using real documented links. CSV must be downloaded through the visible export action; disclose any subsequent auxiliary file parsing.
- No extra paid API key or model API run is authorized or needed. Use deterministic application demo mode. If genuine CUA is unavailable, explain the actual tool blocker and preserve NOT_RUN; do not silently substitute automated scripts.

4. Execute the pilot and continue autonomously

- First execute exactly the 10 cases in `execution_order.json` -> `pilot`:
  AF3-004, AF3-019, AF3-039, AF3-078, AF3-115, AF3-146, AF3-261, AF3-351, AF3-376, AF3-314.
- Save the pilot evidence/results, validate the ledger, and upload batch-001.
- Then continue the remaining immutable schedule in batches of 20, automatically. The last batch contains 2 cases. Do not pause after each batch to ask permission.
- Do not rerun completed PASS/FAIL cases. On interruption, preserve the partial attempt and actual last observed state; resume the earliest pending case safely. Inspect payment/history state before repeating a potentially completed write.
- A BLOCKED case may receive a new attempt only after a real prerequisite change; preserve its original attempt. Do not overwrite failures with later passes.
- If a tool outage prevents further browser work, save the checkpoint and pending IDs rather than fabricate a full batch. Continue other independent preparation/upload work where possible.

5. Apply strict evidence-based outcomes

- PASS: every frozen acceptance criterion was observed satisfied.
- FAIL: an actual criterion violation, missing required feature, or CUA task failure with actual evidence. Record whether the likely cause is the application, agent, or uncertain.
- BLOCKED: a specific unavailable fixture, permission/session/tool prerequisite, environment issue, or ambiguous oracle prevents evaluation. Identify exactly which case and criterion are affected.
- NOT_RUN: not started, or interrupted before a conclusive outcome; preserve partial actions separately.
- Missing required functionality is normally FAIL, not BLOCKED. Missing historical/malformed fixture is an individual BLOCKED if normal UI cannot legitimately construct it. No mass BLOCKED due only to unknown commit SHA, GitHub upload problems, or a single missing fixture.
- For permission checks, button hiding alone does not prove server-side enforcement. Use documented/observed direct URLs and state checks where the case requires them; disclose limits of ordinary browser navigation.
- Do not weaken a failed test, modify app code, fabricate screenshots, infer unobserved backend state, or count an interrupted case as PASS.

6. Record every actual attempt

For each case preserve Test ID, run/attempt IDs, start/end timestamps, actual roles and record IDs, before-state evidence, decisive action/error screenshots, final/persistence screenshots, available native CUA traces, and a readable timestamped action summary. Distinguish native tool exports from an authored action summary. Do not invent raw response IDs.

Complete the acceptance-criterion observations using SATISFIED/VIOLATED/UNOBSERVED and evidence paths. Append full attempts to results/attempts.json before updating results/results.json. Maintain fixture_bindings.json, environment.json, checkpoint.json, upload_ledger.json and evidence hashes. Keep exactly one current row for each of the 472 IDs. Missing downloadable evidence must be disclosed; never replace it with generated images.

7. Publish to GitHub after every batch

I authorize uploading this frozen benchmark and all genuine evaluation results/evidence to KateK77/athenaone-clone.

- Preferred branch: evaluation/athenaflow-v3-independent-cua-472, based on the identified V3 source commit.
- Preferred path: experiments/round-03/cua-evaluation/athenaflow-v3-independent-472/.
- Inspect any existing branch/path first. Resume if hashes match. If unrelated/incompatible content exists, use a uniquely suffixed nonconflicting path/branch and explain it; never overwrite or force-push.
- Commit the frozen benchmark before execution when GitHub is available. After each pilot/batch, commit the case outcomes, screenshots/trace files, evidence index, environment, summary, block/failure details and resume checkpoint. Use reports/batch-001/, batch-002/, etc.
- Push without force. Verify the remote commit SHA and result links. A local commit is not an upload. If permission/connectivity is unavailable, preserve the batch and mark UPLOAD_PENDING, continue independent work, and request only the missing connection/access.
- Preserve original descriptions, V1/V2 history, other benchmarks and all application code. Do not merge PRs, change visibility, deploy or delete prior evaluations.
- Add/update a concise plain-text evaluation index with the tested version, results and evidence links. Do not use colorful badges or claim completion early.

8. Report truthful statistics and final artifacts

Use P=PASS, F=FAIL, B=BLOCKED, U=NOT_RUN and N=472:
- Evaluated pass rate = P/(P+F), or N/A if none evaluated.
- Execution coverage = (P+F)/472.
- Suite success fraction = P/472.
- Report P/F/B/U overall, by module, and by difficulty. Include interruption and evidence-gap counts.
- Preserve first-final-outcome versus current-outcome results when retries exist. Separate different application versions/run segments; never pool them silently.
- Do not count setup/hash/unit/Playwright checks in the 472 CUA denominator.

When finished, publish and provide AthenaFlow_V3_CUA_Final_Results.zip containing the original frozen cases, all results and attempts, summaries, screenshots/actual action evidence, environment/provenance, fixture limitations, upload ledger and GitHub links. If execution remains incomplete, label the archive/report partial and identify the exact pending IDs and restart point.

Start now with validation and target discovery, then the 10-case CUA pilot. Keep me informed in Chinese. Continue in batches automatically without routine approval questions.
