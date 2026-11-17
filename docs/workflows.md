# Workflow walkthroughs

Use the nine public demo roles and the in-app `/help/` guide. Every mutation below persists across reloads and sessions. Dates should be weekdays during the chosen provider's configured office hours.

## Registration → clinical encounter → claim

1. Sign in as `frontdesk.demo`. Search Patients by name/MRN before selecting **Register patient**. Enter fictional demographics, a primary provider, and consent.
2. From the chart's Coverage panel, add a policy. Demo valid member IDs have two uppercase letters and 6–12 digits. Dates must cover the visit. Open the policy and choose **Verify eligibility**. `ERR` prefix produces Verification Error; empty IDs produce Coverage Not Found in the simulator; dates outside coverage produce Inactive.
3. Book an appointment in the matching provider department. Overlaps and out-of-hours appointments produce errors without a partial booking.
4. Open the appointment. Advance Scheduled → Confirmed → Arrived. Open **Complete check-in**, verify all five checklist items and enter an optional simulated copay. Active coverage and registration consent are required. Success creates an encounter, draft note and intake task, and sets Checked In.
5. Sign in as `nurse.demo` or the appropriate department clinician. Open the encounter, record intake and vitals, and complete medication/allergy/history reconciliation. BMI is calculated. Move the appointment to Roomed.
6. Sign in as the assigned physician. Move the appointment to In Progress. Add an encounter diagnosis, including a primary code. Save all SOAP sections. Use templates, copy-forward or the deterministic scribe only after reviewing their provenance and completing placeholders.
7. Add orders if needed. Sign or cancel all drafts before signing the note. Confirm review and select **Sign saved note**. The note becomes immutable, a coding task is created, and further corrections use an addendum. **Close encounter** closes the note workflow and completes an In Progress appointment.
8. Sign in as `coder.demo`. Open the signed encounter. Add a procedure charge with an encounter diagnosis and amount; approve the charge. Select **Generate claim**. An existing claim is not duplicated. Applicable visit copays are allocated.
9. Review and validate the claim. Errors block submission; warnings are displayed separately. Correct demographics, coverage, codes or authorization as indicated.
10. Sign in as `billing.demo`. Submit → Payer response → Adjudicate. Scenario `Pay` settles the remaining balance; `Partial` pays 70% of the remaining amount; `Deny` creates a denial work item; `Reject` stops at Rejected. Close a fully paid claim if desired.

## Orders → results → portal

An assigned physician creates an order linked to a diagnosis and signs it. A nurse/physician moves it to Processing. For laboratory orders, **Enter lab result** captures a selected component, unit, reference interval and supplied flag. Saving creates the result and completes the order. Publish creates a physician result-review task. The physician reviews, then explicitly releases it. Only released, reviewed results are shown to the linked patient. No numerical diagnostic interpretation is generated.

## Denial → correction → resubmission

Open the denial, edit the appeal text, and save supporting information. Return to the claim and choose Correct. This records the denial as Corrected, moves the claim back to Draft, and sets the deterministic resubmission scenario to Pay. Required authorization and other scrubbing checks still apply. Review, validate, submit and adjudicate again. No actual payer transmission occurs.

## Payments

For an adjudicated, denied, partially paid or paid claim, billing or the owning patient can open **Post / Make simulated payment**. Amount must be positive, at most two decimals, and no greater than the outstanding balance. Patient accounts can post only Patient-source payments. A form token and unique reference prevent duplicate posting. The receipt displays the recorded amount, patient, source, claim and timestamp. No card field exists; no money moves.

## Portal requests and communications

`patient.demo` maps to Jamie Alder only. An appointment request creates a front-desk task and a Requested row. Front desk opens the request and books a validated slot; the request becomes Booked. Pre-check-in records demographics/consent readiness but does not bypass staff check-in requirements. Renewal requests create physician tasks. New message threads are automatically bound to the signed-in patient. Patient messages create nurse tasks; staff responses complete them. Reading a thread marks received messages read.

## Waitlist

Front desk adds a patient, preferred provider and date range. **Find & book slot** searches weekdays in 30-minute increments, bounded to the next 90 days of the requested range. It uses the same conflict validation as normal scheduling, books the first matching slot, and creates a simulated notification task. No email or SMS is sent.

## Explicit state boundaries

- Appointment: Scheduled → Confirmed/Arrived → Checked In → Roomed → In Progress → Completed → Checked Out. Cancellation/no-show branches apply only to specified early states. Rescheduling changes the booking time and records the previous/new start in audit history; it does not create a separate Rescheduled appointment record.
- Encounter: In Progress → Documentation Pending → Signed → Closed. Ready for Sign-off is represented by the sign-off checklist rather than a persisted separate state.
- Order: Draft → Signed → Processing → Completed; defined cancellation/failure branches.
- Result: Entered → Published → Reviewed → explicit released flag.
- Claim: Draft → Ready for Review → Validated → Submitted → Accepted → Adjudicated → Paid/Partially Paid/Denied → Closed where allowed; failed validation and rejected/denied correction branches.
- Authorization: Draft → Submitted → Pending Review → Approved/Denied/Additional Information Requested. A request for more information can be resubmitted. Expired approvals are rejected by scrubbing; no background expiration scheduler is present.
