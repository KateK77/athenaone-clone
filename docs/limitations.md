# Known limitations and unimplemented requirements

The original brief describes a much larger enterprise product than this version. Do not score this repository as full completion of that specification.

## Clinical and data limits

- Only fictional patients and a small curated code/test catalog are included. It is not a complete licensed ICD/CPT/HCPCS or medication terminology database.
- No medical-device validation, HIPAA compliance assertion, or clinical suitability is claimed. Medication allergy/duplicate checks are simple deterministic examples, not a drug safety system.
- Lab panels show one selected component per order; there are no multi-analyte panels, specimen accession records or real instrument interfaces.
- History, immunizations and documents are editable text records. Binary file uploads, scanned consent documents and structured vaccine administration are not implemented.
- Notes have one current document per encounter, version snapshots and addenda. There is no rich-text editor, collaborative editing, background autosave or complete clinical macro library.
- Ready for Sign-off is a checklist gate rather than a separate persisted encounter state. Clinical diagnoses linked to signed visits preserve coding; longitudinal status/notes can be updated without altering the signed SOAP text.
- Patients can see their own signed summaries and released results; there is no self-service account enrollment, identity proofing, proxy access, MFA, password-reset email or portal invitation flow.

## Scheduling and operational limits

- Availability is weekday start/end hours. Holidays, clinician leave, lunch breaks, recurring blocks, resources/rooms, overbooking policies, drag-and-drop and video visits are absent.
- Calendar views group interactive chronological blocks; they are not a time-proportional grid.
- Rescheduling updates a booking with audit provenance rather than retaining a distinct Rescheduled lifecycle record.
- Waitlist matching is first-fit with a 90-day search bound. Notifications are local tasks, not actual SMS, email or push deliveries.
- Dashboards are role-aware but use a compact set of metrics rather than every role-specific card in the brief. The practice identity is fixed to the one fictional practice.
- No background scheduler, external job worker or independently configurable workflow automation engine is implemented.

## Financial limits

- All payer, insurance, pharmacy and payment interactions are local simulations. No real transaction endpoint or card storage exists.
- One claim is permitted per encounter. Professional/institutional electronic claim formats, remittance files, line adjudication, contractual adjustments, coordination of benefits, refunds, write-offs are not modeled. V2 adds an explicit billing-confirmed patient responsibility amount; this is not payer-derived line adjudication.
- Charge amounts may be manually entered; claim scrubbing does not provide clinical coding advice or actual payer policy validation.
- Payments allocate to a single claim. Copays larger than the claim remain unallocated and need future credit/refund workflow support.
- Receipt previews and portal balance lists exist; a formal printable statement-generation engine is missing.
- Denial management supports reason/category, appeal text, due date, correction and resubmission. Dedicated appeal documents, denial-specific assignment/aging analytics and external appeal submission are not implemented.
- Authorization is text-supported simulated review. Real attachments and payer-specific rule engines are absent. Authorization expiration is checked during workflow validation, not proactively updated by a background job.

## AI, interoperability and security limits

- Only deterministic text demo mode exists. Optional live LLM mode, audio capture/transcription, diagnosis/order suggestions and a separate AI coding assistant are not implemented. The assistant never generates validated medical advice.
- FHIR-inspired exports are partial representations, not formally validated FHIR R4 resources or a conformant server. No SMART on FHIR, HL7 transport, bulk import/export or terminology server is included.
- Role and patient scope enforcement is tested, but this is a single-practice application, not a multi-tenant security boundary.
- Audit rows are read-only through the UI, but database operators can alter them. There is no cryptographic log verification, centralized SIEM, intrusion detection, full login-attempt logging or external error-monitoring integration.
- Public demo credentials intentionally grant access to synthetic shared state. A public portfolio deployment should contain no real user or patient information.
- SQLite provides no row-level `SELECT FOR UPDATE` behavior. PostgreSQL is required for deployment and must be used for concurrency/load verification; local tests do not prove high-concurrency safety.

## Delivery and evaluation limits

- Local test results and browser screenshots are recorded in the test report. Remote CI, PostgreSQL runtime, and Render deployment must be reported separately from local SQLite results.
- Playwright is browser automation, not a genuine Computer Use Agent evaluation. No CUA evaluation has been performed.
- Accessibility has semantic labels, focusable controls, responsive layouts and basic keyboard tests; there is no independent WCAG audit.
- No load test, recovery drill, penetration test or regulated-system validation has been performed.

## V2-specific boundaries

See [V2 iteration](v2-iteration.md) for polling behavior, legacy read receipts, unit storage precision and current selector scale. Full Description V2 preserves all original requirements; remaining enterprise features above are not implicitly marked implemented by the V2 feedback fixes.
