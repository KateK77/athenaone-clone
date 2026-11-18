# V2 iteration record

## Specification and history

- `description_v1.md` is a byte-for-byte copy of `docs/original-brief.txt`; the original remains unchanged.
- `description_v2.md` is a standalone English specification containing every original product section with integrated V2 requirements. It is not a changelog.
- V1 remains available in Git history at `7240b17f540b6f05e523a1faa463e49499416408` (application validation baseline `b4eeef2d74d4e141393aec804039617356370090`). V2 continues on `main` in the same repository.
- The full enterprise specification remains broader than this research implementation. The inherited gaps in `limitations.md` remain explicitly tracked rather than removed from Description V2.

## Feedback implementation map

| Area | Implementation | Verification |
|---|---|---|
| Patient selection | Search by full name or MRN; name/MRN/DOB labels; scoped native select with keyboard behavior and no-match feedback; preserve preselection | Backend scope check; browser name/MRN/empty-result/keyboard checks |
| Related records | Diagnosis choices identify patient/MRN/encounter and filter to a supplied encounter | Server form validation and existing workflow regression |
| Discoverability | Insurance coverage, Add insurance, Add diagnosis, Add order, Messages navigation and topbar entry | Existing end-to-end workflow updated to explicit action labels |
| Activity histories | Format transitions, copays and other structured details as readable text without changing underlying audit data | Audit list and detail-page assertions |
| Claim validation | Not yet validated distinguished from clean or failed validation; no raw arrays | Draft/validated presentation checks |
| Units | New intake defaults to in/lb; cm/kg remain available; live conversion and BMI preview; canonical metric storage plus display-unit metadata | Decimal conversion, bounds, legacy compatibility, invalid form retention, four browser round trips, save/reload |
| Intake clarity | Inline measurement units, pain scale, explanatory intake text and readable checkbox targets | Browser intake flow; true/false persistence checks |
| Narrow layouts | Clinical card remains visible, profile menu anchored within viewport, long message content wraps | Mobile vitals and logout at 390/700/1280 pixels |
| Workflow states | Scheduled documentation at check-in, explicit separate appointment/documentation status, physician-only start | Server service permission and transition tests |
| Messages | Subject/body sent atomically; per-user read receipts; unread thread styling and counts; active-page polling every 20 seconds and on focus | Scoped unread endpoint, read isolation, compose validation, browser patient/physician round trip |
| Patient billing | Separate confirmed patient responsibility; staff confirmation after adjudication; denial is not automatically patient debt | Denied/closed/zero balance, unauthorized confirmation and share-bounded payment tests |
| Money formatting | Common currency formatter for reports, trends, aging, bills and receipts | Rendering regression and visual verification |
| Remaining manual uncertainties | Direct patient access restrictions and report filter/CSV matching covered automatically; checkbox persistence verified rather than assumed faulty | Isolated regression tests |

## Data compatibility and migration

No reset or reseeding is required for an existing installation. Stop the local server, back up SQLite (or use the deployment database backup process), run `python manage.py migrate`, then restart.

Additive schema changes:

- Vital signs gain `height_unit` and `weight_unit`. Existing rows are explicitly cm/kg; numeric measurements are not converted in place. New forms default to in/lb, normalize into the existing metric columns and record selected units. Legacy POST clients omitting units retain metric semantics.
- `MessageRead` stores a unique message/user receipt. The existing `Message.read` flag remains as an aggregate sender-facing receipt. Old aggregate flags cannot identify which staff member read a message; old messages can therefore appear unread once to individual staff after upgrade. No fabricated per-user history is backfilled.
- Claims gain nullable `patient_responsibility`. Existing financial amounts and payments remain intact. An unset responsibility is displayed as awaiting billing review; billing can explicitly confirm an amount before the patient pays.
- New encounters default to Scheduled. The data migration normalizes only old unsigned, completely blank encounters whose appointments have not started. Signed notes, authored drafts and closed encounters are preserved.

The local launcher defaults to port **18310**, matching the acceptance-test site. `./start.ps1 -Port 18311` chooses another port.

## Validation record

See `v2-test-output.txt` for the final executed suite and `v2-validation.json` for the delivery checks. Browser tests run against an isolated live-test server and temporary database; they do not alter the local acceptance patient. Playwright remains distinct from a Computer Use Agent evaluation.

The first sandboxed browser attempt could not start its driver and was interrupted. An approved run outside the sandbox exposed three new-test fixture errors (synchronous ORM access after Playwright's event loop started). The fixtures were moved before browser initialization; no production authorization checks were disabled to pass tests.

V1 manual evidence covers the completed Iteration Check journey through closed claim CLM-00161 and the Jamie Alder message round trip. V2 automated results are reported separately. No new manual user acceptance is claimed.

## Remaining limits

Messages poll while a page is visible; this is not WebSocket, email, desktop push, or SMS delivery. Patient selectors filter the already authorized options loaded into the form, suitable for the current synthetic data size; they are not a large-dataset remote autocomplete API. Monetary responsibility is a simple explicit billing assignment, not line-level adjudication or contractual adjustment accounting. The portal does not provision a login for newly registered patients. The original limitations on live AI, uploads, lab panels, external integrations, deployment and independent security/accessibility audits remain; consult `limitations.md`.

Final local suite: **114 executed, 114 passed, 0 failed, 0 skipped** (101 backend/integration and 13 Chromium tests). System checks and migration drift checks passed. Local SQLite upgrade preserved the original column values in 13 business tables; counts include 101 patients, 151 appointments, 101 encounters, 81 claims and 32 payments. The existing demonstration server is available on port 18310.

The final regression also covers two independent browser sessions: a new clinician reply updates the patient message badge without reload. Initial badge counts are rendered by the server; polling avoids redundant requests during navigation. An intermediate repeat showed intermittent page failures; server exception capture and explicit page assertions were added and the final suite was rerun after polling changes.
