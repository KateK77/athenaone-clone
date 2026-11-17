# Database schema

The schema is defined by checked-in Django migrations. Foreign keys use `PROTECT` for records that must survive clinical/financial references and `CASCADE` for owned child data. Each table has a surrogate primary key.

| Domain | Tables / entities | Relationships and constraints |
|---|---|---|
| Organization | Practice, Department, Provider | Department belongs to practice; provider belongs to department; optional unique provider user; configured weekday start/end hours |
| Identity | Django User, Profile, Session | One profile per user; explicit role; optional department; passwords use Django hashing |
| Patient | Patient, InsurancePolicy | Unique MRN, unique exact name/DOB combination; case-insensitive duplicate detection in validation; optional unique patient user; multiple policies |
| Schedule | AppointmentType, Appointment, CheckIn, WaitlistEntry | Provider, patient, department, visit type; one check-in per appointment; optional booked waitlist appointment; provider-lock overlap validation |
| Encounters | Encounter, ClinicalNote, NoteVersion, Addendum | One encounter per appointment; one current SOAP note per encounter; unique historical note/version pair; signed notes protected against editing |
| Clinical context | DiagnosisCode, Problem, Allergy, History, VitalSign | Problems may link an encounter; history has medical/surgical/family/social/document/immunization categories; vitals belong to encounter and author |
| Medication | Medication | Patient/provider, dose, strength, route, frequency, dates, quantity, pharmacy, signing timestamp and lifecycle state |
| Orders/results | MedicalOrder, LabResult | Order requires encounter and diagnosis, optional authorization; one selected-component result per order; explicit reviewer and release flag |
| Billing | ProcedureCode, Charge, Claim | Curated procedure amounts; unique encounter/procedure charge; one claim per encounter; charge diagnosis links to encounter diagnoses through validation |
| RCM | Denial, Authorization, Payment | One denial per claim; policy and provider on authorization; payment links claim or visit copay; unique receipt reference; positive amount DB constraint |
| Engagement | Task, MessageThread, Message, AppointmentRequest | Tasks carry role/user/patient and related local URL; messages belong to one patient's thread; appointment requests link their booked appointment |
| AI | AIDraft | Encounter, transcript, structured JSON output, author, model/prompt versions, approval status |
| Audit | AuditEvent | Actor, entity label, object ID, detail JSON, timestamp; append through application service |

## Calculations

- BMI = weight in kg / (height in meters squared), rounded to one decimal place.
- Claim total = sum of charge amount × units for the encounter.
- Claim balance = total − sum of claim-linked payments. No financial values use binary floats.
- Copays are recorded at completed check-in and allocated to the encounter claim when created, if no greater than its charge total. Excess visit credits remain unallocated; automatic overpayment refunds are not implemented.
- Denial rate = currently Denied claims / all claims in selected service-date scope. This is a current-state rate, not a historical denial-incidence rate.
- Acceptance rate = submitted claims in accepted/adjudicated/paid/closed/partially-paid/denied states / claims with a submission timestamp.
- A/R aging uses claim creation date and current balance. It is not a historical as-of ledger.
- Availability utilization uses booked, non-cancelled/non-no-show minutes divided by configured weekday office minutes in the selected range. Holidays, leave and lunch blocks are not modeled.

## Intentional consolidations

Patient contacts/emergency contact/consent are fields rather than separate child tables. Document and immunization entries are typed history records rather than binary file resources. Medication and prescription share one lifecycle model. Claim lines are derived from protected encounter charges rather than copied into a separate snapshot table; charges are locked after validation. Payments each target one claim rather than a many-claim allocation ledger. Task links are local URLs rather than generic foreign keys. A single-practice scope is assumed; this is not a tenant isolation design.

## FHIR-inspired mappings

Authenticated read-only `/fhir/<resource>/<id>/` endpoints expose:

| Resource | Internal source | Included fields |
|---|---|---|
| Patient | Patient | MRN identifier, name, DOB, gender mapping |
| Appointment | Appointment | Patient reference, status mapping, start/end |
| Encounter | Encounter | Patient reference, status, start period |
| Condition | Problem + DiagnosisCode | Patient reference, code/display, status text |
| Observation | VitalSign | Patient reference, vital components, timestamp |
| MedicationRequest | Medication | Name/strength, dose/frequency text, status |
| ServiceRequest | MedicalOrder | Test name, intent, status |
| DiagnosticReport | LabResult | Test name, selected value, units, interval, flag |
| Coverage | InsurancePolicy | Member ID, payer display, coverage period/status |

All resources include a synthetic/nonconformant metadata tag. These are educational representations, not a validated FHIR server: no bundles, search parameter contract, SMART OAuth, terminology validation, or formal conformance declaration is provided.
