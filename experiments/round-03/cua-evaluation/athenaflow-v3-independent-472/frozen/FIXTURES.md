# Synthetic fixture contract

These are required data shapes, not claims that seed records already exist. The suite contains no invented live record IDs, passwords, target URL, deployed SHA, or pre-executed results. All data are fictional. Evaluate application behavior, not medical appropriateness.

## Binding workflow

1. Read existing demo/seed documentation, role mapping and deterministic simulator rules during preflight. Record public demo credentials securely where appropriate; use the supplied public demo identities, not personal accounts.
2. Inspect actual records through CUA and bind patient A/B, encounters, orders, claims, policies and messages in `results/fixture_bindings.json`. Record current state plus screenshot references. A/B are local aliases for each case, not universal patients shared unsafely across all 472 cases.
3. Prefer fresh UI-created records with `AF3_<RUN_ID>_<TEST_ID>` markers for mutations. When preconditions require historic timestamps, malformed records impossible to enter through validated forms, or multiple read-isolated staff, use existing documented synthetic fixtures. Existing official seed/reset commands may initialize a separate evaluation database before the run, with command/version recorded; this is setup, not CUA evidence. Do not create custom backdoor endpoints or weaken form validation.
4. Do not change production/live shared data, clocks, application source, migrations, or backend records to force an outcome. If an existing documented setup mechanism cannot supply a necessary fixture and the normal UI cannot create it, mark the affected case BLOCKED/FIXTURE_UNAVAILABLE. Do not block the whole suite and do not treat an impossible malformed input as evidence of the downstream scrub rule.
5. Discover direct URLs from authorized UI or actual documentation. Bind exact URLs for unauthorized tests and note origin; no guessed IDs or endpoints.
6. Reused fixture state must still satisfy the next case's preconditions. Use separate records when a mutation could contaminate later tests. Never silently reset the whole app between cases.

## Standard input values

| Item | Value or binding rule |
| --- | --- |
| Name | Fictional `Avery AF3 <test-id>` and `Avery AF3 Similar <test-id>`; full identity must remain readable |
| MRN | Unused deterministic `AF3<run suffix><case number>` within documented field format; record actual accepted value |
| DOB | 1988-04-12 for A, 1992-09-23 for B; choose adult synthetic fixtures if existing records used |
| Contact | Example-domain email such as `af3.039@example.com`; synthetic phone 202-555-0147; fictional address |
| Allergy | Synthetic penicillin allergy, rash; use documented simulator-triggering catalog item |
| Transcript | `The patient reports a headache for two days. The clinician reviewed the existing penicillin allergy. No examination measurements or treatment decisions were supplied in this transcript.` |
| Note markers | `AF3 <test-id> subjective`, `AF3 <test-id> assessment`, `AF3 <test-id> plan`; clinically inert synthetic documentation |
| Baseline vitals | BP 120/80 mmHg, HR 72 bpm, RR 16 breaths/min, T 36.8 Celsius, SpO2 98%, height 65 in, weight 150 lb, pain 2/10; BMI 25.0 |
| Metric BMI fixture | 170 cm and 70 kg gives BMI 24.2 after one-decimal display rounding |
| Precision fixture | 65.37 in = 166.0398 cm; 147.29 lb = 66.8096201773 kg, canonical boundary 66.80962018 kg; UI metric displays 166.04 cm and 66.81 kg |
| Conversion factors | 2.54 cm per inch; 0.45359237 kg per pound; do not recompute from rounded displayed values |
| Synthetic payment | Base claim 200.00, confirmed patient responsibility 80.00; payment 30.00 yields total balance 170.00 and responsibility 50.00 |
| Copay | 25.00; unlinked provider-B comparison copay 40.00 |
| Charge pair | 125.00 + 75.00 = 200.00 |
| Money boundary | For balance 50.00, 50.01 is overpayment; for responsibility 40.00, 40.01 exceeds patient responsibility |
| Normal viewport | 1440x900 at 100% browser zoom; actual dimensions must be recorded |
| Narrow/mobile viewport | 390x844 at 100% browser zoom; resize browser/device viewport using available genuine UI, never injected scripts |
| Tablet viewport | 768x1024 at 100% browser zoom |

## Stateful fixture families

- **Roles:** all nine required roles; admin, manager, frontdesk, physician, nurse, assistant, billing, coder and patient. Some isolation tests require a second authorized staff reader, another physician with different assignment, and a second linked patient account. Provision through existing administration UI when permitted. Role labels for laboratory processing are not dictated in Description V3; record the application's documented authorized processing role rather than inventing a new required lab account.
- **Patients:** similar names/different MRN+DOB, one long name, assigned/out-of-scope patients, active/inactive status, a new empty chart, a chart with all history categories, and one with clearly absent measurements.
- **Scheduling:** documented future available slots, unavailable interval, same-provider overlap and adjacent interval, two providers at same time, past no-show-eligible appointment, appointment states including cancelled/completed/checked out, configured durations, waitlist preferences and matched slots. D means a recorded concrete date in application timezone; choose future dates for booking and historical fixtures for missed/completed visits. Record all actual date bindings before action.
- **Check-in/clinical:** missing required consent/registration item, partly completed check-in, roomed patient, scheduled encounter with authored draft, complete signable note, missing diagnosis/acknowledgment, blocking order state if defined, signed immutable note and closed encounter. Do not infer a missing sign-off order policy; use documented behavior and disclose ambiguity.
- **Diagnosis/medication:** curated code catalog entries, active/resolved problems, primary and secondary diagnoses, active/discontinued medications, documented duplicate/allergy trigger and non-trigger. Do not require a full licensed terminology catalog.
- **Orders/results:** each supported order category and lifecycle; pending/specimen/processing/completed lab work; released/unreleased results; six lab examples; known abnormal fixture. Processing failure must use an existing deterministic simulator path; do not induce server failures by tampering.
- **Insurance:** primary and secondary policies, Active/Inactive/Not Found/Pending/Error deterministic eligibility fixtures, expired coverage, incomplete member-ID fixture, unverified appointment and authorization-needed service. Record the actual scenario selector or documented trigger; no invented member-ID magic strings.
- **Billing:** approved/unapproved charges, known unit-price semantics, duplicate service candidate, clean claim and each individual scrub defect, Submitted/Accepted/Rejected/Denied/Adjudicated/Partially Paid/Paid/Closed fixtures, known deterministic payer outcomes. Malformed claims missing required provider/demographics may require a documented seeded fixture because valid UI should prevent creating them.
- **Denials/authorizations:** seven denial reasons; open/resolved appeal workflow; authorization Draft/Submitted/Pending/Additional Information/Approved/Denied/Expired; matching and wrong-service approvals. Appeals are draft simulations, not real submissions.
- **Payments:** unconfirmed versus separately confirmed responsibility, full/partial/no balance, invalid claim state, two-tab stale form and historical receipts. Each payment case uses fresh balances; do not repeatedly consume one shared 200.00 claim.
- **Messages:** two patient scopes; two independently authenticated staff readers for per-user read state; old read thread with new reply; multiple messages; paginated/unloaded messages only if supported. If the UI renders all messages, the displayed-only read case explicitly accepts all rendered messages being marked read and records that no hidden-message variant was tested.
- **Reports:** bind a period `[R_start, R_end]` in app timezone. Required seeded dates include: encounter before range with latest claim submission inside; initial submission inside but latest resubmission outside; payment posting inside/outside independent of encounter date; linked/unlinked copays for different providers/departments; current outstanding old-encounter claim outside selected cohort; documented aging dates. Prefer existing historical fixtures; normal UI often cannot alter creation/submission timestamps. Do not change application clock or DB fields during evaluation. Record fixture inadequacy per case.
- **Interop:** actual documented endpoint routes and resource mappings. Description only requires selected synthetic records and does not establish universal resource coverage, standards conformance, or authorization scope beyond application privacy rules. If a named required resource representation is absent after checking documented scope, record missing-feature FAIL; do not guess a route.
- **Reset:** isolated designated synthetic DB with baseline seed recorded; complete evidence export before reset; create one disposable marker. If isolation cannot be established, block only AF3-447 with reason RESET_SCOPE_UNSAFE. Never reset a live shared or production database.

## Cleanup and environmental controls

Record initial relevant counts and IDs. Do not require globally pristine counts; compare within a scoped patient/provider/period or use before/after deltas. Unknown concurrent writers invalidate exact count comparisons; disclose interference rather than assigning a favorable outcome. Create an isolated run if practical. No source fixes during evaluation. Existing historical records must not be rewritten to imitate successful previous tests.
