# Research evaluation protocol

## Reproducibility

Record the Git commit, Python/Django/browser versions, OS, database backend, environment flags, timezone, and `seed_demo --anchor-date`. Retain the original brief separately from implementation decisions. Do not alter fixture behavior to make a particular hidden evaluator pass.

The seed command is separate from runtime services. Normal workflows never consult a hidden fixture-success flag. Tests use isolated databases. Public demo records can be changed through ordinary visible UI interactions.

## Suggested evaluation cases

| Case | Initial state | Visible actions | Expected persisted result |
|---|---|---|---|
| Register and schedule | No matching patient | Search → register → add/verify policy → book | Patient, unique MRN, policy and appointment appear after reload |
| Prevent double booking | Existing provider slot | Book an overlapping visit | Clear error; no second appointment |
| Check-in | Arrived appointment, active policy, consent | Complete checklist and copay | Checked In, new encounter/note/task, one copay |
| Clinical sign-off | Open encounter | Record intake/vitals, diagnosis, SOAP; sign | BMI shown; signed timestamp/clinician/version; note locked |
| Draft conflict | Same note open in two sessions | Save in one then save stale version | Second save blocked, first retained |
| Results privacy | Published unreleased lab | Patient attempts view, physician reviews/releases | Hidden before release, visible afterward only to owner |
| Financial progression | Signed encounter, approved charge | Generate/scrub/submit/adjudicate claim | Deterministic status history and accurate balance |
| Denial recovery | Denied claim | Appeal → correct → revalidate → resubmit | Corrected denial and processed replacement attempt |
| Payment protection | Positive adjudicated balance | Excess payment, then valid amount, then replay | Excess/replay rejected; valid balance reduced once |
| Patient message | Linked patient account | Create thread, send, staff reply | Thread persists; staff task and read state update |
| Unauthorized action | Nurse/front desk/patient role | Direct protected URL or POST | Server-side 403/404; no forbidden mutation |

## Evidence and scoring

For each case retain initial record identifiers, screenshots/video if collected, user-visible messages, final record state, and relevant audit events. A successful navigation or screenshot alone is not evidence of workflow completion. Test persistence after reload and a fresh login.

Score features using `docs/features.md`: Implemented means the specific described core behavior exists; Partial means the original module also has significant omissions; Missing means it is absent. Do not convert a module's passing smoke test into full functional coverage.

Calculate pass rate as **Passed / Executed × 100%**. List skipped, blocked, not-run and failed separately. A skipped PostgreSQL or CUA run is not a local test pass. Playwright and CUA are distinct evaluation methods. The checked-in browser tests use semantic selectors and visible controls; a future genuine CUA should operate independently through the rendered application.

## Architectural deviations to track

Four domain apps replace the suggested many-app tree; contacts/consent are consolidated fields; one result component per order; current claim lines derive from locked charges; no live AI provider; explicit save instead of autosave; single fictional practice; static weekday availability; text documents instead of files. These are documented scope reductions, not equivalent implementations of omitted requirements.
