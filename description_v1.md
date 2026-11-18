# PROJECT: athenaOne-Inspired Healthcare Platform — Full-Stack Software Reconstruction

## 1. Project Overview

You are an autonomous senior full-stack software engineer, healthcare software architect, UI/UX designer, database engineer, and QA engineer.

Your task is to design and implement a comprehensive, production-style educational simulation of athenaOne, the integrated healthcare software platform developed by athenahealth.

The application should reconstruct the major workflows and product concepts of athenaOne, including:

1. Electronic Health Records (EHR)
2. Practice Management
3. Appointment Scheduling
4. Patient Registration
5. Insurance and Eligibility
6. Clinical Encounters
7. Nursing and Clinical Intake
8. Medical Orders
9. Laboratory Results
10. Medication Management
11. Medical Billing
12. Revenue Cycle Management
13. Claims Processing
14. Denial Management
15. Prior Authorization
16. Patient Engagement
17. Patient Portal
18. Clinical AI Assistant
19. AI-Powered Documentation
20. Analytics and Reporting
21. Administrative Management
22. Role-Based Access Control
23. Audit Logging
24. Clinical Workflow Automation
25. Healthcare Data Interoperability

The final application should feel like a coherent, realistic healthcare enterprise platform.

This is an independent educational and research-oriented reconstruction using synthetic healthcare data.

Do not represent the application as an official athenahealth product.

Do not copy proprietary source code, restricted assets, private APIs, real patient information, or copyrighted brand artwork.

Use an original application identity, such as "AthenaFlow — Healthcare Practice Platform."

The product may be described as "inspired by the workflows of athenaOne."

---

# 2. Research Objectives

This project is part of a larger research initiative investigating the capability of AI coding agents to generate complex software systems from natural-language specifications.

The research will evaluate:

- Functional completeness
- Workflow correctness
- Clinical data consistency
- User interface quality
- Data persistence
- Cross-module integration
- Role-based authorization
- Error handling
- Software reliability
- Agent-generated implementation quality
- Computer Use Agent evaluation performance

The software must therefore be both visually convincing and functionally testable.

Every major interactive feature should have observable, persistent behavior.

Avoid static mockups disguised as functionality.

---

# 3. Technical Architecture

## 3.1 Preferred Technology Stack

Use:

Backend:
- Python 3.13 or a compatible supported version
- Django 5.2 LTS
- Django ORM
- Django authentication framework
- Django migrations

Frontend:
- Django templates
- HTML5
- CSS3
- JavaScript
- Responsive desktop-first layout
- Reusable UI components

Database:
- SQLite for local development
- PostgreSQL-compatible database architecture for deployment

Testing:
- Django TestCase
- pytest where useful
- Playwright
- Browser-based end-to-end testing

Deployment:
- GitHub repository
- Render-compatible configuration
- Environment-variable-based settings
- Automated database migrations
- Synthetic demo-data initialization

Use a modular Django monolith unless the project requirements strongly justify a different architecture.

Prioritize maintainability, simplicity, reliability, and testability.

Do not introduce unnecessary infrastructure.

## 3.2 Suggested Project Structure

athenaflow/
- config/
- accounts/
- dashboard/
- patients/
- scheduling/
- registration/
- insurance/
- encounters/
- clinical/
- nursing/
- orders/
- laboratory/
- medications/
- billing/
- claims/
- authorizations/
- denials/
- portal/
- messaging/
- analytics/
- ai_assistant/
- audit/
- interoperability/
- templates/
- static/
- tests/
- docs/

The precise structure may be improved when justified.

---

# 4. Application Design and User Experience

## 4.1 Overall Design Direction

The interface should resemble a professional American ambulatory healthcare software platform.

Design characteristics:

- Clean enterprise healthcare interface
- White and light-gray background
- Restrained blue and teal accent colors
- Clear information hierarchy
- Dense but readable tables
- Professional typography
- Consistent spacing
- High-contrast status indicators
- Persistent navigation
- Context-aware actions
- Accessible forms
- Desktop-first responsive design

Avoid:
- Generic startup landing-page aesthetics
- Excessive gradients
- Decorative animations
- Oversized empty cards
- Unnecessary whitespace
- Inconsistent visual components
- Dead navigation links

The product should prioritize operational efficiency and clinical usability.

## 4.2 Global Application Layout

The authenticated application should include:

### Top Navigation Bar

- Application name
- Current practice
- Department selector
- Global patient search
- Notifications
- Tasks
- Help
- Current user
- User role
- Profile menu
- Logout

### Sidebar Navigation

- Dashboard
- Schedule
- Patients
- Encounters
- Clinical Inbox
- Orders
- Results
- Medications
- Billing
- Claims
- Denials
- Authorizations
- Patient Portal Administration
- Reports
- AI Assistant
- Administration
- Audit Logs

Navigation must be role-aware.

### Main Content

- Page heading
- Breadcrumbs when useful
- Search
- Filters
- Action buttons
- Table or workspace
- Status indicators
- Empty states
- Error messages
- Success notifications

### UI Quality Requirements

Implement:

- Loading states
- Form validation
- Confirmation dialogs
- Pagination
- Sorting
- Filtering
- Search
- Inline editing where appropriate
- Keyboard-accessible controls
- Responsive tables
- Clear error recovery

Every visible button must either perform an actual action or be explicitly marked as unavailable.

---

# 5. User Roles and Permissions

Create realistic demonstration accounts for:

1. System Administrator
2. Practice Manager
3. Front Desk Staff
4. Physician
5. Nurse
6. Medical Assistant
7. Billing Specialist
8. Coding Specialist
9. Patient

## 5.1 Administrator

Can:

- Manage staff accounts
- Assign roles
- Configure departments
- Configure providers
- Configure appointment types
- Manage practice settings
- View audit logs
- Reset synthetic demo data

## 5.2 Practice Manager

Can:

- View operational dashboards
- Manage schedules
- Monitor appointment performance
- Review billing performance
- Access practice reports
- Manage appropriate operational settings

## 5.3 Front Desk

Can:

- Register patients
- Edit demographics
- Schedule appointments
- Reschedule appointments
- Cancel appointments
- Check patients in
- Check patients out
- Verify insurance information
- Record simulated copays

Cannot sign physician documentation.

## 5.4 Physician

Can:

- View assigned patient charts
- Review medical history
- Manage diagnoses
- Create encounter notes
- Place medical orders
- Review laboratory results
- Create prescriptions
- Use AI clinical assistance
- Sign and close encounters

## 5.5 Nurse

Can:

- Review assigned worklists
- Record vital signs
- Document intake
- Update permitted clinical observations
- Review medication lists
- Process appropriate clinical tasks

Cannot sign physician-only documentation.

## 5.6 Medical Assistant

Can:

- Room patients
- Record vitals
- Prepare encounters
- Update permitted intake information

## 5.7 Billing Specialist

Can:

- Review claims
- Submit simulated claims
- Post payments
- Manage patient balances
- Investigate rejected claims
- Review accounts receivable

## 5.8 Coding Specialist

Can:

- Review encounter diagnoses
- Assign ICD-10-CM codes
- Assign CPT/HCPCS procedure codes
- Review charge capture
- Correct coding-related claim errors

## 5.9 Patient

Can access only their own:

- Appointments
- Medical summaries
- Released results
- Medications
- Messages
- Bills
- Payment history
- Personal information

Enforce all authorization rules on the backend.

Never rely on UI visibility alone for security.

---

# 6. Dashboard

Create role-specific dashboards.

## 6.1 Physician Dashboard

Display:

- Today's appointments
- Patients waiting
- Encounters in progress
- Unsigned notes
- Pending orders
- Results awaiting review
- Clinical inbox
- Follow-up tasks

## 6.2 Front Desk Dashboard

Display:

- Today's schedule
- Arriving patients
- Checked-in patients
- Missing registration information
- Insurance verification issues
- Copay collection tasks
- Cancellations
- Open appointment slots

## 6.3 Billing Dashboard

Display:

- Unbilled encounters
- Claims awaiting submission
- Rejected claims
- Denied claims
- Outstanding balances
- Payment activity
- Accounts receivable aging
- Billing workqueue

## 6.4 Administrator Dashboard

Display:

- Active patients
- Daily visits
- Provider utilization
- Appointment completion
- Claims submitted
- Denial rate
- Revenue trends
- Operational alerts

Dashboard metrics must be calculated from database records.

---

# 7. Patient Registration and Management

## 7.1 Patient Directory

Implement a searchable patient list.

Columns:

- Patient ID
- Medical Record Number
- Full Name
- Date of Birth
- Age
- Sex
- Phone
- Primary Provider
- Last Visit
- Status

Filters:

- Name
- MRN
- Date of Birth
- Provider
- Department
- Patient Status

## 7.2 Patient Registration

Registration form fields:

- First Name
- Middle Name
- Last Name
- Preferred Name
- Date of Birth
- Sex
- Gender Identity (optional)
- Phone Number
- Email
- Address
- Emergency Contact
- Preferred Language
- Primary Care Provider
- Insurance Information
- Consent Status

Requirements:

- Unique MRN
- Required-field validation
- Duplicate-patient detection
- Search before registration
- Proper field formatting
- Server-side validation
- Audit logging

## 7.3 Patient Chart

Tabs:

1. Summary
2. Encounters
3. Problem List
4. Medications
5. Allergies
6. Medical History
7. Surgical History
8. Family History
9. Social History
10. Vitals
11. Orders
12. Results
13. Documents
14. Immunizations
15. Appointments
16. Billing

Patient charts must display consistent information across modules.

---

# 8. Appointment Scheduling

Build a realistic scheduling workspace.

## 8.1 Calendar Views

Support:

- Daily view
- Weekly view
- Provider view
- Department view

Display appointments as interactive calendar blocks.

Each appointment includes:

- Patient
- Provider
- Department
- Appointment type
- Date
- Time
- Duration
- Reason for visit
- Status

## 8.2 Appointment Types

Examples:

- New Patient Visit
- Established Patient Visit
- Annual Physical
- Follow-up
- Telehealth
- Laboratory Visit
- Procedure Visit
- Urgent Visit

Each appointment type can have a default duration.

## 8.3 Scheduling Operations

Support:

- Create
- Reschedule
- Cancel
- Confirm
- Check in
- Mark arrived
- Mark no-show
- Complete
- View appointment history

Validate provider availability.

Prevent overlapping appointments unless a documented scheduling rule explicitly permits them.

## 8.4 Appointment Lifecycle

Scheduled → Confirmed → Arrived → Checked In → Roomed → In Progress → Completed → Checked Out

Additional states:

- Cancelled
- No Show
- Rescheduled

Use explicit state-transition validation.

Do not allow arbitrary invalid transitions.

## 8.5 Waitlist

Implement:

- Waitlist enrollment
- Preferred provider
- Preferred date range
- Available-slot matching
- Simulated patient notification
- Waitlist booking

---

# 9. Front Desk Check-In

Create a multi-step check-in workflow.

Steps:

1. Confirm patient identity
2. Verify demographics
3. Verify insurance
4. Review consent documents
5. Collect relevant intake forms
6. Record simulated copay
7. Mark patient checked in
8. Add patient to clinical worklist

The interface should indicate completed and incomplete steps.

Prevent completion when mandatory registration requirements are missing.

---

# 10. Nursing and Clinical Intake

## 10.1 Nursing Worklist

Display:

- Patient
- Appointment time
- Provider
- Reason for visit
- Current status
- Intake completion

## 10.2 Vital Signs

Support:

- Blood pressure
- Heart rate
- Respiratory rate
- Temperature
- Oxygen saturation
- Height
- Weight
- BMI
- Pain score

BMI should be calculated automatically.

Store timestamps and author information.

## 10.3 Intake Documentation

Include:

- Chief complaint
- Medication reconciliation
- Allergy review
- History review
- Screening questions
- Relevant observations

Completed intake information should appear in the physician encounter.

---

# 11. Clinical Encounters

This is one of the most important modules.

## 11.1 Encounter Workspace

Build a detailed clinical encounter screen.

Use a three-panel layout where practical.

Left panel:
- Patient summary
- Medical history
- Problems
- Medications
- Allergies
- Recent vitals

Center:
- Encounter documentation
- HPI
- ROS
- Physical examination
- Assessment
- Plan

Right panel:
- Clinical tasks
- Diagnoses
- Orders
- AI assistant
- Encounter checklist

## 11.2 Encounter States

- Scheduled
- In Progress
- Documentation Pending
- Ready for Sign-off
- Signed
- Closed

Signed notes must not be silently editable.

Corrections should use an auditable addendum workflow.

## 11.3 SOAP Documentation

Sections:

Subjective:
- Chief Complaint
- HPI
- Review of Systems

Objective:
- Vitals
- Physical Examination
- Relevant Results

Assessment:
- Clinical Problems
- Working Diagnoses

Plan:
- Medications
- Tests
- Referrals
- Follow-up
- Patient Instructions

Support:

- Save Draft
- Edit Draft
- Autosave when practical
- Templates
- Clinical macros
- Copy-forward with provenance
- Preview Note
- Sign Note
- Add Addendum

## 11.4 Encounter Sign-off

Before signing, validate:

- Required documentation
- Encounter diagnosis
- Order status
- Required acknowledgments

Signing must record:

- Signing clinician
- Timestamp
- Document version
- Relevant audit event

---

# 12. Clinical Problems and Diagnoses

Implement:

- Longitudinal Problem List
- Encounter Diagnoses
- Primary Diagnosis
- Secondary Diagnoses
- Diagnosis Status
- Clinical Notes
- ICD-10-CM Code

Support:

- Add
- Edit
- Resolve
- Reactivate when appropriate
- Link diagnosis to encounter
- Link diagnosis to order

Use a synthetic, curated terminology catalog.

Do not imply the terminology database is complete.

---

# 13. Medication Management

Create medication management functionality.

## 13.1 Medication List

Fields:

- Medication name
- Strength
- Dose
- Route
- Frequency
- Start date
- End date
- Prescribing provider
- Status

## 13.2 Prescription Workflow

Physicians can:

- Search a medication catalog
- Create draft prescriptions
- Select dose
- Select route
- Select frequency
- Specify duration
- Specify quantity
- Select a simulated pharmacy
- Review
- Sign simulated prescriptions

No real pharmacy transmission is permitted.

## 13.3 Medication Reconciliation

Implement:

- Current medication review
- Reconciliation status
- Duplicate medication warnings
- Allergy warning simulation
- Medication history

Use predefined synthetic rules for warnings.

Do not claim that the prototype provides validated clinical decision support.

---

# 14. Orders and Laboratory Results

## 14.1 Orders

Order categories:

- Laboratory
- Imaging
- Referral
- Procedure
- Medication

Each order includes:

- Order ID
- Patient
- Encounter
- Ordering clinician
- Order type
- Priority
- Diagnosis association
- Date
- Status

## 14.2 Order Lifecycle

Draft → Signed → Processing → Completed

Alternative states:

- Cancelled
- Failed

## 14.3 Laboratory Results

Create a simulated lab-processing interface.

Support:

- Pending orders
- Specimen collected
- Processing
- Result entered
- Result published
- Clinician review

Example tests:

- CBC
- CMP
- HbA1c
- Lipid Panel
- TSH
- Urinalysis

Results should contain:

- Test name
- Value
- Unit
- Reference interval
- Abnormal flag
- Result timestamp
- Review status

Do not generate arbitrary diagnostic interpretations as medical facts.

## 14.4 Result Review

Physicians can:

- View results
- Mark reviewed
- Add clinical comments
- Release permitted results to patient portal

Unreleased results must remain hidden from patients.

---

# 15. Insurance Management

## 15.1 Insurance Information

Fields:

- Payer
- Plan
- Member ID
- Group Number
- Subscriber
- Relationship
- Effective Date
- Expiration Date
- Primary/Secondary Coverage

## 15.2 Eligibility Verification

Implement a simulated eligibility checker.

Possible results:

- Active
- Inactive
- Coverage Not Found
- Verification Pending
- Verification Error

Display:

- Verification timestamp
- Coverage status
- Copay estimate
- Deductible
- Out-of-pocket information

All insurance responses must be synthetic.

## 15.3 Insurance Workqueue

Track:

- Expired coverage
- Missing member IDs
- Eligibility failures
- Unverified appointments
- Authorization requirements

---

# 16. Medical Billing and Revenue Cycle Management

Build a substantial billing subsystem.

## 16.1 Charge Capture

Generate billable charge records from completed encounters.

Fields:

- Patient
- Encounter
- Provider
- Diagnosis
- Procedure code
- Units
- Charge amount
- Billing status

## 16.2 Coding Workspace

Support:

- ICD-10-CM diagnosis selection
- CPT/HCPCS procedure selection
- Diagnosis-to-procedure linking
- Missing code warnings
- Duplicate charge detection
- Coding review
- Charge approval

Use a curated demonstration code catalog.

Do not claim complete official code-set licensing or coverage.

## 16.3 Claim Generation

Create simulated claims containing:

- Claim ID
- Patient
- Provider
- Service Date
- Payer
- Diagnosis Codes
- Procedure Codes
- Charges
- Total Amount
- Claim Status

## 16.4 Claim Lifecycle

Draft → Ready for Review → Validated → Submitted → Accepted → Adjudicated → Paid → Closed

Alternative states:

- Validation Failed
- Rejected
- Denied
- Partially Paid

## 16.5 Claim Scrubbing

Implement deterministic validation rules.

Examples:

- Missing diagnosis
- Missing procedure code
- Missing insurance
- Invalid member ID format
- Missing provider
- Duplicate claim
- Incomplete patient demographics
- Missing authorization where required

Show errors and warnings separately.

A claim with blocking validation errors cannot be submitted.

## 16.6 Simulated Payer Responses

Build a local payer simulator.

Possible outcomes:

- Accepted
- Rejected
- Paid
- Partially Paid
- Denied

Use documented, deterministic scenarios so automated tests are reproducible.

Do not connect to real payer networks.

---

# 17. Denial Management

Build a dedicated denial-management workspace.

## 17.1 Denial Dashboard

Display:

- Total denied claims
- Denial rate
- Outstanding denied amount
- Denials by payer
- Denials by reason
- Aging of unresolved denials

## 17.2 Denial Reasons

Simulate:

- Coverage inactive
- Missing authorization
- Coding mismatch
- Duplicate claim
- Filing issue
- Medical necessity documentation missing
- Demographic mismatch

## 17.3 Denial Resolution

Allow billing specialists to:

- Open denial
- Review claim
- Inspect denial reason
- Add notes
- Correct permitted claim fields
- Resubmit simulated claim
- Create appeal draft
- Mark resolved

Maintain historical denial records.

Do not delete the original outcome when the claim is corrected.

---

# 18. Prior Authorization Management

Create an authorization workspace.

Fields:

- Authorization ID
- Patient
- Insurance
- Requested service
- Diagnosis
- Requesting provider
- Submission date
- Expiration date
- Status

Statuses:

- Draft
- Submitted
- Pending Review
- Additional Information Requested
- Approved
- Denied
- Expired

Support:

- Create request
- Submit simulated request
- Review supporting documents
- Track status
- Record simulated payer decision

Authorization status should be linked to relevant orders and billing workflows.

---

# 19. Payments and Patient Billing

Implement:

- Patient balances
- Insurance payments
- Patient payments
- Copay collection
- Payment history
- Statements
- Account balances
- Outstanding invoices

All transactions must be simulated.

Do not store real card numbers.

A payment must update balances consistently.

Prevent payments that violate configured balance rules.

Provide receipt previews.

---

# 20. Patient Portal

Build a separate patient-facing interface.

Patients should be able to:

1. Sign in
2. View upcoming appointments
3. Request appointments
4. Cancel eligible appointments
5. Complete simulated pre-check-in
6. View visit summaries
7. View released laboratory results
8. View medications
9. Request medication renewals
10. Send secure messages
11. View outstanding balances
12. Make simulated payments
13. Update permitted demographic information

## 20.1 Patient Dashboard

Display:

- Upcoming appointment
- Recent visit
- Recent released results
- Active medications
- Unread messages
- Outstanding balance

## 20.2 Secure Messaging

Support:

- Patient-initiated messages
- Staff responses
- Thread history
- Read/unread state
- Message timestamps

Patients must never access another patient's messages.

## 20.3 Appointments

Patient appointment requests must appear in the scheduling workflow.

## 20.4 Results

Only released results should appear in the portal.

---

# 21. AI Clinical Assistant

Build a research-oriented AI assistant integrated into the EHR.

This is a major distinguishing feature.

## 21.1 AI Patient Summary

Generate a structured summary from synthetic patient chart data.

Include:

- Demographics
- Active problems
- Current medications
- Allergies
- Recent encounters
- Recent laboratory results
- Pending orders
- Relevant follow-up needs

The output must be grounded in patient records.

## 21.2 AI Encounter Preparation

For a selected appointment, generate:

- Visit context
- Relevant medical history
- Recent clinical changes
- Outstanding clinical tasks
- Potential documentation gaps

Clearly distinguish source facts from generated suggestions.

## 21.3 AI SOAP Note Drafting

Input:

- Structured encounter data
- Clinician-entered transcript
- Chief complaint
- Relevant patient chart context

Output:

- Draft Subjective
- Draft Objective
- Draft Assessment
- Draft Plan

The physician must review the draft before signing.

Never automatically sign AI-generated notes.

## 21.4 Simulated Ambient Scribe

Implement an ambient-documentation demonstration.

At minimum:

- Accept a synthetic visit transcript
- Generate a structured note draft
- Display editable output
- Allow clinician correction
- Require explicit approval

Optional:

- Browser-based audio capture
- Speech transcription through a configured provider

If a real audio transcription backend is unavailable, the text transcript workflow must remain fully functional.

Do not claim that audio is being transcribed when it is not.

## 21.5 AI Diagnosis and Order Suggestions

Provide optional research demonstrations for:

- Potential encounter diagnoses
- Possible order categories
- Missing documentation
- Follow-up considerations

These must remain unapproved suggestions.

Do not automatically create clinical orders from AI output.

Require explicit clinician action.

## 21.6 AI Billing Assistance

Create an optional AI-assisted coding interface.

Capabilities:

- Suggest relevant coding categories
- Detect missing documentation
- Explain claim validation errors
- Suggest possible denial-resolution steps

Never automatically transmit claims.

## 21.7 AI Architecture

Support two modes:

### Deterministic Demo Mode

No API key required.

Use predefined, reproducible synthetic examples.

All primary demonstration workflows must work offline.

### Optional LLM Mode

If an LLM API key is configured:

- Use a server-side integration
- Keep API keys out of source control
- Validate structured outputs
- Implement timeout handling
- Handle malformed model responses
- Record model and prompt versions
- Avoid sending real patient information
- Keep human approval gates

The core application must never depend on a paid API to function.

---

# 22. Clinical Inbox and Task Management

Create a shared workflow inbox.

Task categories:

- Results to review
- Unsigned notes
- Pending orders
- Medication renewal requests
- Patient messages
- Authorization follow-ups
- Missing documentation
- Billing exceptions

Tasks should include:

- Assigned user
- Patient
- Related record
- Priority
- Status
- Created timestamp
- Due date

Users can:

- View
- Assign
- Reassign
- Complete
- Filter
- Search

Role permissions apply.

---

# 23. Analytics and Reporting

Create a reporting dashboard.

## 23.1 Clinical Metrics

- Patient encounters
- Encounter completion rate
- Unsigned notes
- Pending results
- Common diagnosis categories

## 23.2 Operational Metrics

- Appointment volume
- No-show rate
- Provider utilization
- Check-in completion
- Average appointment status distribution

## 23.3 Financial Metrics

- Total charges
- Claims submitted
- Claim acceptance rate
- Denial rate
- Simulated payments
- Outstanding balances
- A/R aging

## 23.4 Reporting Requirements

Reports should be generated from application data.

Support:

- Date filters
- Provider filters
- Department filters
- Summary cards
- Charts
- Tables
- CSV export

Never display hardcoded metrics as if they reflect current database state.

---

# 24. Interoperability

Implement a simplified interoperability module.

Support:

- FHIR R4-inspired resource representations
- Patient
- Appointment
- Encounter
- Condition
- Observation
- MedicationRequest
- ServiceRequest
- DiagnosticReport
- Coverage

Provide read-only JSON endpoints for selected synthetic records.

Use documented mappings between internal database models and exported resource structures.

Do not claim formal FHIR conformance unless separately validated.

Optional:

- Synthetic data import
- Synthetic data export
- Patient summary export

---

# 25. Database Design

Design a normalized, relational database.

Suggested entities:

Identity and Organization:
- User
- Role
- Practice
- Department
- Provider
- UserDepartmentAssignment

Patient:
- Patient
- PatientIdentifier
- PatientContact
- EmergencyContact
- Consent
- InsurancePolicy

Scheduling:
- Appointment
- AppointmentType
- AppointmentSlot
- ProviderAvailability
- WaitlistEntry
- CheckInRecord

Clinical:
- Encounter
- ClinicalNote
- NoteVersion
- Problem
- Diagnosis
- Allergy
- Medication
- Prescription
- VitalSign
- MedicalHistory
- ProcedureOrder
- LaboratoryOrder
- LaboratoryResult
- ClinicalDocument

Revenue Cycle:
- Charge
- ProcedureCode
- Claim
- ClaimLine
- ClaimValidation
- Denial
- Appeal
- Authorization
- Payment
- PaymentAllocation
- PatientStatement

Communication:
- MessageThread
- Message
- Notification
- Task

AI:
- AIRequest
- AIResponse
- AIDraft
- AIReviewDecision

Security:
- AuditEvent
- DemoResetEvent

Preserve referential integrity.

Use database transactions for multi-record operations.

Do not allow orphaned claims, orders, or encounters.

---

# 26. Cross-Module Consistency

This requirement is critical.

The application must behave like one integrated system.

Examples:

1. Registering a patient updates the patient directory.
2. Booking an appointment updates the schedule.
3. Checking in an appointment updates the nursing worklist.
4. Recording vitals updates the patient chart and encounter.
5. Signing an order creates the corresponding processing task.
6. Publishing a lab result updates the physician results inbox.
7. Releasing a result makes it visible in the patient portal.
8. Signing an encounter makes it eligible for billing.
9. Creating charges makes them visible in the coding workqueue.
10. Submitting a claim updates claim history.
11. Denying a claim creates a denial workqueue entry.
12. Posting payment updates outstanding balances.
13. Sending a patient message updates the staff inbox.
14. Completing a task updates dashboard counts.
15. Every material change produces an appropriate audit event.

All changes should persist across page refreshes and user sessions.

---

# 27. Synthetic Demo Data

Create a realistic synthetic healthcare dataset.

Minimum target:

- 1 fictional practice
- 3 departments
- 8 providers
- 9 role-based demo accounts
- 100 patients
- 150 appointments
- 80 encounters
- 100 clinical notes
- 100 diagnoses
- 150 medication records
- 100 laboratory orders
- 100 laboratory results
- 80 claims
- 20 denials
- 30 payments
- 20 authorizations
- 30 message threads

The precise totals may be adjusted if relational consistency requires it.

Data must be clinically and operationally plausible.

Create scenarios for:

- Routine annual physical
- Chronic diabetes follow-up
- Hypertension follow-up
- Acute respiratory complaint
- Preventive screening
- Medication refill
- Lab review
- Insurance eligibility failure
- Missing authorization
- Claim denial
- Claim correction
- Partial insurance payment
- Patient outstanding balance

Use fictional patients only.

Avoid using real people's identifying information.

---

# 28. Demo Accounts

Generate role-based demo credentials.

Required accounts:

- admin.demo
- manager.demo
- frontdesk.demo
- physician.demo
- nurse.demo
- assistant.demo
- billing.demo
- coder.demo
- patient.demo

Use dedicated public demo credentials that are distinct from any real credentials.

Document the demo account list in README.md.

Ensure every account can log in and perform its permitted workflow.

Provide a demo account selector on the landing page if appropriate.

---

# 29. Demo Reset

Implement a safe synthetic-data reset mechanism.

Requirements:

- Restricted to authorized administrators
- Explicit confirmation
- Clear warning
- No accidental invocation
- Reset only the designated demonstration database
- Never reset a production database
- Recreate consistent synthetic seed data
- Return the application to a known state
- Record a reset event when appropriate

Also support a documented management command for resetting local synthetic demo data.

Do not enable destructive reset operations in production by default.

---

# 30. Automated Testing

Implement comprehensive tests.

## 30.1 Unit Tests

Test:

- Model constraints
- Validation logic
- Status transitions
- Calculations
- Authorization rules
- Claim scrubbing
- Payment allocation
- Clinical document versioning

## 30.2 Integration Tests

Test cross-module workflows:

- Registration → Scheduling
- Scheduling → Check-in
- Check-in → Intake
- Intake → Encounter
- Encounter → Orders
- Orders → Results
- Results → Portal
- Encounter → Billing
- Billing → Claim
- Claim → Denial
- Denial → Correction
- Payment → Balance Update

## 30.3 Browser Tests

Use Playwright for deterministic end-to-end tests.

Test:

- Login
- Navigation
- Forms
- Search
- Filtering
- Scheduling
- Clinical encounters
- Billing workflows
- Patient portal
- Permissions

## 30.4 Computer Use Agent Compatibility

The application must be suitable for later evaluation by a genuine Computer Use Agent.

Use:

- Visible buttons
- Semantic HTML
- Accessible labels
- Stable navigation
- Readable status indicators
- Predictable form interactions
- Clear success messages
- Clear validation errors

Avoid requiring hidden application state or direct database access for user-facing tasks.

Do not substitute Playwright scripts for genuine CUA evaluation when the research explicitly calls for a CUA.

Playwright and CUA are separate testing approaches.

---

# 31. Testability and Observability

For every important workflow:

- Define expected initial state
- Define allowed user actions
- Define expected final state
- Expose final state through the UI
- Persist final state in the database
- Provide reliable reset or fixture setup

Record:

- Relevant audit events
- Application errors
- Failed validation
- State transitions

Avoid exposing sensitive information in logs.

---

# 32. Security Requirements

Implement:

- Server-side authentication
- Role-based authorization
- CSRF protection
- Secure password handling
- Session management
- Patient-level access control
- Audit logging
- Input validation
- ORM-based query handling
- Environment-based secrets

Never commit:

- Real credentials
- API keys
- Real patient data
- Production secrets
- Private tokens

Do not connect to real clinical, pharmacy, payer, or payment systems.

All external transactions must be explicitly simulated.

---

# 33. GitHub Repository

Create a new repository if GitHub access is available.

Preferred repository name:

KateK77/athenaone-clone

Preferred visibility:

Public, provided the repository contains only synthetic data and public demo credentials.

Do not modify or overwrite the existing CareFlow EHR repository.

Maintain clean Git history.

Use meaningful commits.

Create:

- README.md
- docs/architecture.md
- docs/features.md
- docs/workflows.md
- docs/database-schema.md
- docs/testing.md
- docs/limitations.md
- docs/research-evaluation.md

The README must include:

- Project overview
- Original inspiration
- Independence disclaimer
- Technology stack
- Feature overview
- Installation
- Local startup
- Database migrations
- Demo data initialization
- Demo accounts
- Testing instructions
- Screenshots
- Deployment instructions
- Known limitations

---

# 34. Deployment Requirements

Prepare the application for a public portfolio demonstration.

Requirements:

- Render-compatible deployment configuration
- PostgreSQL compatibility
- Environment configuration
- Health-check endpoint
- Static file handling
- Secure production settings
- Database migration instructions
- Demo seed command

The application should continue to function when deployed.

Do not assume local SQLite storage is persistent on ephemeral hosting.

Do not promise permanently free hosting.

Keep hosting costs and operational requirements documented.

---

# 35. Implementation Strategy

Build the application in coherent phases.

Suggested phases:

Phase 0: Architecture, project scaffold, authentication, layout

Phase 1: Patient registration and patient chart

Phase 2: Scheduling and front desk

Phase 3: Nursing intake and clinical encounters

Phase 4: Orders, laboratory results, and medications

Phase 5: Insurance, billing, and claims

Phase 6: Denials, authorizations, and payments

Phase 7: Patient portal and communication

Phase 8: AI clinical assistance

Phase 9: Analytics, interoperability, and administration

Phase 10: Integration hardening and regression testing

Each phase must include:

- Database models
- Migrations
- Backend logic
- Frontend views
- Validation
- Permission enforcement
- Automated tests
- Documentation

Do not sacrifice cross-module integration for superficial feature count.

---

# 36. Completion Requirements

A module is considered complete only when:

1. Its primary pages render.
2. Its core actions work.
3. Data persists.
4. Relevant permissions are enforced.
5. Cross-module state remains consistent.
6. Invalid actions are handled.
7. Automated tests cover its major behavior.
8. The workflow can be performed through the UI.

Do not mark incomplete features as complete.

Do not report test passes unless tests actually executed.

---

# 37. Final Research Deliverables

When implementation is complete, provide:

## A. Feature Inventory

A table containing:

- Module
- Feature
- Implemented / Partial / Missing
- Relevant URL
- Test coverage
- Known limitations

## B. Architecture Report

Describe:

- Backend
- Frontend
- Database
- Authentication
- Authorization
- AI integration
- Inter-module dependencies

## C. Test Report

Provide:

- Number of tests created
- Number executed
- Passed
- Failed
- Skipped
- Pass rate
- Test execution environment

Use:

Pass Rate = Passed / Executed × 100%

Report skipped and blocked tests separately.

## D. GitHub Report

Provide:

- Repository URL
- Branch
- Latest commit
- Push status
- README status

## E. Limitations

Explicitly document:

- Missing features
- Simplified clinical rules
- Simulated insurance behavior
- Synthetic datasets
- AI limitations
- Deployment restrictions
- Differences from the commercial product

---

# 38. Important Research Constraints

This project is intended to support reproducible research on AI-generated software.

Therefore:

- Do not silently change the requirements.
- Record architectural assumptions.
- Document implementation deviations.
- Preserve meaningful development history.
- Do not fabricate test results.
- Do not substitute screenshots for functionality.
- Do not claim nonexistent integrations.
- Do not claim HIPAA compliance, medical-device validation, or clinical suitability.
- Do not use real patient information.
- Make important workflows deterministic and reproducible.
- Keep test fixture generation separate from implementation logic.

Do not create hidden shortcuts specifically designed to inflate evaluation results.

The final system should be evaluated against its actual implemented functionality.

---

# 39. Execution Instructions

You are responsible for implementing this software.

Start by:

1. Inspecting the current workspace.
2. Identifying any existing repository or code.
3. Creating the architecture plan.
4. Defining the database schema.
5. Establishing the design system.
6. Implementing authentication and role management.
7. Building the clinical and operational workflows.
8. Integrating the modules.
9. Creating synthetic data.
10. Running automated tests.
11. Fixing observed failures.
12. Preparing GitHub and deployment documentation.

Proceed autonomously with reasonable technical decisions.

Do not stop after writing a plan.

Implement the actual application.

When requirements are ambiguous, make a reasonable assumption, record it, and continue unless the decision would create substantial security risk or require external authorization.

Do not claim completion until the application has been implemented and verified.

The ultimate objective is a comprehensive, functional, visually professional, and testable reconstruction of the major athenaOne healthcare workflows, suitable for a public software engineering portfolio and subsequent AI agent evaluation research.