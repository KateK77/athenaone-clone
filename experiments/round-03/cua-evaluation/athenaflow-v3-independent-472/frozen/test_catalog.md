# AthenaFlow V3 — 472 frozen CUA tests

All cases are NOT_RUN. Definitions and expected results are not observations.

## Authentication and role boundaries (18)

### AF3-001 — Administrator demo login

Difficulty: Easy. Execution sequence: 11. Description sections: 5, 28, 32.

Preconditions/data: Signed out; documented admin.demo credentials

1. Sign in as admin.demo
2. Open the account menu

Acceptance criteria:

- C1: Administrator identity and role are visible
- C2: Administration is reachable

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-002 — Manager demo login

Difficulty: Easy. Execution sequence: 12. Description sections: 5, 28, 32.

Preconditions/data: Signed out; documented manager.demo credentials

1. Sign in as manager.demo
2. Open operational dashboard

Acceptance criteria:

- C1: Manager identity is correct
- C2: Operational dashboard loads without an authorization error

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-003 — Front desk demo login

Difficulty: Easy. Execution sequence: 13. Description sections: 5, 28, 32.

Preconditions/data: Signed out; documented frontdesk.demo credentials

1. Sign in as frontdesk.demo
2. Open scheduling

Acceptance criteria:

- C1: Front desk identity is correct
- C2: Scheduling workspace is accessible

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-004 — Physician demo login

Difficulty: Easy. Execution sequence: 1. Description sections: 5, 28, 32.

Preconditions/data: Signed out; documented physician.demo credentials

1. Sign in as physician.demo
2. Open assigned patient chart

Acceptance criteria:

- C1: Physician identity is correct
- C2: Assigned chart opens

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-005 — Nurse demo login

Difficulty: Easy. Execution sequence: 14. Description sections: 5, 28, 32.

Preconditions/data: Signed out; documented nurse.demo credentials

1. Sign in as nurse.demo
2. Open nursing worklist

Acceptance criteria:

- C1: Nurse identity is correct
- C2: Nursing worklist opens

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-006 — Medical assistant demo login

Difficulty: Easy. Execution sequence: 15. Description sections: 5, 28, 32.

Preconditions/data: Signed out; documented assistant.demo credentials

1. Sign in as assistant.demo
2. Open intake workflow

Acceptance criteria:

- C1: Medical assistant identity is correct
- C2: Permitted intake workflow opens

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-007 — Billing demo login

Difficulty: Easy. Execution sequence: 16. Description sections: 5, 28, 32.

Preconditions/data: Signed out; documented billing.demo credentials

1. Sign in as billing.demo
2. Open claims

Acceptance criteria:

- C1: Billing identity is correct
- C2: Claim workspace opens

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-008 — Coder demo login

Difficulty: Easy. Execution sequence: 17. Description sections: 5, 28, 32.

Preconditions/data: Signed out; documented coder.demo credentials

1. Sign in as coder.demo
2. Open coding workspace

Acceptance criteria:

- C1: Coder identity is correct
- C2: Coding workspace opens

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-009 — Patient demo login

Difficulty: Easy. Execution sequence: 18. Description sections: 5, 28, 32.

Preconditions/data: Signed out; documented patient.demo credentials

1. Sign in as patient.demo
2. Open portal overview

Acceptance criteria:

- C1: Patient identity is correct
- C2: Only the linked patient's overview is shown

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-010 — Invalid password rejected

Difficulty: Medium. Execution sequence: 19. Description sections: 5, 28, 32.

Preconditions/data: Signed out; valid public demo username

1. Enter the username with deliberately incorrect password once
2. Submit sign-in

Acceptance criteria:

- C1: No authenticated session is created
- C2: Readable error permits correction without disclosing secrets

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-011 — Required login fields

Difficulty: Medium. Execution sequence: 20. Description sections: 5, 28, 32.

Preconditions/data: Signed out

1. Submit empty login form
2. Enter only username and submit

Acceptance criteria:

- C1: Missing required input is identified
- C2: No authenticated session is created

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-012 — Logout invalidates authenticated navigation

Difficulty: Medium. Execution sequence: 21. Description sections: 5, 28, 32.

Preconditions/data: Signed-in physician; chart URL recorded from UI

1. Sign out
2. Use Back then reload the chart URL

Acceptance criteria:

- C1: Authenticated chart data cannot be retrieved after logout
- C2: Sign-in or access-denied page is displayed

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-013 — Unauthenticated direct staff URL

Difficulty: Hard. Execution sequence: 22. Description sections: 5, 28, 32.

Preconditions/data: Signed out; real staff URL recorded from authorized UI

1. Paste the recorded staff URL in browser address bar
2. Navigate

Acceptance criteria:

- C1: Protected content is withheld
- C2: Authentication is requested without a server traceback

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-014 — Front desk cannot sign note

Difficulty: Hard. Execution sequence: 23. Description sections: 5, 28, 32.

Preconditions/data: frontdesk.demo; unsigned encounter; sign URL observed while authorized if exposed

1. Open encounter as front desk
2. Attempt signing through any available action or previously observed URL

Acceptance criteria:

- C1: No physician signature is created
- C2: Missing action alone is insufficient evidence when an observed direct URL is available

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-015 — Nurse cannot sign physician documentation

Difficulty: Hard. Execution sequence: 24. Description sections: 5, 28, 32.

Preconditions/data: nurse.demo; unsigned physician note

1. Open note as nurse
2. Try offered sign action or previously observed signing page
3. Reopen note as physician

Acceptance criteria:

- C1: Note remains unsigned
- C2: Unauthorized signing is denied without changing content

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-016 — Patient cannot open another chart

Difficulty: Hard. Execution sequence: 25. Description sections: 5, 28, 32.

Preconditions/data: Two synthetic patients A and B; B chart URL observed by authorized staff

1. Sign in as patient A
2. Navigate directly to B chart URL

Acceptance criteria:

- C1: No B identity or clinical content is disclosed
- C2: Access is denied or redirected safely

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-017 — Billing role cannot manage staff roles

Difficulty: Hard. Execution sequence: 26. Description sections: 5, 28, 32.

Preconditions/data: billing.demo; account administration URL observed as admin

1. Open recorded administration URL as billing user
2. Attempt any exposed role edit

Acceptance criteria:

- C1: Staff role changes are denied
- C2: Existing roles remain unchanged

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-018 — Cross-role session identity isolation

Difficulty: Hard. Execution sequence: 27. Description sections: 5, 28, 32.

Preconditions/data: Physician signed in; patient credentials available

1. Sign out physician
2. Sign in patient in same browser
3. Revisit previous staff page

Acceptance criteria:

- C1: Patient permissions govern the new session
- C2: Previous physician access is not retained

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

## Global navigation and accessibility (20)

### AF3-019 — Global patient search identity

Difficulty: Easy. Execution sequence: 2. Description sections: 4, 7.1, 31.

Preconditions/data: Two patients with similar names and distinct MRNs

1. Search common name globally
2. Inspect results
3. Select intended MRN

Acceptance criteria:

- C1: Results distinguish name MRN and DOB
- C2: Selected chart matches intended patient

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-020 — Role-aware navigation destinations

Difficulty: Medium. Execution sequence: 28. Description sections: 4, 7.1, 31.

Preconditions/data: Physician account; permitted modules listed in source

1. Visit dashboard schedule patients encounters inbox orders results medications and AI links

Acceptance criteria:

- C1: Each permitted link opens its named workspace
- C2: No dead navigation or misleading destination is encountered

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-021 — Department context changes coherently

Difficulty: Medium. Execution sequence: 29. Description sections: 4, 7.1, 31.

Preconditions/data: Staff account with two authorized departments

1. Select department A
2. Open schedule
3. Select B
4. Inspect active context

Acceptance criteria:

- C1: Selected department is visible
- C2: Department-dependent views reflect the selected context without mislabeling records

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-022 — Account dropdown at desktop width

Difficulty: Medium. Execution sequence: 30. Description sections: 4, 7.1, 31.

Preconditions/data: Staff logged in; 1440x900 viewport

1. Open account menu
2. Reach Sign out using keyboard

Acceptance criteria:

- C1: Menu stays in viewport
- C2: Sign out is fully visible and keyboard reachable

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-023 — Staff account dropdown on narrow viewport

Difficulty: Medium. Execution sequence: 31. Description sections: 4, 7.1, 31.

Preconditions/data: Staff logged in; 390x844 viewport

1. Open account menu
2. Tab to Sign out
3. Activate it

Acceptance criteria:

- C1: Menu and sign-out control remain visible
- C2: Logout completes

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-024 — Portal account dropdown without global search

Difficulty: Medium. Execution sequence: 32. Description sections: 4, 7.1, 31.

Preconditions/data: Patient logged in; 390x844 viewport

1. Open account menu
2. Reach and activate Sign out

Acceptance criteria:

- C1: Menu is within viewport despite absent global search
- C2: Logout works

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-025 — Tablet navigation and content reflow

Difficulty: Medium. Execution sequence: 33. Description sections: 4, 7.1, 31.

Preconditions/data: Physician chart open; 768x1024 viewport

1. Open navigation
2. Switch to encounter
3. Inspect patient summary

Acceptance criteria:

- C1: Navigation is usable
- C2: Identifiers allergies and vitals remain visible without overlapping panels

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-026 — Mobile chart essential information

Difficulty: Medium. Execution sequence: 34. Description sections: 4, 7.1, 31.

Preconditions/data: Populated chart; 390x844 viewport

1. Open chart summary
2. Scroll through vitals and allergies

Acceptance criteria:

- C1: Name MRN DOB allergies and recorded vitals remain readable
- C2: Clinical cards reflow instead of hiding essential information

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-027 — Keyboard form operation

Difficulty: Medium. Execution sequence: 35. Description sections: 4, 7.1, 31.

Preconditions/data: Registration form with known valid input

1. Use Tab and Shift+Tab through fields
2. Select dropdown option with keyboard
3. Submit valid form

Acceptance criteria:

- C1: Focus is visibly tracked
- C2: Essential form actions can be completed without pointer-only controls

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-028 — Checkbox label toggles control

Difficulty: Medium. Execution sequence: 36. Description sections: 4, 7.1, 31.

Preconditions/data: Diagnosis primary checkbox and authorization-required checkbox available

1. Click label once
2. Inspect state
3. Click label again

Acceptance criteria:

- C1: Label and control operate together
- C2: Checked and unchecked states are visually distinct

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-029 — Explicit clinical action names

Difficulty: Easy. Execution sequence: 37. Description sections: 4, 7.1, 31.

Preconditions/data: Patient chart with permitted create actions

1. Inspect insurance diagnosis order and message entry points

Acceptance criteria:

- C1: Actions use clear contextual names equivalent to Add insurance Add diagnosis Add order and New message
- C2: Insurance coverage is identified explicitly

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-030 — Readable typography at default zoom

Difficulty: Medium. Execution sequence: 38. Description sections: 4, 7.1, 31.

Preconditions/data: Desktop and mobile viewports; browser zoom 100 percent

1. Inspect sign-in staff form and portal
2. Capture screenshots

Acceptance criteria:

- C1: Text controls and secondary labels are readable without clipping
- C2: Exact CSS pixel-size conformance is not claimed from screenshots alone

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-031 — Recognizable buttons and focus

Difficulty: Medium. Execution sequence: 39. Description sections: 4, 7.1, 31.

Preconditions/data: Staff form with primary and secondary actions

1. Inspect controls without hovering
2. Tab through actions

Acceptance criteria:

- C1: Primary action is visually distinct
- C2: Secondary actions have readable borders and text
- C3: Focused control is apparent

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-032 — Form spacing and amount width

Difficulty: Medium. Execution sequence: 40. Description sections: 4, 7.1, 31.

Preconditions/data: Payment form; 390x844 viewport

1. Inspect last field submit action and amount entry
2. Type 1234.56 without submitting

Acceptance criteria:

- C1: Final field and action have usable separation
- C2: Amount remains readable within available width

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-033 — Responsive long tables

Difficulty: Medium. Execution sequence: 41. Description sections: 4, 7.1, 31.

Preconditions/data: Patient directory and claims table; 390x844 viewport

1. Inspect table
2. Use provided scroll or stacked layout
3. Open a row action

Acceptance criteria:

- C1: Essential cells and actions are reachable
- C2: Whole page does not require horizontal hunting caused by overflowing layout

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-034 — Readable empty state

Difficulty: Easy. Execution sequence: 42. Description sections: 4, 7.1, 31.

Preconditions/data: A documented filter yielding zero appointments

1. Apply empty-result filter
2. Inspect workspace

Acceptance criteria:

- C1: Explicit empty-state explanation appears
- C2: No stale rows remain and recovery controls are available

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-035 — Recoverable field validation

Difficulty: Medium. Execution sequence: 43. Description sections: 4, 7.1, 31.

Preconditions/data: Registration form with one missing required field

1. Enter other valid values
2. Submit
3. Correct missing field

Acceptance criteria:

- C1: Readable field error appears
- C2: Other submitted values persist
- C3: Correction can be saved

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-036 — Destructive-action cancellation

Difficulty: Medium. Execution sequence: 44. Description sections: 4, 7.1, 31.

Preconditions/data: Existing cancellable appointment

1. Open cancellation confirmation
2. Choose keep or dismiss
3. Reload appointment

Acceptance criteria:

- C1: No cancellation occurs
- C2: Appointment retains original status and details

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-037 — Loading interaction does not duplicate submission

Difficulty: Medium. Execution sequence: 45. Description sections: 4, 7.1, 31.

Preconditions/data: Synthetic message compose form

1. Enter subject/body
2. Activate submit twice quickly using visible control
3. Open thread list

Acceptance criteria:

- C1: Only one intended thread is created
- C2: UI gives progress or disables duplicate action, or equivalent safe behavior

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-038 — Patient selection summary wraps

Difficulty: Medium. Execution sequence: 46. Description sections: 4, 7.1, 31.

Preconditions/data: Form patient selector; long synthetic patient name; 390x844

1. Select patient
2. Inspect selection summary after closing dropdown

Acceptance criteria:

- C1: Full name MRN and DOB remain visible in a wrapping summary
- C2: Native dropdown truncation does not hide identity

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

## Registration and patient selection (24)

### AF3-039 — Register complete patient

Difficulty: Medium. Execution sequence: 3. Description sections: 7, 26.

Preconditions/data: Unique per-case synthetic MRN; valid demographic fixture

1. Search MRN to exclude duplicate
2. Complete registration with all required fields
3. Save
4. Reload directory

Acceptance criteria:

- C1: Exactly one new patient exists
- C2: MRN name DOB and contact match entered values

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-040 — Minimal required registration

Difficulty: Medium. Execution sequence: 47. Description sections: 7, 26.

Preconditions/data: Unused synthetic identity; optional fields blank

1. Complete only UI-required registration fields
2. Save
3. Open chart

Acceptance criteria:

- C1: Required-only record saves
- C2: Optional omissions do not produce fabricated values

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-041 — Required identity validation

Difficulty: Medium. Execution sequence: 48. Description sections: 7, 26.

Preconditions/data: New registration; all required identity fields empty

1. Fill contact only
2. Submit

Acceptance criteria:

- C1: Required identity fields are identified
- C2: No incomplete patient is created

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-042 — Duplicate MRN rejected

Difficulty: Hard. Execution sequence: 49. Description sections: 7, 26.

Preconditions/data: Existing patient A MRN

1. Register another name with A's MRN
2. Submit
3. Search MRN

Acceptance criteria:

- C1: Duplicate is rejected
- C2: Original patient is unchanged and no second record appears

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-043 — Duplicate demographic warning

Difficulty: Medium. Execution sequence: 50. Description sections: 7, 26.

Preconditions/data: Existing patient with known name and DOB

1. Start new registration with same name and DOB and unused MRN
2. Submit or review duplicate check

Acceptance criteria:

- C1: Potential duplicate is clearly surfaced
- C2: User is not silently redirected to or merged with the existing patient

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-044 — Search before registering

Difficulty: Medium. Execution sequence: 51. Description sections: 7, 26.

Preconditions/data: Existing patient A

1. Search A by MRN from registration entry workflow
2. Open matching result

Acceptance criteria:

- C1: Existing identity is easy to find before creation
- C2: No new record is created by searching

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-045 — Edit contact information

Difficulty: Medium. Execution sequence: 52. Description sections: 7, 26.

Preconditions/data: Patient A with recorded phone/address

1. Change phone and address to fixture values
2. Save
3. Reload chart

Acceptance criteria:

- C1: New contact information persists
- C2: MRN and clinical history remain unchanged

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-046 — Optional preferred name and language

Difficulty: Medium. Execution sequence: 53. Description sections: 7, 26.

Preconditions/data: Patient A

1. Set preferred name and preferred language
2. Save
3. Reopen demographics

Acceptance criteria:

- C1: Both fields retain chosen values
- C2: Legal name is preserved separately

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-047 — Emergency contact persistence

Difficulty: Medium. Execution sequence: 54. Description sections: 7, 26.

Preconditions/data: Patient A; synthetic emergency contact

1. Add name relationship and phone
2. Save
3. Reload demographics

Acceptance criteria:

- C1: Emergency contact matches saved values
- C2: Patient's own phone is not overwritten

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-048 — Consent state persistence

Difficulty: Medium. Execution sequence: 55. Description sections: 7, 26.

Preconditions/data: Patient with editable consent state

1. Set recorded consent status
2. Save
3. Reload
4. Change to another offered state and save

Acceptance criteria:

- C1: Each explicit state persists
- C2: Consent is distinguishable from an unchecked form that was never saved

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-049 — Invalid demographic formatting

Difficulty: Medium. Execution sequence: 56. Description sections: 7, 26.

Preconditions/data: New registration; email value not-an-email and nonnumeric DOB input where possible

1. Enter malformed values
2. Submit using browser form

Acceptance criteria:

- C1: Invalid input is rejected with readable guidance
- C2: No corrupted patient record is created

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-050 — Directory search by exact MRN

Difficulty: Easy. Execution sequence: 57. Description sections: 7, 26.

Preconditions/data: Existing unique MRN

1. Search exact MRN
2. Open result

Acceptance criteria:

- C1: Result identifies the expected patient
- C2: No similarly named patient's chart is opened

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-051 — Directory search by name

Difficulty: Easy. Execution sequence: 58. Description sections: 7, 26.

Preconditions/data: Two known patients sharing last name

1. Search shared last name

Acceptance criteria:

- C1: Both matching records are discoverable
- C2: MRN and DOB distinguish them

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-052 — DOB directory filter

Difficulty: Medium. Execution sequence: 59. Description sections: 7, 26.

Preconditions/data: Known patients on different birth dates

1. Apply DOB filter for A
2. Inspect results
3. Clear filter

Acceptance criteria:

- C1: Returned rows match requested birth date
- C2: Clearing restores broader results

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-053 — Provider and department directory filters

Difficulty: Medium. Execution sequence: 60. Description sections: 7, 26.

Preconditions/data: Patients assigned to distinct providers/departments

1. Filter by provider A and department A
2. Inspect rows
3. Change provider

Acceptance criteria:

- C1: Displayed scope follows selected filters
- C2: Filter labels match rendered data

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-054 — Patient status filter

Difficulty: Medium. Execution sequence: 61. Description sections: 7, 26.

Preconditions/data: Known active and inactive patients

1. Filter Active
2. Filter Inactive
3. Clear filter

Acceptance criteria:

- C1: Each view reflects chosen patient status
- C2: Inactive records are not mislabeled as active

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-055 — Directory sorting and pagination

Difficulty: Medium. Execution sequence: 62. Description sections: 7, 26.

Preconditions/data: More patients than one page; known names at page boundary

1. Sort by offered name column
2. Move to next page
3. Return

Acceptance criteria:

- C1: Ordering follows chosen direction
- C2: Rows are not duplicated or lost at the tested boundary

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-056 — Patient selector typed name filter

Difficulty: Medium. Execution sequence: 63. Description sections: 7, 26.

Preconditions/data: Scheduling form; similar-name patients

1. Type full name into patient selector
2. Select by MRN and DOB

Acceptance criteria:

- C1: Search narrows candidates
- C2: Selected identity is unambiguous

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-057 — Patient selector typed MRN filter

Difficulty: Medium. Execution sequence: 64. Description sections: 7, 26.

Preconditions/data: Insurance form; patient A

1. Type A's MRN
2. Select result
3. Save valid policy

Acceptance criteria:

- C1: Correct patient is selected
- C2: Policy attaches to A

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-058 — Search does not replace selection

Difficulty: Medium. Execution sequence: 65. Description sections: 7, 26.

Preconditions/data: Clinical form with patient A preselected

1. Search for B without selecting B
2. Inspect summary
3. Save valid A-associated record

Acceptance criteria:

- C1: Selection remains A until explicitly changed
- C2: Saved record belongs to A

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-059 — Keyboard patient selection and empty result

Difficulty: Medium. Execution sequence: 66. Description sections: 7, 26.

Preconditions/data: Scheduling patient selector

1. Type impossible search value
2. Inspect empty state
3. Search A
4. Select using arrows and Enter

Acceptance criteria:

- C1: Empty result is explicit
- C2: Keyboard selection resolves A with correct identifiers

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-060 — Patient selection survives validation

Difficulty: Hard. Execution sequence: 67. Description sections: 7, 26.

Preconditions/data: Insurance form with patient A selected and missing member ID

1. Submit invalid form
2. Inspect selection
3. Correct member ID
4. Save

Acceptance criteria:

- C1: A stays selected through error
- C2: Entered valid values persist
- C3: Saved coverage belongs to A

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-061 — Diagnosis and encounter selectors prevent wrong-patient context

Difficulty: Hard. Execution sequence: 68. Description sections: 7, 26.

Preconditions/data: Patients A/B with distinct encounters and diagnoses

1. Select A in order form
2. Inspect related selectors
3. Select an available A encounter and diagnosis

Acceptance criteria:

- C1: Related choices show sufficient context
- C2: B-only records cannot be linked to A through exposed UI

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-062 — Scoped patient selector for restricted role

Difficulty: Hard. Execution sequence: 69. Description sections: 7, 26.

Preconditions/data: Assigned physician with documented patient scope; out-of-scope B fixture

1. Search B's exact MRN in clinical selector
2. Attempt known B form URL if available

Acceptance criteria:

- C1: Search and direct form obey the same documented patient scope
- C2: No out-of-scope record can be created or accessed

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

## Longitudinal patient chart (14)

### AF3-063 — Summary reconciles patient identity

Difficulty: Easy. Execution sequence: 70. Description sections: 7.3, 26.

Preconditions/data: Patient A with demographic and clinical fixture

1. Open chart Summary
2. Compare name MRN DOB sex and provider to demographics

Acceptance criteria:

- C1: Identity matches patient record
- C2: No cross-patient summary data appears

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-064 — Encounter history opens correct visit

Difficulty: Medium. Execution sequence: 71. Description sections: 7.3, 26.

Preconditions/data: Patient with two encounters on different dates

1. Open Encounters tab
2. Select older visit
3. Return and select newer visit

Acceptance criteria:

- C1: Dates statuses and providers distinguish visits
- C2: Each link opens the selected encounter

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-065 — Medical and surgical histories persist

Difficulty: Medium. Execution sequence: 72. Description sections: 7.3, 26.

Preconditions/data: Patient A; permitted history editing

1. Add synthetic medical and surgical history entries
2. Save
3. Reload tabs

Acceptance criteria:

- C1: Entries persist in their correct history categories
- C2: Patient linkage remains A

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-066 — Family and social histories remain distinct

Difficulty: Medium. Execution sequence: 73. Description sections: 7.3, 26.

Preconditions/data: Patient A; editable history

1. Add family-history marker and separate social-history marker
2. Save
3. Reload

Acceptance criteria:

- C1: Both markers persist in correct sections
- C2: One category does not overwrite the other

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-067 — Add allergy and review chart banner

Difficulty: Medium. Execution sequence: 74. Description sections: 7.3, 26.

Preconditions/data: Patient A; synthetic penicillin allergy with reaction rash

1. Add allergy
2. Save
3. Open encounter summary

Acceptance criteria:

- C1: Allergy substance and reaction persist
- C2: Encounter allergy display reflects the change

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-068 — Allergy edit history and current state

Difficulty: Medium. Execution sequence: 75. Description sections: 7.3, 26.

Preconditions/data: Patient with allergy entry

1. Edit reaction severity using offered controls
2. Save
3. Reopen allergy list

Acceptance criteria:

- C1: Current allergy details reflect edit
- C2: Unrelated allergies are unchanged

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-069 — Chart medication status display

Difficulty: Medium. Execution sequence: 76. Description sections: 7.3, 26.

Preconditions/data: Patient with one active and one discontinued medication

1. Open Medications tab
2. Inspect current and history views

Acceptance criteria:

- C1: Active versus discontinued status is distinguishable
- C2: Discontinued medication is not shown as actively taken without qualification

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-070 — Vitals chronology and units

Difficulty: Medium. Execution sequence: 77. Description sections: 7.3, 26.

Preconditions/data: Patient with two timestamped vitals sets using different recorded units

1. Open Vitals tab
2. Open encounter entries

Acceptance criteria:

- C1: Chronology author and units distinguish measurements
- C2: Latest values do not overwrite historical measurements

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-071 — Orders and results cross-links

Difficulty: Medium. Execution sequence: 78. Description sections: 7.3, 26.

Preconditions/data: Patient with order and published result

1. Open Orders tab
2. Follow related result
3. Return through chart

Acceptance criteria:

- C1: Order result and patient references agree
- C2: Links do not open another patient's result

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-072 — Clinical document association

Difficulty: Medium. Execution sequence: 79. Description sections: 7.3, 26.

Preconditions/data: Patient A; supported document upload or creation; synthetic text document

1. Attach or create document through UI
2. Save
3. Reopen Documents tab

Acceptance criteria:

- C1: Document title and patient association persist
- C2: Document is retrievable through the UI

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-073 — Immunization record display

Difficulty: Medium. Execution sequence: 80. Description sections: 7.3, 26.

Preconditions/data: Patient with seeded immunization entry

1. Open Immunizations tab
2. Inspect details
3. Reload

Acceptance criteria:

- C1: Immunization name date and available details persist
- C2: No unsupported administration is implied by merely viewing

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-074 — Chart appointment history

Difficulty: Medium. Execution sequence: 81. Description sections: 7.3, 26.

Preconditions/data: Patient with past and future appointments

1. Open Appointments tab
2. Open each appointment

Acceptance criteria:

- C1: History includes correct date provider and status
- C2: Navigation stays scoped to the patient

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-075 — Chart billing summary links

Difficulty: Medium. Execution sequence: 82. Description sections: 7.3, 26.

Preconditions/data: Patient with one known claim and balance

1. Open Billing tab
2. Open related claim as permitted staff

Acceptance criteria:

- C1: Balance matches claim detail
- C2: Claim identity and patient linkage agree

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-076 — Chart consistency after new diagnosis

Difficulty: Hard. Execution sequence: 83. Description sections: 7.3, 26.

Preconditions/data: Patient A with open encounter

1. Add diagnosis in encounter
2. Open longitudinal chart and encounter again

Acceptance criteria:

- C1: Diagnosis appears in its intended encounter or problem scope
- C2: No unintended duplicate or different-patient diagnosis is created

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

## Scheduling and waitlist (26)

### AF3-077 — Create appointment with default duration

Difficulty: Medium. Execution sequence: 84. Description sections: 8.

Preconditions/data: Patient A; future free provider slot; configured appointment type

1. Select patient provider date time and visit type
2. Inspect default duration
3. Save
4. Reload schedule

Acceptance criteria:

- C1: Appointment uses configured duration
- C2: Card shows correct patient time type reason duration and status

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-078 — Daily date change auto-updates

Difficulty: Medium. Execution sequence: 4. Description sections: 8.

Preconditions/data: Appointments on dates D and D+1; JavaScript enabled

1. Change schedule date to D+1 without pressing Apply

Acceptance criteria:

- C1: Heading identifies D+1
- C2: Rendered appointments change to D+1 without a second action

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-079 — Provider filter auto-updates

Difficulty: Medium. Execution sequence: 85. Description sections: 8.

Preconditions/data: Appointments for providers A and B; JavaScript enabled

1. Change provider filter to A without pressing Apply

Acceptance criteria:

- C1: Only selected provider's applicable appointments remain
- C2: Visible active filter matches results

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-080 — Department filter auto-updates

Difficulty: Medium. Execution sequence: 86. Description sections: 8.

Preconditions/data: Appointments in two departments; JavaScript enabled

1. Change department filter without pressing Apply

Acceptance criteria:

- C1: Schedule changes to selected department
- C2: Displayed heading and context remain coherent

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-081 — Date navigation retains filters

Difficulty: Medium. Execution sequence: 87. Description sections: 8.

Preconditions/data: Provider A and department A filters active

1. Move one day forward
2. Move back

Acceptance criteria:

- C1: Provider and department filters stay selected
- C2: Rendered rows follow date and retained filters

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-082 — Week heading and chronological ordering

Difficulty: Medium. Execution sequence: 88. Description sections: 8.

Preconditions/data: Appointments spanning a known week

1. Switch to week view
2. Inspect dates and times
3. Navigate next week

Acceptance criteria:

- C1: Heading matches actual rendered week
- C2: Appointments are chronological within displayed days

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-083 — Appointment-bearing provider groups prominent

Difficulty: Easy. Execution sequence: 89. Description sections: 8.

Preconditions/data: Providers with and without appointments on selected day

1. Open day schedule
2. Inspect group organization

Acceptance criteria:

- C1: Populated groups are readily visible
- C2: Empty groups are compact and labeled no appointments rather than available

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-084 — Narrow schedule avoids empty horizontal canvas

Difficulty: Medium. Execution sequence: 90. Description sections: 8.

Preconditions/data: Mixed populated and empty provider groups; 390x844

1. Open schedule
2. Locate populated provider appointments
3. Open one card

Acceptance criteria:

- C1: Appointment details and actions are reachable
- C2: Mostly empty wide canvas does not obscure populated groups

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-085 — Calendar card opens correct details

Difficulty: Medium. Execution sequence: 91. Description sections: 8.

Preconditions/data: Two adjacent appointments for same provider

1. Open second card
2. Compare details with card

Acceptance criteria:

- C1: Patient time duration reason and status match selected appointment
- C2: First appointment is not opened accidentally

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-086 — Provider overlap prevented

Difficulty: Hard. Execution sequence: 92. Description sections: 8.

Preconditions/data: Existing provider A appointment 10:00-10:30 on D

1. Attempt second A appointment 10:15-10:45 on D
2. Submit

Acceptance criteria:

- C1: Overlap is rejected unless an explicit pre-recorded scheduling rule permits it
- C2: Existing appointment remains unchanged

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-087 — Back-to-back booking boundary

Difficulty: Medium. Execution sequence: 93. Description sections: 8.

Preconditions/data: Provider A available 10:00-11:00; booking 10:00-10:30

1. Book 10:30-11:00 on same day

Acceptance criteria:

- C1: Adjacent non-overlapping slot is accepted under recorded availability rules
- C2: No false overlap is reported

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-088 — Different-provider simultaneous booking

Difficulty: Medium. Execution sequence: 94. Description sections: 8.

Preconditions/data: Two available providers; distinct patients; same time

1. Book provider A at time T
2. Book provider B at T

Acceptance criteria:

- C1: Both independent appointments can exist
- C2: Provider conflict is not incorrectly applied across providers

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-089 — Unavailable provider slot rejected

Difficulty: Hard. Execution sequence: 95. Description sections: 8.

Preconditions/data: Documented provider unavailability interval

1. Attempt appointment wholly within unavailable interval

Acceptance criteria:

- C1: UI prevents or rejects booking with explanation
- C2: No appointment is persisted in prohibited slot

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-090 — Reschedule retains appointment identity/history

Difficulty: Medium. Execution sequence: 96. Description sections: 8.

Preconditions/data: Existing future appointment

1. Move to valid different date/time
2. Save
3. Open history and both schedule dates

Acceptance criteria:

- C1: Appointment appears in new slot and not as active in old slot
- C2: Reschedule is traceable without duplicate active booking

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-091 — Cancel appointment

Difficulty: Medium. Execution sequence: 97. Description sections: 8.

Preconditions/data: Existing cancellable appointment

1. Cancel with synthetic reason
2. Confirm
3. Reload schedule and history

Acceptance criteria:

- C1: Cancelled status persists
- C2: Appointment history retains cancellation and original identity

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-092 — Confirm scheduled appointment

Difficulty: Medium. Execution sequence: 98. Description sections: 8.

Preconditions/data: Scheduled appointment

1. Choose Confirm
2. Reload details

Acceptance criteria:

- C1: Status becomes Confirmed
- C2: History records transition

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-093 — Mark arrived appointment

Difficulty: Medium. Execution sequence: 99. Description sections: 8.

Preconditions/data: Confirmed appointment

1. Choose Mark arrived
2. Reload front desk list

Acceptance criteria:

- C1: Status becomes Arrived
- C2: Arrival is visible to front desk workflow

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-094 — Mark no-show appointment

Difficulty: Medium. Execution sequence: 100. Description sections: 8.

Preconditions/data: Eligible past scheduled appointment under documented rules

1. Choose No Show
2. Confirm if requested
3. Reload

Acceptance criteria:

- C1: No Show state persists
- C2: History identifies transition

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-095 — Invalid lifecycle transition rejected

Difficulty: Hard. Execution sequence: 101. Description sections: 8.

Preconditions/data: Cancelled appointment; previously observed status action URL where applicable

1. Open details
2. Attempt offered Roomed or Complete action, or observed action page

Acceptance criteria:

- C1: Invalid transition is unavailable or denied
- C2: Cancelled appointment does not become active without documented restoration

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-096 — Check-out completion boundary

Difficulty: Hard. Execution sequence: 102. Description sections: 8.

Preconditions/data: Completed appointment with required checkout details

1. Complete allowed check-out action
2. Reload history

Acceptance criteria:

- C1: Appointment becomes Checked Out
- C2: Earlier clinical completion history remains intact

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-097 — Appointment type duration configuration reflected

Difficulty: Medium. Execution sequence: 103. Description sections: 8.

Preconditions/data: Admin can configure demo visit type; manager/front desk booking

1. Set test type duration to 25 minutes as admin
2. Book that type as front desk

Acceptance criteria:

- C1: New appointment defaults to 25 minutes
- C2: Unrelated appointment types retain previous defaults

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-098 — Waitlist enrollment preferences

Difficulty: Medium. Execution sequence: 104. Description sections: 8.

Preconditions/data: Patient A awaiting appointment

1. Add waitlist entry with provider A and date range D1-D2
2. Save
3. Reload

Acceptance criteria:

- C1: Patient provider and date range persist
- C2: Entry appears in waitlist

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-099 — Waitlist matching respects preferences

Difficulty: Hard. Execution sequence: 105. Description sections: 8.

Preconditions/data: Waitlist entry for provider A D1-D2; one matching and one outside slot

1. Open available-slot matches

Acceptance criteria:

- C1: Matching slot is offered
- C2: Outside date/provider slot is not mislabeled as a matching preference

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-100 — Waitlist simulated notification

Difficulty: Medium. Execution sequence: 106. Description sections: 8.

Preconditions/data: Matching waitlist entry and open slot

1. Trigger simulated notification
2. Open entry history

Acceptance criteria:

- C1: Notification is clearly simulated
- C2: Status or history records notification without implying real delivery

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-101 — Waitlist booking resolves entry

Difficulty: Hard. Execution sequence: 107. Description sections: 8.

Preconditions/data: Notified entry with free matching slot

1. Book through waitlist
2. Open schedule and waitlist

Acceptance criteria:

- C1: Exactly one appointment appears
- C2: Waitlist entry no longer presents the same request as unbooked

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-102 — Schedule Apply fallback present and usable

Difficulty: Medium. Execution sequence: 108. Description sections: 8.

Preconditions/data: Schedule date/filter controls

1. Inspect explicit Apply control
2. Change date and activate Apply
3. Inspect heading and results

Acceptance criteria:

- C1: Explicit fallback can submit selected filters
- C2: Rendered period and filters agree; JavaScript-disabled behavior is a separately disclosed unverified condition unless browser can disable JS without scripts

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

## Front desk check-in (12)

### AF3-103 — Check-in identity step

Difficulty: Medium. Execution sequence: 109. Description sections: 9, 11.2, 26.

Preconditions/data: Arrived appointment for A

1. Start check-in
2. Inspect patient identity
3. Confirm identity step

Acceptance criteria:

- C1: Name MRN and DOB identify A
- C2: Identity confirmation is reflected in step progress

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-104 — Check-in demographics step

Difficulty: Medium. Execution sequence: 110. Description sections: 9, 11.2, 26.

Preconditions/data: Patient with editable phone and arrived appointment

1. Update phone during check-in
2. Save step
3. Open demographics

Acceptance criteria:

- C1: Corrected phone persists
- C2: Demographic step completion is visible

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-105 — Check-in coverage review

Difficulty: Medium. Execution sequence: 111. Description sections: 9, 11.2, 26.

Preconditions/data: Patient with policy and arrived appointment

1. Review insurance in check-in
2. Run simulated verification
3. Save step

Acceptance criteria:

- C1: Coverage status is visible
- C2: Verification belongs to selected patient and policy

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-106 — Consent blocks incomplete check-in

Difficulty: Medium. Execution sequence: 112. Description sections: 9, 11.2, 26.

Preconditions/data: Required consent missing; remaining required steps complete

1. Attempt final check-in without consent

Acceptance criteria:

- C1: Check-in is not finalized
- C2: Missing mandatory consent is identified

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-107 — Intake forms completion indicator

Difficulty: Medium. Execution sequence: 113. Description sections: 9, 11.2, 26.

Preconditions/data: Check-in requires supported intake form

1. Complete intake form
2. Save
3. Reopen check-in

Acceptance criteria:

- C1: Submitted answers persist
- C2: Step indicator reflects completion

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-108 — Simulated copay during check-in

Difficulty: Medium. Execution sequence: 114. Description sections: 9, 11.2, 26.

Preconditions/data: Eligible appointment; no prior copay; amount 25.00

1. Record simulated copay 25.00
2. View receipt/history

Acceptance criteria:

- C1: One 25.00 copay is recorded
- C2: Amount and simulated nature are explicit

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-109 — Copay revisit does not double charge

Difficulty: Hard. Execution sequence: 115. Description sections: 9, 11.2, 26.

Preconditions/data: Appointment with 25.00 copay already recorded

1. Return to check-in
2. Reload confirmation
3. Inspect payment history

Acceptance criteria:

- C1: Original copay remains singular
- C2: Balance and history do not add another 25.00

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-110 — Check-in resumes saved progress

Difficulty: Medium. Execution sequence: 116. Description sections: 9, 11.2, 26.

Preconditions/data: Partially completed workflow

1. Save demographics step
2. Leave page
3. Reopen check-in

Acceptance criteria:

- C1: Completed step remains complete
- C2: Unfinished mandatory steps remain identifiable

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-111 — Complete check-in creates worklist entry

Difficulty: Hard. Execution sequence: 117. Description sections: 9, 11.2, 26.

Preconditions/data: All mandatory steps satisfied; arrived appointment

1. Finalize check-in
2. Sign in as nurse
3. Open worklist

Acceptance criteria:

- C1: Appointment is Checked In
- C2: Patient appears once in nursing worklist

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-112 — Initial encounter does not start physician care

Difficulty: Hard. Execution sequence: 118. Description sections: 9, 11.2, 26.

Preconditions/data: Appointment before physician start; completed front desk check-in

1. Open newly created encounter
2. Compare appointment and encounter states

Acceptance criteria:

- C1: Encounter starts Scheduled
- C2: Checked In appointment is not falsely labeled physician In Progress

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-113 — Missing registration requirements block completion

Difficulty: Hard. Execution sequence: 119. Description sections: 9, 11.2, 26.

Preconditions/data: Patient missing one explicitly required registration item

1. Attempt final check-in
2. Correct item through UI
3. Retry

Acceptance criteria:

- C1: Initial completion is rejected with specific missing item
- C2: Completion succeeds after correction

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-114 — Check-in history is readable

Difficulty: Medium. Execution sequence: 120. Description sections: 9, 11.2, 26.

Preconditions/data: Completed check-in with 25.00 copay

1. Open activity history

Acceptance criteria:

- C1: Check-in event includes actor timestamp and formatted $25.00
- C2: Raw dictionaries arrays and object syntax are not displayed

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

## Vitals units and clinical intake (26)

### AF3-115 — New intake defaults to imperial units

Difficulty: Easy. Execution sequence: 5. Description sections: 10.

Preconditions/data: Fresh intake form with no prior measurements

1. Open intake
2. Inspect height and weight selectors

Acceptance criteria:

- C1: Height defaults to in
- C2: Weight defaults to lb

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-116 — Independent unit selection

Difficulty: Medium. Execution sequence: 121. Description sections: 10.

Preconditions/data: New intake; height 170 cm and weight 150 lb

1. Set height cm and weight lb independently
2. Save
3. Reload

Acceptance criteria:

- C1: Each unit selection persists independently
- C2: Saved values retain represented measurements

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-117 — Imperial to metric conversion

Difficulty: Medium. Execution sequence: 122. Description sections: 10.

Preconditions/data: Unsaved height 65 in and weight 150 lb

1. Switch height to cm and weight to kg

Acceptance criteria:

- C1: Height displays 165.1 cm
- C2: Weight displays 68.04 kg with no more than two decimals

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-118 — Metric to imperial conversion

Difficulty: Medium. Execution sequence: 123. Description sections: 10.

Preconditions/data: Unsaved height 170 cm and weight 70 kg

1. Switch to in and lb

Acceptance criteria:

- C1: Height displays 66.93 in
- C2: Weight displays 154.32 lb with no more than two decimals

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-119 — Repeated unit toggle before saving

Difficulty: Hard. Execution sequence: 124. Description sections: 10.

Preconditions/data: Enter 65.37 in and 147.29 lb

1. Toggle both units five round trips without editing
2. Return to original units

Acceptance criteria:

- C1: Original displayed values 65.37 in and 147.29 lb are restored
- C2: Rounding does not accumulate across toggles

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-120 — Precision survives save and reload

Difficulty: Hard. Execution sequence: 125. Description sections: 10.

Preconditions/data: Enter height 65.37 in and weight 147.29 lb

1. Save
2. Reload
3. Switch to metric
4. Switch back
5. Save and reload

Acceptance criteria:

- C1: Original imperial values remain 65.37 and 147.29
- C2: Metric display is 166.04 cm and 66.81 kg; internal eight-decimal storage is not claimed directly verified

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-121 — Changing converted value overrides original measurement

Difficulty: Hard. Execution sequence: 126. Description sections: 10.

Preconditions/data: Enter height 65 in~Switch to cm showing 165.1 cm

1. Edit height to 170 cm
2. Save
3. Reload
4. Switch to in

Acceptance criteria:

- C1: Saved height is 170 cm and converts to 66.93 in
- C2: Old canonical value does not restore 65 in

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-122 — Changed converted weight persists

Difficulty: Hard. Execution sequence: 127. Description sections: 10.

Preconditions/data: Enter 150 lb and convert to kg

1. Replace displayed weight with 70 kg
2. Save
3. Reload
4. Switch to lb

Acceptance criteria:

- C1: Saved weight is 70 kg and converts to 154.32 lb
- C2: Original 150 lb does not override the edit

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-123 — BMI automatic calculation

Difficulty: Medium. Execution sequence: 128. Description sections: 10.

Preconditions/data: Height 170 cm and weight 70 kg

1. Enter both measurements
2. Save
3. Inspect BMI

Acceptance criteria:

- C1: BMI displays 24.2
- C2: BMI is labeled and shown to one decimal place

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-124 — BMI invariant under unit switches

Difficulty: Hard. Execution sequence: 129. Description sections: 10.

Preconditions/data: Height 170 cm weight 70 kg with BMI 24.2

1. Toggle height only
2. Toggle weight only
3. Save and reload

Acceptance criteria:

- C1: BMI remains 24.2
- C2: Independent unit changes do not change represented BMI

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-125 — Trailing zeros suppressed

Difficulty: Medium. Execution sequence: 130. Description sections: 10.

Preconditions/data: Enter 65.00 in and 150.00 lb

1. Save
2. Open saved vitals

Acceptance criteria:

- C1: Height and weight display without unnecessary decimal zeros
- C2: Units remain explicit

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-126 — At most two displayed decimals

Difficulty: Medium. Execution sequence: 131. Description sections: 10.

Preconditions/data: Editable input permits 65.375 in and 147.295 lb or equivalent fixture

1. Enter values
2. Save or follow displayed precision validation
3. Reload accepted measurement

Acceptance criteria:

- C1: UI consistently limits displayed height/weight to at most two decimals
- C2: Any input rejection is explicit and preserves values; exact internal rounding mode is not inferred

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-127 — Validation preserves selected units

Difficulty: Hard. Execution sequence: 132. Description sections: 10.

Preconditions/data: Height 170 cm and weight 154.32 lb; one invalid required vital field

1. Submit
2. Inspect error form
3. Correct invalid field
4. Save

Acceptance criteria:

- C1: cm/lb selections and valid measurements survive error
- C2: Saved values represent submitted measurements

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-128 — Unit conversion after validation error

Difficulty: Hard. Execution sequence: 133. Description sections: 10.

Preconditions/data: Enter 65.37 in 147.29 lb; induce required-field error

1. Submit
2. Toggle units on returned form
3. Correct error
4. Save
5. Reload

Acceptance criteria:

- C1: Conversion remains consistent with original entered measurements
- C2: Stale error-page metadata does not silently replace values

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-129 — Zero or negative height rejected

Difficulty: Medium. Execution sequence: 134. Description sections: 10.

Preconditions/data: Fresh intake with otherwise valid values

1. Enter 0 height
2. Submit
3. Enter negative height where browser permits
4. Submit

Acceptance criteria:

- C1: Nonpositive height cannot be saved
- C2: Readable validation identifies height

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-130 — Zero or negative weight rejected

Difficulty: Medium. Execution sequence: 135. Description sections: 10.

Preconditions/data: Fresh intake with otherwise valid values

1. Enter 0 weight
2. Submit
3. Enter negative weight where browser permits
4. Submit

Acceptance criteria:

- C1: Nonpositive weight cannot be saved
- C2: No impossible BMI is stored visibly

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-131 — Pain range boundary accepted

Difficulty: Medium. Execution sequence: 136. Description sections: 10.

Preconditions/data: Intake with otherwise valid vitals

1. Save pain 0
2. Reopen editable intake
3. Save pain 10

Acceptance criteria:

- C1: Both endpoints are accepted
- C2: Saved pain remains within labeled 0-10 scale

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-132 — Pain outside range rejected

Difficulty: Medium. Execution sequence: 137. Description sections: 10.

Preconditions/data: Fresh intake

1. Enter pain 11
2. Submit
3. Try -1 where possible

Acceptance criteria:

- C1: Out-of-range values cannot be saved
- C2: Pain validation is understandable

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-133 — All vital fields show units

Difficulty: Easy. Execution sequence: 138. Description sections: 10.

Preconditions/data: Fresh intake form

1. Inspect BP heart rate respiratory rate temperature oxygen and pain labels

Acceptance criteria:

- C1: Labels show mmHg bpm breaths/min degrees Celsius percent and 0-10 respectively
- C2: Units are not ambiguous

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-134 — Complete vitals set persists

Difficulty: Medium. Execution sequence: 139. Description sections: 10.

Preconditions/data: BP 120/80 HR 72 RR 16 temp 36.8 SpO2 98 height 65 in weight 150 lb pain 2

1. Enter complete set
2. Save
3. Reload encounter and chart

Acceptance criteria:

- C1: All nine measurements and BMI are visible with correct units
- C2: No field disappears from saved views

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-135 — Vital author and timestamp

Difficulty: Medium. Execution sequence: 140. Description sections: 10.

Preconditions/data: Nurse entering a new complete vitals set

1. Save vitals
2. Open chronological history

Acceptance criteria:

- C1: Author identifies acting nurse
- C2: Timestamp corresponds to saved entry and distinguishes earlier measurements

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-136 — Existing metric record keeps meaning

Difficulty: Hard. Execution sequence: 141. Description sections: 10.

Preconditions/data: Existing height 170 cm weight 70 kg fixture

1. Open historical vitals
2. View/edit without changing measurements
3. Save if applicable

Acceptance criteria:

- C1: Original measurements retain metric meaning
- C2: Defaults do not reinterpret 170 as inches or 70 as pounds

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-137 — Chief complaint and intake note transfer

Difficulty: Medium. Execution sequence: 142. Description sections: 10.

Preconditions/data: Nurse on A encounter; unique complaint and observation text

1. Enter chief complaint and intake note
2. Save
3. Open as physician

Acceptance criteria:

- C1: Physician encounter contains entered complaint and observations
- C2: Intake note purpose is explained in form

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-138 — Reconciliation and review indicators

Difficulty: Medium. Execution sequence: 143. Description sections: 10.

Preconditions/data: Patient with known medication allergy and history entries

1. Complete medication reconciliation allergy review and history review
2. Save
3. Reload

Acceptance criteria:

- C1: Each completed review is distinguishable
- C2: Review state persists without changing unrelated clinical records

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-139 — Screening questions and observations

Difficulty: Medium. Execution sequence: 144. Description sections: 10.

Preconditions/data: Intake with supported screening items

1. Record permitted answers and observation marker
2. Save
3. Reopen intake

Acceptance criteria:

- C1: Answers and observation persist
- C2: Physician can find the recorded intake information

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-140 — Assistant rooming cannot start physician care

Difficulty: Hard. Execution sequence: 145. Description sections: 10.

Preconditions/data: assistant.demo; checked-in appointment

1. Record intake
2. Choose Roomed
3. Attempt physician Start if exposed
4. Open as physician

Acceptance criteria:

- C1: Roomed state persists
- C2: Physician care remains unstarted until assigned physician or admin starts it

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

## Encounters notes and signatures (24)

### AF3-141 — Encounter workspace patient context

Difficulty: Easy. Execution sequence: 146. Description sections: 11, 26.

Preconditions/data: Assigned patient with history problems medications allergies and recent vitals

1. Open encounter workspace
2. Inspect clinical panels

Acceptance criteria:

- C1: Relevant patient context and documentation areas are accessible
- C2: Patient identity remains clear

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-142 — Appointment and documentation states separately labeled

Difficulty: Medium. Execution sequence: 147. Description sections: 11, 26.

Preconditions/data: Roomed appointment and Scheduled encounter

1. Open encounter
2. Inspect both status labels

Acceptance criteria:

- C1: Appointment progress and documentation status are distinct
- C2: Roomed does not imply a signed or started encounter

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-143 — Assigned physician starts care

Difficulty: Medium. Execution sequence: 148. Description sections: 11, 26.

Preconditions/data: Roomed appointment; assigned physician signed in

1. Choose Start physician care
2. Reload appointment and encounter

Acceptance criteria:

- C1: Appointment care progresses to In Progress
- C2: Encounter moves to In Progress with actor/history

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-144 — Unassigned physician cannot start care

Difficulty: Hard. Execution sequence: 149. Description sections: 11, 26.

Preconditions/data: Second physician not assigned to encounter under documented scope

1. Open encounter or observed start page as unassigned physician
2. Attempt Start if offered

Acceptance criteria:

- C1: Start is denied
- C2: Assigned physician and original states remain unchanged

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-145 — Administrator can start permitted care

Difficulty: Hard. Execution sequence: 150. Description sections: 11, 26.

Preconditions/data: Roomed appointment; admin account

1. Open appointment
2. Start physician care through offered authorized action

Acceptance criteria:

- C1: Start succeeds for administrator
- C2: History identifies administrator rather than falsely attributing physician action

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-146 — Save complete SOAP draft

Difficulty: Medium. Execution sequence: 6. Description sections: 11, 26.

Preconditions/data: In-progress encounter; distinct text for all SOAP subsections

1. Enter complaint HPI ROS exam assessment and plan
2. Save Draft
3. Reload

Acceptance criteria:

- C1: All submitted sections persist
- C2: Note remains unsigned

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-147 — Edit existing unsigned draft

Difficulty: Medium. Execution sequence: 151. Description sections: 11, 26.

Preconditions/data: Draft note with markers in Subjective and Plan

1. Change Plan only
2. Save
3. Reload

Acceptance criteria:

- C1: Plan changes persist
- C2: Unedited Subjective remains intact
- C3: No signature appears

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-148 — Preview note matches draft

Difficulty: Medium. Execution sequence: 152. Description sections: 11, 26.

Preconditions/data: Draft with known SOAP text and recorded vitals

1. Open Preview
2. Compare sections and values

Acceptance criteria:

- C1: Preview reflects current saved draft and patient context
- C2: Preview does not sign note

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-149 — Clinical template insertion

Difficulty: Medium. Execution sequence: 153. Description sections: 11, 26.

Preconditions/data: In-progress encounter; available template

1. Select template
2. Apply
3. Edit one section
4. Save

Acceptance criteria:

- C1: Template populates editable content
- C2: Saved edit is retained
- C3: Template does not introduce another patient's facts

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-150 — Clinical macro expansion

Difficulty: Medium. Execution sequence: 154. Description sections: 11, 26.

Preconditions/data: Unsigned note; documented available macro

1. Insert macro using visible workflow
2. Review expanded text
3. Save

Acceptance criteria:

- C1: Macro produces intended readable text
- C2: Draft remains editable and unsigned

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-151 — Copy-forward provenance

Difficulty: Hard. Execution sequence: 155. Description sections: 11, 26.

Preconditions/data: Patient with prior note and new unsigned encounter

1. Copy forward prior content using UI
2. Inspect source/provenance
3. Save

Acceptance criteria:

- C1: Copied content identifies its source
- C2: New note is not presented as newly observed facts without provenance

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-152 — Documentation Pending state

Difficulty: Medium. Execution sequence: 156. Description sections: 11, 26.

Preconditions/data: In-progress encounter with incomplete draft

1. Use permitted workflow to mark documentation pending
2. Reload

Acceptance criteria:

- C1: Documentation Pending state persists
- C2: Appointment progress remains separately labeled

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-153 — Ready for Sign-off state

Difficulty: Medium. Execution sequence: 157. Description sections: 11, 26.

Preconditions/data: Draft satisfying documented preparation requirements

1. Move to Ready for Sign-off
2. Open unsigned-note workqueue

Acceptance criteria:

- C1: Encounter is ready but unsigned
- C2: Workqueue reflects need for clinician signature

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-154 — Required documentation blocks signing

Difficulty: Hard. Execution sequence: 158. Description sections: 11, 26.

Preconditions/data: Draft missing an explicitly required section

1. Attempt Sign
2. Inspect error and status

Acceptance criteria:

- C1: Signature is not created
- C2: Missing documentation is identified

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-155 — Missing encounter diagnosis blocks signing

Difficulty: Hard. Execution sequence: 159. Description sections: 11, 26.

Preconditions/data: Otherwise signable note without encounter diagnosis

1. Attempt Sign

Acceptance criteria:

- C1: Signature is not created
- C2: Missing diagnosis is explained

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-156 — Order-state gate on sign-off

Difficulty: Hard. Execution sequence: 160. Description sections: 11, 26.

Preconditions/data: Encounter with an order state documented to block sign-off

1. Attempt Sign
2. Resolve blocking order through UI
3. Retry

Acceptance criteria:

- C1: Initial sign-off is blocked with order reason
- C2: After resolution allowed sign-off can proceed

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-157 — Acknowledgment gate on sign-off

Difficulty: Hard. Execution sequence: 161. Description sections: 11, 26.

Preconditions/data: Signable encounter with required acknowledgment unchecked

1. Attempt Sign
2. Complete acknowledgment
3. Retry

Acceptance criteria:

- C1: Unchecked requirement blocks signing
- C2: Acknowledged valid note can be signed

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-158 — Sign note records signature details

Difficulty: Medium. Execution sequence: 162. Description sections: 11, 26.

Preconditions/data: Complete note all gates satisfied

1. Explicitly Sign
2. Open signed note details

Acceptance criteria:

- C1: Signing clinician timestamp and version are visible
- C2: Signed state persists

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-159 — Signed note immutable on revisit

Difficulty: Hard. Execution sequence: 163. Description sections: 11, 26.

Preconditions/data: Signed note; previous edit page URL recorded before signing

1. Open signed note
2. Revisit edit page via browser
3. Attempt any exposed edit

Acceptance criteria:

- C1: Original signed content cannot be silently changed
- C2: Editing is denied or routed to auditable addendum

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-160 — Auditable addendum preserves original

Difficulty: Hard. Execution sequence: 164. Description sections: 11, 26.

Preconditions/data: Signed note; correction text marker

1. Create addendum
2. Save/sign as required
3. Open original and addendum

Acceptance criteria:

- C1: Original signed text is retained
- C2: Addendum author time and association are visible

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-161 — Close signed encounter

Difficulty: Medium. Execution sequence: 165. Description sections: 11, 26.

Preconditions/data: Signed encounter meeting closure prerequisites

1. Close encounter
2. Reload chart history

Acceptance criteria:

- C1: Encounter becomes Closed
- C2: Signed note and signature metadata remain intact

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-162 — Closed encounter cannot become fresh draft silently

Difficulty: Hard. Execution sequence: 166. Description sections: 11, 26.

Preconditions/data: Closed signed encounter; prior draft-edit URL known

1. Navigate to prior edit URL
2. Attempt editable action if present

Acceptance criteria:

- C1: Closed signed content is preserved
- C2: No unsigned overwrite is created

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-163 — Draft version provenance after successive saves

Difficulty: Hard. Execution sequence: 167. Description sections: 11, 26.

Preconditions/data: Unsigned note with first version text

1. Save first version
2. Change text and save again
3. Open available version/history view

Acceptance criteria:

- C1: Saved revisions are traceable through versions or audit history
- C2: Current draft matches latest save without misattributing author

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-164 — Starting care preserves an authored draft

Difficulty: Hard. Execution sequence: 168. Description sections: 11, 26.

Preconditions/data: Scheduled encounter linked to unstarted appointment but containing authored draft fixture

1. Start physician care as assigned physician
2. Reload note

Acceptance criteria:

- C1: Authored draft content remains unchanged
- C2: Lifecycle transition does not reset documentation

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

## Problems and diagnoses (12)

### AF3-165 — Add longitudinal problem

Difficulty: Medium. Execution sequence: 169. Description sections: 12, 4.2.

Preconditions/data: Patient A; curated diabetes entry

1. Open problem list
2. Add curated diabetes diagnosis and note
3. Save
4. Reload

Acceptance criteria:

- C1: Problem name code status and note persist
- C2: Problem belongs to A

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-166 — Edit problem details

Difficulty: Medium. Execution sequence: 170. Description sections: 12, 4.2.

Preconditions/data: Existing active problem

1. Edit permitted clinical note/status detail
2. Save
3. Reload

Acceptance criteria:

- C1: Edited field persists
- C2: Problem identity and unrelated entries remain unchanged

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-167 — Resolve active problem

Difficulty: Medium. Execution sequence: 171. Description sections: 12, 4.2.

Preconditions/data: Existing active problem

1. Choose Resolve
2. Save
3. Reopen active and history views

Acceptance criteria:

- C1: Resolved status persists
- C2: Historical problem remains accessible

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-168 — Reactivate resolved problem

Difficulty: Medium. Execution sequence: 172. Description sections: 12, 4.2.

Preconditions/data: Resolved problem eligible for reactivation

1. Choose Reactivate
2. Save
3. Reload

Acceptance criteria:

- C1: Problem is active again
- C2: Existing history is retained without creating an unintended duplicate

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-169 — Encounter diagnosis association

Difficulty: Medium. Execution sequence: 173. Description sections: 12, 4.2.

Preconditions/data: Two encounters for patient A

1. Add curated diagnosis to newer encounter
2. Open both encounters

Acceptance criteria:

- C1: Diagnosis is linked to intended encounter
- C2: Older encounter does not gain unintended association

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-170 — Primary diagnosis true persists

Difficulty: Medium. Execution sequence: 174. Description sections: 12, 4.2.

Preconditions/data: Encounter diagnosis with primary unchecked

1. Read primary explanation
2. Check Primary
3. Save
4. Reload

Acceptance criteria:

- C1: Primary designation persists
- C2: Explanatory text clarifies meaning

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-171 — Primary diagnosis false persists

Difficulty: Medium. Execution sequence: 175. Description sections: 12, 4.2.

Preconditions/data: Editable diagnosis currently primary; valid alternative primary if required

1. Uncheck Primary
2. Save
3. Reload

Acceptance criteria:

- C1: Explicit false state persists
- C2: Prior checked state does not silently return

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-172 — Primary checkbox survives error

Difficulty: Hard. Execution sequence: 176. Description sections: 12, 4.2.

Preconditions/data: New diagnosis with Primary checked but required code missing

1. Submit
2. Inspect checkbox
3. Choose code
4. Save

Acceptance criteria:

- C1: Checked state survives validation error
- C2: Saved diagnosis matches chosen designation

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-173 — Secondary diagnoses retained

Difficulty: Medium. Execution sequence: 177. Description sections: 12, 4.2.

Preconditions/data: Encounter with primary diagnosis and two secondary diagnoses

1. Add secondary diagnoses
2. Save
3. Reopen

Acceptance criteria:

- C1: All intended diagnoses persist
- C2: Primary and secondary designations remain distinguishable

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-174 — Curated code selection matches label

Difficulty: Medium. Execution sequence: 178. Description sections: 12, 4.2.

Preconditions/data: Curated ICD-10-CM catalog entry visible

1. Search catalog
2. Select code
3. Save diagnosis
4. Inspect saved label/code

Acceptance criteria:

- C1: Saved label and code match selection
- C2: Catalog is not advertised as complete official terminology

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-175 — Diagnosis-to-order linkage

Difficulty: Hard. Execution sequence: 179. Description sections: 12, 4.2.

Preconditions/data: A encounter with two diagnoses; new lab order

1. Select second diagnosis on order
2. Save
3. Open order

Acceptance criteria:

- C1: Order references selected diagnosis and correct encounter
- C2: First diagnosis is not silently substituted

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-176 — Diagnosis cannot cross patient boundaries

Difficulty: Hard. Execution sequence: 180. Description sections: 12, 4.2.

Preconditions/data: A order form; B diagnosis known from authorized chart

1. Inspect diagnosis options with A selected
2. Try an observed B-linked form URL where applicable

Acceptance criteria:

- C1: B-only diagnosis cannot be attached to A through UI
- C2: Existing A and B diagnoses remain intact

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

## Medication management (16)

### AF3-177 — Medication details and status

Difficulty: Easy. Execution sequence: 181. Description sections: 13.

Preconditions/data: Patient with complete active medication entry

1. Open medication detail

Acceptance criteria:

- C1: Name strength dose route frequency dates provider and status are visible
- C2: Patient association is correct

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-178 — Medication catalog search

Difficulty: Medium. Execution sequence: 182. Description sections: 13.

Preconditions/data: Curated catalog with known item

1. Search medication name
2. Choose strength
3. Inspect selected item

Acceptance criteria:

- C1: Chosen name and strength match catalog result
- C2: Selection is not silently replaced

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-179 — Create prescription draft

Difficulty: Medium. Execution sequence: 183. Description sections: 13.

Preconditions/data: Patient A; curated medication; simulated pharmacy

1. Fill dose route frequency duration quantity and pharmacy
2. Save draft
3. Reload

Acceptance criteria:

- C1: All prescription fields persist
- C2: Prescription remains unsigned and simulated

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-180 — Edit prescription draft

Difficulty: Medium. Execution sequence: 184. Description sections: 13.

Preconditions/data: Unsigned prescription with quantity 30

1. Change quantity to 60
2. Save
3. Reload

Acceptance criteria:

- C1: Quantity becomes 60
- C2: Unchanged medication and route remain intact

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-181 — Prescription review before signing

Difficulty: Medium. Execution sequence: 185. Description sections: 13.

Preconditions/data: Complete unsigned prescription

1. Open review
2. Compare dose route frequency quantity and pharmacy

Acceptance criteria:

- C1: Review matches saved prescription
- C2: Review itself does not sign or transmit

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-182 — Sign simulated prescription

Difficulty: Medium. Execution sequence: 186. Description sections: 13.

Preconditions/data: Physician; valid reviewed draft

1. Explicitly sign
2. Open medication/history view

Acceptance criteria:

- C1: Signed simulated prescription is recorded
- C2: No real pharmacy transmission is represented

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-183 — Missing prescription fields block save/sign

Difficulty: Hard. Execution sequence: 187. Description sections: 13.

Preconditions/data: Draft missing required dose or pharmacy as declared by form

1. Attempt save/sign
2. Inspect error

Acceptance criteria:

- C1: Incomplete prescription is rejected
- C2: Required missing fields are identified

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-184 — Prescription quantity invalid input

Difficulty: Medium. Execution sequence: 188. Description sections: 13.

Preconditions/data: Otherwise valid prescription; quantity zero or negative

1. Enter invalid quantity
2. Submit

Acceptance criteria:

- C1: Nonpositive quantity cannot become a valid signed prescription
- C2: Error is readable

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-185 — Nurse cannot sign prescription

Difficulty: Hard. Execution sequence: 189. Description sections: 13.

Preconditions/data: nurse.demo; physician prescription draft and observed sign page

1. Open prescription as nurse
2. Try exposed signing action or page

Acceptance criteria:

- C1: No physician prescription signature is created
- C2: Action is denied or unavailable with direct URL denial where observable

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-186 — Duplicate medication warning

Difficulty: Medium. Execution sequence: 190. Description sections: 13.

Preconditions/data: Patient already taking medication M

1. Create draft for same curated medication M
2. Review

Acceptance criteria:

- C1: Synthetic duplicate warning is displayed
- C2: Warning identifies relevant existing medication

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-187 — Synthetic allergy warning

Difficulty: Medium. Execution sequence: 191. Description sections: 13.

Preconditions/data: Patient with seeded allergy triggering documented rule

1. Choose medication matching trigger
2. Review prescription

Acceptance criteria:

- C1: Allergy warning identifies synthetic conflict
- C2: Prototype does not claim validated decision support

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-188 — Non-trigger medication does not show wrong allergy

Difficulty: Medium. Execution sequence: 192. Description sections: 13.

Preconditions/data: Same patient; documented non-trigger medication

1. Choose non-trigger medication
2. Review

Acceptance criteria:

- C1: No allergy conflict falsely references another drug or patient
- C2: Existing allergy remains visible for review

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-189 — Medication reconciliation completion

Difficulty: Medium. Execution sequence: 193. Description sections: 13.

Preconditions/data: Nurse; patient with medication list

1. Review list
2. Record reconciliation complete
3. Reload encounter

Acceptance criteria:

- C1: Reconciliation status persists
- C2: Review does not sign a prescription

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-190 — Medication history after discontinuation

Difficulty: Medium. Execution sequence: 194. Description sections: 13.

Preconditions/data: Medication eligible for permitted status edit

1. Mark discontinued through supported UI
2. Save
3. Open active list and history

Acceptance criteria:

- C1: Discontinued state is visible
- C2: Historical entry remains and is not shown as active without qualification

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-191 — Medication start and end dates

Difficulty: Medium. Execution sequence: 195. Description sections: 13.

Preconditions/data: Draft with valid start/end dates

1. Save dates
2. Reload medication detail

Acceptance criteria:

- C1: Dates persist accurately
- C2: Start/end labels do not swap

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-192 — Prescription patient context preserved

Difficulty: Hard. Execution sequence: 196. Description sections: 13.

Preconditions/data: Two patients with similar names; A draft prescription

1. Navigate away and back to A prescription
2. Sign as authorized physician
3. Open B medication list

Acceptance criteria:

- C1: Prescription stays associated with A
- C2: B does not gain A's medication

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

## Medical orders (16)

### AF3-193 — Create laboratory order

Difficulty: Medium. Execution sequence: 197. Description sections: 14.1, 14.2, 26.

Preconditions/data: A encounter with diagnosis; curated CBC test

1. Add laboratory order selecting CBC and diagnosis
2. Save draft
3. Reload

Acceptance criteria:

- C1: Order identifies patient encounter clinician category diagnosis priority and date
- C2: Status is Draft

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-194 — Create imaging order

Difficulty: Medium. Execution sequence: 198. Description sections: 14.1, 14.2, 26.

Preconditions/data: A encounter; supported imaging catalog entry

1. Add imaging order
2. Save
3. Open detail

Acceptance criteria:

- C1: Imaging category and requested service persist
- C2: Patient and encounter links are correct

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-195 — Create referral order

Difficulty: Medium. Execution sequence: 199. Description sections: 14.1, 14.2, 26.

Preconditions/data: A encounter; supported referral destination

1. Add referral with reason
2. Save
3. Reload

Acceptance criteria:

- C1: Referral destination and reason persist
- C2: Order remains associated with A

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-196 — Create procedure order

Difficulty: Medium. Execution sequence: 200. Description sections: 14.1, 14.2, 26.

Preconditions/data: A encounter; supported procedure entry

1. Add procedure order with diagnosis
2. Save
3. Reload

Acceptance criteria:

- C1: Procedure and diagnosis association persist
- C2: No other encounter gains order

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-197 — Create medication category order

Difficulty: Medium. Execution sequence: 201. Description sections: 14.1, 14.2, 26.

Preconditions/data: A encounter; medication order workflow available

1. Create medication-category order through designated UI
2. Open detail

Acceptance criteria:

- C1: Order category is Medication
- C2: Clinical context is preserved and transaction is simulated

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-198 — Order priority and detail persistence

Difficulty: Medium. Execution sequence: 202. Description sections: 14.1, 14.2, 26.

Preconditions/data: Draft lab order with normal priority

1. Change to supported urgent priority
2. Save
3. Reload

Acceptance criteria:

- C1: Priority persists
- C2: Other order details stay unchanged

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-199 — Sign draft order

Difficulty: Medium. Execution sequence: 203. Description sections: 14.1, 14.2, 26.

Preconditions/data: Complete draft order

1. Review
2. Sign
3. Reload

Acceptance criteria:

- C1: Status becomes Signed
- C2: Signing action is recorded

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-200 — Signing creates processing task

Difficulty: Hard. Execution sequence: 204. Description sections: 14.1, 14.2, 26.

Preconditions/data: Unsigned lab order with no processing task

1. Sign order
2. Open processing task queue

Acceptance criteria:

- C1: One task is associated with signed order
- C2: No task for another patient is substituted

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-201 — Processing transition

Difficulty: Medium. Execution sequence: 205. Description sections: 14.1, 14.2, 26.

Preconditions/data: Signed order

1. Move to Processing through authorized workflow
2. Reload

Acceptance criteria:

- C1: Status becomes Processing
- C2: History retains signing event

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-202 — Complete processing order

Difficulty: Medium. Execution sequence: 206. Description sections: 14.1, 14.2, 26.

Preconditions/data: Processing order with required completion information

1. Complete order
2. Reload chart Orders tab

Acceptance criteria:

- C1: Completed status persists
- C2: Order appears consistently in chart and processing view

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-203 — Cancel eligible order

Difficulty: Medium. Execution sequence: 207. Description sections: 14.1, 14.2, 26.

Preconditions/data: Draft or signed order whose documented rule permits cancellation

1. Cancel with reason
2. Confirm
3. Reload

Acceptance criteria:

- C1: Cancelled status and reason persist
- C2: Cancelled order is not treated as active processing

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-204 — Record failed processing

Difficulty: Medium. Execution sequence: 208. Description sections: 14.1, 14.2, 26.

Preconditions/data: Order with supported deterministic failed-processing scenario

1. Execute documented simulated failure through UI
2. Open order history

Acceptance criteria:

- C1: Failed status and reason are visible
- C2: Failure is not misreported as Completed

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-205 — Prevent invalid order transition

Difficulty: Hard. Execution sequence: 209. Description sections: 14.1, 14.2, 26.

Preconditions/data: Draft order with incomplete prerequisites

1. Try completing directly through exposed action or previously observed completion page

Acceptance criteria:

- C1: Invalid Draft-to-Completed transition is denied
- C2: Draft is not silently completed

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-206 — Missing diagnosis blocks required order workflow

Difficulty: Hard. Execution sequence: 210. Description sections: 14.1, 14.2, 26.

Preconditions/data: Order type requires diagnosis; no diagnosis selected

1. Attempt save/sign
2. Inspect feedback

Acceptance criteria:

- C1: Missing association is identified
- C2: Order cannot progress past documented blocking gate

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-207 — Order cancelled does not complete from stale page

Difficulty: Hard. Execution sequence: 211. Description sections: 14.1, 14.2, 26.

Preconditions/data: Cancellable order opened in two browser tabs

1. Cancel in tab one
2. Return to tab two and attempt old action
3. Reload

Acceptance criteria:

- C1: Stale action cannot complete cancelled order
- C2: Current state remains consistent

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-208 — Order filtering by patient/status

Difficulty: Medium. Execution sequence: 212. Description sections: 14.1, 14.2, 26.

Preconditions/data: Known Draft Signed and Completed orders across patients

1. Filter patient A and Signed
2. Open displayed order

Acceptance criteria:

- C1: Results satisfy both filters
- C2: Order count/details do not include unrelated patient B

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

## Laboratory processing and result release (16)

### AF3-209 — Pending lab workqueue

Difficulty: Medium. Execution sequence: 213. Description sections: 14.3, 14.4, 20.4.

Preconditions/data: Signed CBC order awaiting specimen

1. Open lab-processing queue
2. Locate order by patient and order ID

Acceptance criteria:

- C1: Correct pending order is present
- C2: It is not labeled completed

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-210 — Specimen collection recorded

Difficulty: Medium. Execution sequence: 214. Description sections: 14.3, 14.4, 20.4.

Preconditions/data: Pending lab order

1. Record specimen collected
2. Reload lab timeline

Acceptance criteria:

- C1: Collection step is recorded for correct order
- C2: Time and current processing state are distinguishable

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-211 — Processing state reflected

Difficulty: Medium. Execution sequence: 215. Description sections: 14.3, 14.4, 20.4.

Preconditions/data: Specimen-collected order

1. Start lab processing
2. Open order detail

Acceptance criteria:

- C1: Processing state appears in both lab and order views
- C2: Patient linkage agrees

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-212 — Enter numeric lab result

Difficulty: Medium. Execution sequence: 216. Description sections: 14.3, 14.4, 20.4.

Preconditions/data: Processing HbA1c order; synthetic value 7.2 percent; interval from fixture

1. Enter value unit and reference interval
2. Save draft result
3. Reload

Acceptance criteria:

- C1: Value 7.2 unit and interval persist
- C2: Draft is not prematurely released

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-213 — Abnormal flag preserved

Difficulty: Medium. Execution sequence: 217. Description sections: 14.3, 14.4, 20.4.

Preconditions/data: Synthetic lab result marked abnormal by documented fixture rule

1. Save flagged result
2. Open result detail

Acceptance criteria:

- C1: Abnormal flag is explicit and tied to reference interval/value
- C2: No unsupported diagnosis is asserted

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-214 — Publish entered result

Difficulty: Medium. Execution sequence: 218. Description sections: 14.3, 14.4, 20.4.

Preconditions/data: Complete unpublished result

1. Publish through processing UI
2. Open physician result inbox

Acceptance criteria:

- C1: Published result appears for review
- C2: Timestamp and pending review state are visible

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-215 — Physician reviews result

Difficulty: Medium. Execution sequence: 219. Description sections: 14.3, 14.4, 20.4.

Preconditions/data: Published unreviewed result

1. Open as physician
2. Mark reviewed
3. Reload

Acceptance criteria:

- C1: Review state persists
- C2: Reviewer and time are traceable where provided

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-216 — Clinical comment on result

Difficulty: Medium. Execution sequence: 220. Description sections: 14.3, 14.4, 20.4.

Preconditions/data: Published result; authorized physician

1. Add comment marker
2. Save
3. Reopen

Acceptance criteria:

- C1: Comment persists on correct result
- C2: Original numeric value is not overwritten by comment

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-217 — Unreleased result hidden from portal

Difficulty: Hard. Execution sequence: 221. Description sections: 14.3, 14.4, 20.4.

Preconditions/data: Published staff result not released; linked patient login

1. Open portal results
2. Navigate to observed staff result URL as patient

Acceptance criteria:

- C1: Unreleased result content is withheld
- C2: No indirect detail page reveals it

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-218 — Release result to patient

Difficulty: Hard. Execution sequence: 222. Description sections: 14.3, 14.4, 20.4.

Preconditions/data: Reviewed result eligible for release

1. Release as physician
2. Sign in linked patient
3. Open results

Acceptance criteria:

- C1: Released result becomes visible with correct value unit and date
- C2: Only linked patient sees it

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-219 — Other patient's released result denied

Difficulty: Hard. Execution sequence: 223. Description sections: 14.3, 14.4, 20.4.

Preconditions/data: Released result for B; patient A session; B URL observed as authorized staff

1. Navigate directly to B result URL as A

Acceptance criteria:

- C1: B result value and identity are not disclosed
- C2: Access is denied safely

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-220 — Result table panels remain distinguishable

Difficulty: Medium. Execution sequence: 224. Description sections: 14.3, 14.4, 20.4.

Preconditions/data: Patient with CBC CMP HbA1c lipid TSH and urinalysis fixtures

1. Open each result from list
2. Inspect labels and data

Acceptance criteria:

- C1: Each supported test displays its own name and values
- C2: One generic result is not reused misleadingly across tests

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-221 — Missing result value validation

Difficulty: Medium. Execution sequence: 225. Description sections: 14.3, 14.4, 20.4.

Preconditions/data: Result entry form with required value blank

1. Complete other fields
2. Submit

Acceptance criteria:

- C1: Incomplete result cannot be published
- C2: Missing value error preserves entered context

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-222 — Review status does not equal patient release

Difficulty: Hard. Execution sequence: 226. Description sections: 14.3, 14.4, 20.4.

Preconditions/data: Unreviewed unreleased result

1. Mark reviewed only
2. Open linked patient portal

Acceptance criteria:

- C1: Result remains hidden until explicit permitted release
- C2: Reviewed and Released are distinguishable states

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-223 — Result timestamp ordering

Difficulty: Medium. Execution sequence: 227. Description sections: 14.3, 14.4, 20.4.

Preconditions/data: Two published results with different timestamps

1. Open chart Results
2. Change available sort or inspect default chronological order

Acceptance criteria:

- C1: Timestamps identify each result
- C2: Order follows displayed sort direction

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-224 — Published result preserves source order context

Difficulty: Hard. Execution sequence: 228. Description sections: 14.3, 14.4, 20.4.

Preconditions/data: Result for A order with encounter E

1. Open result
2. Follow order and encounter links

Acceptance criteria:

- C1: Patient order service and encounter match
- C2: Review/release never moves result to another encounter

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

## Insurance coverage and eligibility (16)

### AF3-225 — Add primary insurance coverage

Difficulty: Medium. Execution sequence: 229. Description sections: 15.

Preconditions/data: Patient A; synthetic payer/plan/member/subscriber data

1. Choose Add insurance
2. Complete all policy fields
3. Save
4. Reload chart coverage

Acceptance criteria:

- C1: Payer plan member group subscriber relationship dates and primary designation persist

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-226 — Add secondary coverage

Difficulty: Medium. Execution sequence: 230. Description sections: 15.

Preconditions/data: Patient with primary policy; distinct synthetic secondary policy

1. Add secondary insurance
2. Save
3. Inspect both policies

Acceptance criteria:

- C1: Both policies remain distinct
- C2: Secondary does not silently replace primary

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-227 — Edit insurance member information

Difficulty: Medium. Execution sequence: 231. Description sections: 15.

Preconditions/data: Existing editable policy

1. Change member/group identifiers to valid synthetic values
2. Save
3. Reload

Acceptance criteria:

- C1: New identifiers persist
- C2: Patient and payer association remain correct

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-228 — Insurance required-field validation

Difficulty: Medium. Execution sequence: 232. Description sections: 15.

Preconditions/data: New policy with required member ID blank

1. Fill other fields
2. Submit
3. Correct missing value

Acceptance criteria:

- C1: Required field is identified
- C2: Valid values and selected patient survive error
- C3: Corrected policy saves

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-229 — Coverage date interval validation

Difficulty: Medium. Execution sequence: 233. Description sections: 15.

Preconditions/data: New policy with expiration earlier than effective date

1. Enter inverted dates
2. Submit

Acceptance criteria:

- C1: Inconsistent coverage interval is rejected or explicitly flagged as invalid
- C2: It cannot be silently treated as valid active coverage

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-230 — Active eligibility simulation

Difficulty: Medium. Execution sequence: 234. Description sections: 15.

Preconditions/data: Policy mapped to documented deterministic Active scenario

1. Run simulated eligibility verification
2. Inspect result

Acceptance criteria:

- C1: Active status timestamp copay deductible and out-of-pocket details are visible as synthetic

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-231 — Inactive eligibility simulation

Difficulty: Medium. Execution sequence: 235. Description sections: 15.

Preconditions/data: Policy mapped to deterministic Inactive scenario

1. Run verification
2. Open coverage workqueue

Acceptance criteria:

- C1: Inactive status is shown
- C2: Issue enters appropriate failure workqueue

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-232 — Coverage not found scenario

Difficulty: Medium. Execution sequence: 236. Description sections: 15.

Preconditions/data: Policy mapped to deterministic Not Found scenario

1. Run verification
2. Inspect feedback

Acceptance criteria:

- C1: Coverage Not Found is distinct from Active or generic success
- C2: Retry/correction path is understandable

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-233 — Verification pending scenario

Difficulty: Medium. Execution sequence: 237. Description sections: 15.

Preconditions/data: Policy mapped to deterministic Pending scenario

1. Run verification
2. Reload details

Acceptance criteria:

- C1: Verification Pending remains distinguishable
- C2: UI does not falsely report completed verification

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-234 — Verification error scenario

Difficulty: Medium. Execution sequence: 238. Description sections: 15.

Preconditions/data: Policy mapped to deterministic Error scenario

1. Run verification
2. Inspect recovery controls

Acceptance criteria:

- C1: Verification Error is explicit
- C2: Existing policy information remains and correction/retry is possible

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-235 — Eligibility history on reverification

Difficulty: Medium. Execution sequence: 239. Description sections: 15.

Preconditions/data: Policy previously verified; documented scenario can be changed via permitted UI

1. Update allowed scenario-driving policy field
2. Reverify
3. Open history

Acceptance criteria:

- C1: New timestamp and result are recorded
- C2: Prior verification outcome remains traceable

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-236 — Expired coverage queue

Difficulty: Medium. Execution sequence: 240. Description sections: 15.

Preconditions/data: Policy whose expiration precedes evaluation date

1. Open insurance workqueue
2. Filter expired coverage

Acceptance criteria:

- C1: Policy is identified as expired
- C2: Patient and affected appointment context are available

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-237 — Missing member ID queue

Difficulty: Medium. Execution sequence: 241. Description sections: 15.

Preconditions/data: Existing deliberately incomplete synthetic policy fixture

1. Open insurance workqueue
2. Filter missing identifiers

Acceptance criteria:

- C1: Missing member ID issue is visible
- C2: Correct policy and patient are linked

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-238 — Unverified appointment queue

Difficulty: Medium. Execution sequence: 242. Description sections: 15.

Preconditions/data: Upcoming appointment with unverified coverage

1. Open unverified appointment queue
2. Verify coverage through UI
3. Return

Acceptance criteria:

- C1: Appointment is initially flagged
- C2: Queue updates after successful verification

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-239 — Authorization requirement flag true/false

Difficulty: Medium. Execution sequence: 243. Description sections: 15.

Preconditions/data: Policy or related service form exposes authorization-required checkbox

1. Read explanation
2. Save checked
3. Reload
4. Save unchecked
5. Reload

Acceptance criteria:

- C1: Both true and false persist
- C2: Requirement meaning is explained

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-240 — Insurance coverage stays patient-scoped

Difficulty: Hard. Execution sequence: 244. Description sections: 15.

Preconditions/data: A policy; patient B portal session; policy URL observed by staff

1. Open recorded A policy page as B

Acceptance criteria:

- C1: A coverage/member data are not disclosed
- C2: Unauthorized edit is not possible

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

## Charge capture and coding (16)

### AF3-241 — Signed/completed encounter billing eligibility

Difficulty: Medium. Execution sequence: 245. Description sections: 16.1, 16.2.

Preconditions/data: Completed signed encounter without charges

1. Open unbilled encounters
2. Locate encounter
3. Open charge capture

Acceptance criteria:

- C1: Eligible encounter appears with correct patient provider and service context

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-242 — Unsigned encounter cannot masquerade as billable completion

Difficulty: Hard. Execution sequence: 246. Description sections: 16.1, 16.2.

Preconditions/data: Unsigned incomplete encounter

1. Open unbilled/charge workflow
2. Attempt final charge approval if exposed

Acceptance criteria:

- C1: Workflow does not claim encounter is signed/completed
- C2: Any required completion gate is enforced

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-243 — Create charge from encounter

Difficulty: Medium. Execution sequence: 247. Description sections: 16.1, 16.2.

Preconditions/data: Eligible encounter; curated procedure; one unit; amount 125.00

1. Create charge
2. Save
3. Reload

Acceptance criteria:

- C1: Patient encounter provider diagnosis procedure units amount and billing status persist

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-244 — Multiple charge units total

Difficulty: Medium. Execution sequence: 248. Description sections: 16.1, 16.2.

Preconditions/data: Eligible charge; documented unit-price semantics; price 75.00 units 3

1. Set price and units
2. Save
3. Inspect extended total

Acceptance criteria:

- C1: Extended amount is 225.00 under recorded unit-price semantics
- C2: Field labels make amount basis clear

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-245 — ICD-10-CM coding selection

Difficulty: Medium. Execution sequence: 249. Description sections: 16.1, 16.2.

Preconditions/data: Eligible encounter diagnosis; curated code

1. Search diagnosis catalog
2. Assign code
3. Save

Acceptance criteria:

- C1: Selected code and label persist
- C2: Encounter association remains correct

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-246 — CPT/HCPCS procedure selection

Difficulty: Medium. Execution sequence: 250. Description sections: 16.1, 16.2.

Preconditions/data: Charge with curated procedure selector

1. Search procedure code
2. Choose code
3. Save

Acceptance criteria:

- C1: Procedure code and label match selection
- C2: Catalog is described as a curated demonstration

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-247 — Link diagnosis to procedure

Difficulty: Medium. Execution sequence: 251. Description sections: 16.1, 16.2.

Preconditions/data: Encounter with two diagnoses and a charge

1. Choose second diagnosis for charge
2. Save
3. Reopen

Acceptance criteria:

- C1: Charge links to intended diagnosis
- C2: Unselected diagnosis is not substituted

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-248 — Missing diagnosis code warning

Difficulty: Medium. Execution sequence: 252. Description sections: 16.1, 16.2.

Preconditions/data: Editable charge with missing required diagnosis code

1. Open coding review
2. Attempt approval

Acceptance criteria:

- C1: Missing code issue is readable
- C2: Invalid charge cannot silently pass required coding gate

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-249 — Missing procedure code warning

Difficulty: Medium. Execution sequence: 253. Description sections: 16.1, 16.2.

Preconditions/data: Editable charge without required procedure code

1. Run coding review
2. Attempt approval

Acceptance criteria:

- C1: Procedure deficiency is identified
- C2: Missing code is not replaced with invented code

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-250 — Duplicate charge detection

Difficulty: Hard. Execution sequence: 254. Description sections: 16.1, 16.2.

Preconditions/data: Existing charge for service fixture

1. Attempt equivalent second charge using same encounter service/date/units
2. Review

Acceptance criteria:

- C1: Potential duplicate is detected under documented rule
- C2: Duplicate is not silently accepted as a clean unique charge

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-251 — Coding review completion

Difficulty: Medium. Execution sequence: 255. Description sections: 16.1, 16.2.

Preconditions/data: Complete valid charge

1. Perform coding review
2. Save review decision
3. Reload

Acceptance criteria:

- C1: Review state is recorded
- C2: Charge data remain unchanged

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-252 — Charge approval

Difficulty: Medium. Execution sequence: 256. Description sections: 16.1, 16.2.

Preconditions/data: Reviewed valid charge

1. Approve charge
2. Open billing workqueue

Acceptance criteria:

- C1: Approved status persists
- C2: Charge becomes available to permitted claim workflow

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-253 — Correct coding issue and re-review

Difficulty: Medium. Execution sequence: 257. Description sections: 16.1, 16.2.

Preconditions/data: Charge with known missing code warning

1. Select valid code
2. Save
3. Run coding review again

Acceptance criteria:

- C1: Resolved issue disappears from current review
- C2: New review does not retain stale blocking status

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-254 — Invalid charge amount

Difficulty: Medium. Execution sequence: 258. Description sections: 16.1, 16.2.

Preconditions/data: Charge form; negative amount

1. Enter -10.00
2. Submit

Acceptance criteria:

- C1: Negative charge cannot be approved as ordinary positive service charge
- C2: Validation preserves other fields

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-255 — Invalid charge units

Difficulty: Medium. Execution sequence: 259. Description sections: 16.1, 16.2.

Preconditions/data: Charge form with units 0 or negative

1. Enter invalid units
2. Submit

Acceptance criteria:

- C1: Invalid units are rejected
- C2: No malformed charge is created

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-256 — Coding role cannot silently sign clinical note

Difficulty: Hard. Execution sequence: 260. Description sections: 16.1, 16.2.

Preconditions/data: coder.demo; unsigned encounter underlying charge

1. Open associated note
2. Attempt available signing page/action

Acceptance criteria:

- C1: Clinical note remains unsigned
- C2: Coding permissions do not grant physician signature

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

## Claim validation and payer lifecycle (26)

### AF3-257 — Generate draft claim from approved charges

Difficulty: Medium. Execution sequence: 261. Description sections: 16.3, 16.4, 16.5, 16.6.

Preconditions/data: Approved charges 125.00 and 75.00 for same eligible encounter

1. Generate claim
2. Open detail

Acceptance criteria:

- C1: Draft claim has correct patient provider service date payer diagnoses procedures and total 200.00

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-258 — Claim current stage and next action

Difficulty: Easy. Execution sequence: 262. Description sections: 16.3, 16.4, 16.5, 16.6.

Preconditions/data: Claim at Ready for Review

1. Open detail top area
2. Inspect workflow guidance

Acceptance criteria:

- C1: Current stage and authorized next action are adjacent and clear
- C2: Secondary actions are separate

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-259 — Claim ready for review transition

Difficulty: Medium. Execution sequence: 263. Description sections: 16.3, 16.4, 16.5, 16.6.

Preconditions/data: Complete draft claim

1. Move to Ready for Review
2. Reload

Acceptance criteria:

- C1: State persists
- C2: History records transition

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-260 — Not yet validated differs from clean validation

Difficulty: Medium. Execution sequence: 264. Description sections: 16.3, 16.4, 16.5, 16.6.

Preconditions/data: New claim never scrubbed

1. Open validation section
2. Run clean validation
3. Reopen

Acceptance criteria:

- C1: Initial state says not yet validated
- C2: After success no errors and no warnings are distinguishable from unvalidated state

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-261 — Missing diagnosis scrub error

Difficulty: Medium. Execution sequence: 7. Description sections: 16.3, 16.4, 16.5, 16.6.

Preconditions/data: Claim fixture without required diagnosis

1. Run validation

Acceptance criteria:

- C1: Readable blocking diagnosis error appears
- C2: Claim is not submission-ready

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-262 — Missing procedure scrub error

Difficulty: Medium. Execution sequence: 265. Description sections: 16.3, 16.4, 16.5, 16.6.

Preconditions/data: Claim fixture lacking required procedure code

1. Run validation

Acceptance criteria:

- C1: Readable procedure error appears
- C2: Claim is not submission-ready

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-263 — Missing insurance scrub error

Difficulty: Medium. Execution sequence: 266. Description sections: 16.3, 16.4, 16.5, 16.6.

Preconditions/data: Claim fixture without coverage

1. Run validation

Acceptance criteria:

- C1: Missing insurance is identified
- C2: Validation does not invent a payer

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-264 — Invalid member format scrub error

Difficulty: Medium. Execution sequence: 267. Description sections: 16.3, 16.4, 16.5, 16.6.

Preconditions/data: Claim with member identifier invalid under documented simulator rule

1. Run validation

Acceptance criteria:

- C1: Member-format error explains required correction
- C2: Claim cannot be submitted with blocking error

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-265 — Missing provider scrub error

Difficulty: Medium. Execution sequence: 268. Description sections: 16.3, 16.4, 16.5, 16.6.

Preconditions/data: Deliberately incomplete claim fixture with no required provider

1. Run validation

Acceptance criteria:

- C1: Missing-provider error is displayed
- C2: Claim is not falsely Validated

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-266 — Duplicate claim scrub error

Difficulty: Medium. Execution sequence: 269. Description sections: 16.3, 16.4, 16.5, 16.6.

Preconditions/data: Existing claim; equivalent second claim fixture

1. Run validation on duplicate candidate

Acceptance criteria:

- C1: Duplicate issue references relevant conflict
- C2: Candidate is not silently treated as clean

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-267 — Incomplete demographics scrub error

Difficulty: Medium. Execution sequence: 270. Description sections: 16.3, 16.4, 16.5, 16.6.

Preconditions/data: Claim fixture with a required demographic item missing

1. Run validation

Acceptance criteria:

- C1: Specific demographic deficiency appears
- C2: Blocking issue prevents submission

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-268 — Missing required authorization scrub error

Difficulty: Medium. Execution sequence: 271. Description sections: 16.3, 16.4, 16.5, 16.6.

Preconditions/data: Service requires authorization; no valid linked approval

1. Run validation

Acceptance criteria:

- C1: Missing authorization issue is displayed
- C2: Submission is blocked until gate is satisfied

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-269 — Validation errors and warnings separately rendered

Difficulty: Medium. Execution sequence: 272. Description sections: 16.3, 16.4, 16.5, 16.6.

Preconditions/data: Deterministic fixture producing an error and a warning

1. Run validation
2. Inspect sections

Acceptance criteria:

- C1: Each issue is readable and correctly classified
- C2: No raw array dictionary or empty-list syntax appears

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-270 — Blocking validation prevents submission

Difficulty: Hard. Execution sequence: 273. Description sections: 16.3, 16.4, 16.5, 16.6.

Preconditions/data: Claim currently Validation Failed with known blocking error

1. Attempt Submit via exposed action or previously observed submit page

Acceptance criteria:

- C1: No Submitted state or payer response is created
- C2: Blocking reason remains visible

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-271 — Claim input change invalidates clean validation

Difficulty: Hard. Execution sequence: 274. Description sections: 16.3, 16.4, 16.5, 16.6.

Preconditions/data: Validated unsubmitted claim

1. Change editable member ID or charge input affecting validation
2. Save
3. Inspect validation and attempt submit

Acceptance criteria:

- C1: Old clean validation is invalidated
- C2: Required revalidation occurs before submission

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-272 — Correct claim and validate successfully

Difficulty: Medium. Execution sequence: 275. Description sections: 16.3, 16.4, 16.5, 16.6.

Preconditions/data: Claim with one known correctable error

1. Correct offending field
2. Save
3. Run validation

Acceptance criteria:

- C1: Blocking issue clears
- C2: State becomes Validated only after successful fresh validation

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-273 — Submit validated claim

Difficulty: Medium. Execution sequence: 276. Description sections: 16.3, 16.4, 16.5, 16.6.

Preconditions/data: Validated claim; deterministic accepted scenario

1. Submit simulated claim
2. Reload history

Acceptance criteria:

- C1: State becomes Submitted or documented subsequent deterministic state
- C2: Submission timestamp and event are recorded
- C3: No real payer transmission is claimed

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-274 — Payer accepted response

Difficulty: Medium. Execution sequence: 277. Description sections: 16.3, 16.4, 16.5, 16.6.

Preconditions/data: Submitted claim mapped to Accepted scenario

1. Run documented local payer simulation
2. Reload

Acceptance criteria:

- C1: Accepted response and history are recorded
- C2: No denial or payment is fabricated

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-275 — Payer rejected response

Difficulty: Medium. Execution sequence: 278. Description sections: 16.3, 16.4, 16.5, 16.6.

Preconditions/data: Submitted claim mapped to Rejected scenario

1. Run local payer simulation
2. Open rejection details

Acceptance criteria:

- C1: Rejected status includes reason and correction path
- C2: Original submission history remains

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-276 — Payer denied response

Difficulty: Medium. Execution sequence: 279. Description sections: 16.3, 16.4, 16.5, 16.6.

Preconditions/data: Submitted eligible claim mapped to Denied scenario

1. Run local payer simulation
2. Open denial queue

Acceptance criteria:

- C1: Denied status appears
- C2: Associated denial entry is created

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-277 — Payer partially paid response

Difficulty: Medium. Execution sequence: 280. Description sections: 16.3, 16.4, 16.5, 16.6.

Preconditions/data: Adjudicable claim mapped to partial-payment scenario with specified amount

1. Run simulation
2. Open claim and payment history

Acceptance criteria:

- C1: Partially Paid status and posted amount match deterministic scenario
- C2: Remaining balance reconciles

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-278 — Payer paid response

Difficulty: Medium. Execution sequence: 281. Description sections: 16.3, 16.4, 16.5, 16.6.

Preconditions/data: Eligible claim mapped to full-payment scenario

1. Run simulation
2. Inspect balance and history

Acceptance criteria:

- C1: Paid state has zero outstanding balance
- C2: One simulated payment event or documented adjudication payment record is traceable

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-279 — Adjudication stage progression

Difficulty: Medium. Execution sequence: 282. Description sections: 16.3, 16.4, 16.5, 16.6.

Preconditions/data: Accepted claim with documented adjudication workflow

1. Record simulated adjudication
2. Reload

Acceptance criteria:

- C1: Adjudicated state or documented resolved payment state is recorded
- C2: History preserves Accepted-to-adjudication progression

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-280 — Close fully settled claim

Difficulty: Medium. Execution sequence: 283. Description sections: 16.3, 16.4, 16.5, 16.6.

Preconditions/data: Paid claim with zero outstanding balance

1. Choose Close
2. Reload

Acceptance criteria:

- C1: Claim becomes Closed
- C2: Financial history remains visible

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-281 — Invalid claim transition denied

Difficulty: Hard. Execution sequence: 284. Description sections: 16.3, 16.4, 16.5, 16.6.

Preconditions/data: Draft unvalidated claim

1. Try exposed Paid or Close action or previously observed state-action page

Acceptance criteria:

- C1: Draft cannot bypass validation/submission/adjudication gates
- C2: No fabricated settlement occurs

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-282 — Repeated submit from stale browser tab

Difficulty: Hard. Execution sequence: 285. Description sections: 16.3, 16.4, 16.5, 16.6.

Preconditions/data: Validated claim open in two tabs

1. Submit in tab one
2. Use stale Submit in tab two
3. Inspect history

Acceptance criteria:

- C1: Duplicate submission is rejected or safely idempotent
- C2: No unintended second claim or payer transaction appears

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

## Denials and appeals (12)

### AF3-283 — Denial dashboard reconciliation

Difficulty: Medium. Execution sequence: 286. Description sections: 17, 16.4.

Preconditions/data: Known denial fixtures with amounts and payers

1. Open denial dashboard
2. Compare totals with filtered denial rows

Acceptance criteria:

- C1: Count outstanding amount payer/reason groups and aging correspond to visible scope

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-284 — Denial detail links to claim

Difficulty: Medium. Execution sequence: 287. Description sections: 17, 16.4.

Preconditions/data: Existing denied claim

1. Open denial detail
2. Follow Back to claim
3. Open denial edit
4. Follow claim link

Acceptance criteria:

- C1: Both detail and edit expose explicit correct claim links

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-285 — Denial reason categories distinguishable

Difficulty: Medium. Execution sequence: 288. Description sections: 17, 16.4.

Preconditions/data: Fixtures for inactive coverage missing authorization coding mismatch duplicate filing documentation and demographics

1. Filter each available reason
2. Open representative details

Acceptance criteria:

- C1: Each fixture retains its recorded reason
- C2: Reasons are not collapsed into unrelated generic descriptions

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-286 — Add denial investigation note

Difficulty: Medium. Execution sequence: 289. Description sections: 17, 16.4.

Preconditions/data: Open unresolved denial

1. Add unique investigation note
2. Save
3. Reload

Acceptance criteria:

- C1: Note persists with appropriate actor/time association
- C2: Original reason remains

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-287 — Correct permitted claim field

Difficulty: Medium. Execution sequence: 290. Description sections: 17, 16.4.

Preconditions/data: Denial caused by documented member-ID issue

1. Follow related claim
2. Correct allowed member ID
3. Save
4. Return to denial

Acceptance criteria:

- C1: Correction persists
- C2: Original denial remains available

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-288 — Resubmit corrected denial

Difficulty: Hard. Execution sequence: 291. Description sections: 17, 16.4.

Preconditions/data: Denied claim with correctable issue; correction completed

1. Revalidate
2. Submit permitted corrected claim
3. Open claim history

Acceptance criteria:

- C1: Resubmission is recorded
- C2: Prior denial and original submission remain traceable

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-289 — Create appeal draft

Difficulty: Medium. Execution sequence: 292. Description sections: 17, 16.4.

Preconditions/data: Denied claim; synthetic supporting explanation

1. Open appeal creation
2. Enter explanation
3. Save draft
4. Reload

Acceptance criteria:

- C1: Appeal text and claim association persist
- C2: Draft is not falsely transmitted externally

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-290 — Appeal supporting documentation

Difficulty: Medium. Execution sequence: 293. Description sections: 17, 16.4.

Preconditions/data: Appeal draft; supported synthetic attachment/reference workflow

1. Attach or select synthetic supporting document
2. Save
3. Reopen

Acceptance criteria:

- C1: Supporting document remains linked to appeal
- C2: Other patient's documents are not exposed

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-291 — Mark denial resolved

Difficulty: Medium. Execution sequence: 294. Description sections: 17, 16.4.

Preconditions/data: Denial meeting documented resolution conditions

1. Record resolution note
2. Mark resolved
3. Reload workqueue

Acceptance criteria:

- C1: Resolved status persists
- C2: Unresolved queue/count updates appropriately

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-292 — Resolution preserves original outcome

Difficulty: Hard. Execution sequence: 295. Description sections: 17, 16.4.

Preconditions/data: Resolved denial after successful correction

1. Open historical denial and related claim

Acceptance criteria:

- C1: Original denied outcome reason amount and history remain
- C2: Correction does not delete prior outcome

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-293 — Denial payer and reason combined filters

Difficulty: Medium. Execution sequence: 296. Description sections: 17, 16.4.

Preconditions/data: Denials across two payers and reasons

1. Apply payer A and missing-authorization reason
2. Inspect rows
3. Clear one filter

Acceptance criteria:

- C1: Rows follow both active filters
- C2: Clearing one preserves the other

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-294 — Front desk cannot adjudicate denial

Difficulty: Hard. Execution sequence: 297. Description sections: 17, 16.4.

Preconditions/data: frontdesk.demo; observed denial resolution URL

1. Open denial resolution page
2. Try any exposed resolve/appeal submission action

Acceptance criteria:

- C1: Unauthorized financial resolution is denied
- C2: Denial state remains unchanged

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

## Prior authorization (14)

### AF3-295 — Create authorization request draft

Difficulty: Medium. Execution sequence: 298. Description sections: 18, 4.2.

Preconditions/data: Patient A policy; service diagnosis and provider

1. Create request with required fields
2. Save
3. Reload

Acceptance criteria:

- C1: Patient insurance service diagnosis provider dates and Draft status persist

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-296 — Authorization required fields

Difficulty: Medium. Execution sequence: 299. Description sections: 18, 4.2.

Preconditions/data: New request missing service and diagnosis

1. Submit incomplete form

Acceptance criteria:

- C1: Missing required fields are explained
- C2: No invalid submitted authorization is created

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-297 — Authorization insurance scope

Difficulty: Medium. Execution sequence: 300. Description sections: 18, 4.2.

Preconditions/data: Patient A with primary policy; B policy exists

1. Open A request
2. Inspect insurance choices
3. Select A policy

Acceptance criteria:

- C1: Choices obey patient scope
- C2: Request cannot use B-only coverage through visible UI

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-298 — Submit simulated authorization

Difficulty: Medium. Execution sequence: 301. Description sections: 18, 4.2.

Preconditions/data: Complete draft request

1. Submit
2. Reload detail/history

Acceptance criteria:

- C1: Submitted status and date persist
- C2: Request is explicitly simulated

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-299 — Pending Review transition

Difficulty: Medium. Execution sequence: 302. Description sections: 18, 4.2.

Preconditions/data: Submitted request

1. Apply documented pending-review simulated workflow
2. Reload

Acceptance criteria:

- C1: Pending Review state is distinguishable from Approved
- C2: History records transition

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-300 — Additional information requested

Difficulty: Medium. Execution sequence: 303. Description sections: 18, 4.2.

Preconditions/data: Pending request with deterministic additional-information scenario

1. Record simulated information request
2. Open details

Acceptance criteria:

- C1: Requested information and status are visible
- C2: Request is not treated as approved

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-301 — Provide supporting information

Difficulty: Medium. Execution sequence: 304. Description sections: 18, 4.2.

Preconditions/data: Request awaiting information; synthetic supporting document/text

1. Add required supporting material
2. Save/resubmit as offered

Acceptance criteria:

- C1: Supporting content persists
- C2: Workflow reflects response without erasing original request

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-302 — Approved authorization decision

Difficulty: Medium. Execution sequence: 305. Description sections: 18, 4.2.

Preconditions/data: Pending request mapped to approval scenario

1. Record simulated approval and expiration
2. Reload

Acceptance criteria:

- C1: Approved status service scope and expiration persist

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-303 — Denied authorization decision

Difficulty: Medium. Execution sequence: 306. Description sections: 18, 4.2.

Preconditions/data: Pending request mapped to denial scenario

1. Record simulated denial with reason
2. Reload

Acceptance criteria:

- C1: Denied status and reason persist
- C2: Related service is not shown as authorized

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-304 — Expired authorization

Difficulty: Medium. Execution sequence: 307. Description sections: 18, 4.2.

Preconditions/data: Previously approved fixture with past expiration

1. Open request and relevant service authorization status

Acceptance criteria:

- C1: Expired status or clear expired validity is shown
- C2: It is not treated as currently valid approval

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-305 — Approval satisfies matching claim gate

Difficulty: Hard. Execution sequence: 308. Description sections: 18, 4.2.

Preconditions/data: Claim blocked solely for missing matching authorization; approved matching request

1. Link approval through UI
2. Revalidate claim

Acceptance criteria:

- C1: Authorization error clears for matching patient service and validity period
- C2: Other validation rules still apply

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-306 — Wrong service approval cannot satisfy gate

Difficulty: Hard. Execution sequence: 309. Description sections: 18, 4.2.

Preconditions/data: Approved authorization for service X; claim requires service Y

1. Attempt linking through available UI
2. Validate claim

Acceptance criteria:

- C1: Mismatched approval is rejected or does not clear required gate
- C2: Claim remains blocked appropriately

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-307 — Expired approval cannot satisfy claim gate

Difficulty: Hard. Execution sequence: 310. Description sections: 18, 4.2.

Preconditions/data: Claim requiring currently valid authorization; expired matching approval

1. Link expired approval if allowed
2. Run validation

Acceptance criteria:

- C1: Expired approval does not satisfy current requirement
- C2: Reason is understandable

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-308 — Authorization required checkbox preserves false after error

Difficulty: Hard. Execution sequence: 311. Description sections: 18, 4.2.

Preconditions/data: Request/service form with checkbox and another missing field

1. Set checkbox false
2. Submit invalid form
3. Correct missing field
4. Save
5. Reload

Acceptance criteria:

- C1: Explicit false survives error and save
- C2: UI explains meaning rather than restoring old true value

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

## Payments responsibility and receipts (24)

### AF3-309 — Post simulated insurance payment

Difficulty: Medium. Execution sequence: 312. Description sections: 19, 20, 23.4.

Preconditions/data: Adjudicated claim balance 200.00; permitted staff

1. Post insurance payment 50.00
2. Open receipt and history

Acceptance criteria:

- C1: One 50.00 payment exists
- C2: Outstanding balance becomes 150.00

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-310 — Partial patient payment reduces confirmed responsibility

Difficulty: Medium. Execution sequence: 313. Description sections: 19, 20, 23.4.

Preconditions/data: Adjudicated claim balance 200.00; confirmed responsibility 80.00; linked patient

1. Pay simulated 30.00
2. Reload portal bill and history

Acceptance criteria:

- C1: Responsibility becomes 50.00
- C2: Claim outstanding balance becomes 170.00
- C3: One receipt exists

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-311 — Full confirmed patient responsibility payment

Difficulty: Medium. Execution sequence: 314. Description sections: 19, 20, 23.4.

Preconditions/data: Claim balance 200.00 confirmed patient responsibility 80.00

1. Pay simulated 80.00 as linked patient
2. Reload

Acceptance criteria:

- C1: Patient responsibility becomes zero
- C2: Remaining claim balance 120.00 is not falsely called patient debt

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-312 — Payment cannot exceed total claim balance

Difficulty: Hard. Execution sequence: 315. Description sections: 19, 20, 23.4.

Preconditions/data: Eligible claim balance 50.00; staff payment form

1. Enter 50.01
2. Submit

Acceptance criteria:

- C1: Overpayment is rejected
- C2: Balance and payment count remain unchanged

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-313 — Patient cannot exceed confirmed responsibility

Difficulty: Hard. Execution sequence: 316. Description sections: 19, 20, 23.4.

Preconditions/data: Claim balance 200.00 responsibility 40.00; patient payment form

1. Enter 40.01
2. Submit

Acceptance criteria:

- C1: Payment is rejected even though total balance is larger
- C2: Responsibility and history are unchanged

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-314 — Unconfirmed responsibility withholds patient payment

Difficulty: Hard. Execution sequence: 10. Description sections: 19, 20, 23.4.

Preconditions/data: Adjudicated claim with positive balance but no confirmed patient responsibility

1. Open portal bill
2. Try observed related payment page if available

Acceptance criteria:

- C1: Bill says awaiting billing review or equivalent
- C2: Patient cannot pay unconfirmed amount

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-315 — Denied balance is not automatically patient debt

Difficulty: Hard. Execution sequence: 317. Description sections: 19, 20, 23.4.

Preconditions/data: Denied claim with positive balance and no confirmed patient responsibility

1. Open linked patient bills

Acceptance criteria:

- C1: Denied balance is not labeled as amount patient owes
- C2: Patient payment action is withheld

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-316 — Staff confirms adjudicated responsibility

Difficulty: Medium. Execution sequence: 318. Description sections: 19, 20, 23.4.

Preconditions/data: Adjudicated claim balance 200.00 with no prior responsibility confirmation

1. Confirm responsibility 75.00 as authorized billing staff
2. Open portal as patient

Acceptance criteria:

- C1: Patient owes 75.00 explicitly
- C2: Confirmation is auditable and separate from 200.00 total balance

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-317 — Responsibility cannot exceed outstanding balance

Difficulty: Hard. Execution sequence: 319. Description sections: 19, 20, 23.4.

Preconditions/data: Adjudicated claim balance 200.00

1. Attempt confirm responsibility 200.01

Acceptance criteria:

- C1: Out-of-bounds confirmation is rejected
- C2: Previous responsibility amount is preserved

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-318 — Responsibility cannot be confirmed before adjudication

Difficulty: Hard. Execution sequence: 320. Description sections: 19, 20, 23.4.

Preconditions/data: Unadjudicated Draft or Submitted claim

1. Open observed responsibility page
2. Attempt confirmation if offered

Acceptance criteria:

- C1: Confirmation is denied in ineligible state
- C2: Portal does not gain payable responsibility

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-319 — Patient cannot confirm their own responsibility

Difficulty: Hard. Execution sequence: 321. Description sections: 19, 20, 23.4.

Preconditions/data: Patient session; staff confirmation URL observed on own claim

1. Navigate to confirmation URL
2. Attempt exposed action

Acceptance criteria:

- C1: Unauthorized confirmation is rejected
- C2: Financial responsibility is unchanged

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-320 — Staff payment blocked in invalid claim state

Difficulty: Hard. Execution sequence: 322. Description sections: 19, 20, 23.4.

Preconditions/data: Draft unadjudicated claim with charges

1. Open observed payment page
2. Attempt positive payment if exposed

Acceptance criteria:

- C1: Payment is rejected due to state
- C2: No receipt or payment history entry is created

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-321 — Paid/closed claims do not invite payment

Difficulty: Hard. Execution sequence: 323. Description sections: 19, 20, 23.4.

Preconditions/data: Paid claim and Closed claim with zero balance

1. Open each as staff
2. Visit prior payment URL if known

Acceptance criteria:

- C1: Payment action is absent or disabled
- C2: Direct navigation cannot submit additional positive payment

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-322 — Zero and negative payments rejected

Difficulty: Medium. Execution sequence: 324. Description sections: 19, 20, 23.4.

Preconditions/data: Eligible claim with positive balance

1. Enter 0 and submit
2. Enter -1 where possible and submit

Acceptance criteria:

- C1: Neither amount posts a payment
- C2: Readable amount validation is shown

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-323 — Receipt refresh is idempotent

Difficulty: Hard. Execution sequence: 325. Description sections: 19, 20, 23.4.

Preconditions/data: New successful simulated 25.00 payment

1. Reload receipt twice
2. Inspect payment history

Acceptance criteria:

- C1: Only one 25.00 payment exists
- C2: Balance changes once

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-324 — Back navigation does not restore ready-to-pay stale form

Difficulty: Hard. Execution sequence: 326. Description sections: 19, 20, 23.4.

Preconditions/data: Successful payment from form

1. Press Back
2. Inspect restored page
3. Reload if needed

Acceptance criteria:

- C1: Completed form is not presented as ready for duplicate submission
- C2: History shows one payment

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-325 — Two-tab stale-balance protection

Difficulty: Hard. Execution sequence: 327. Description sections: 19, 20, 23.4.

Preconditions/data: Claim balance and responsibility 50.00; same payment form in two tabs

1. Pay 50.00 in tab one
2. Attempt 50.00 from tab two

Acceptance criteria:

- C1: Second attempt is rejected or safely deduplicated
- C2: Balance never becomes negative

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-326 — Staff receipt return paths

Difficulty: Medium. Execution sequence: 328. Description sections: 19, 20, 23.4.

Preconditions/data: Successful staff payment

1. Open receipt
2. Use related claim link
3. Return to receipt and payment history

Acceptance criteria:

- C1: Prominent correct claim and history navigation works
- C2: Updated balance is displayed to authorized staff

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-327 — Patient receipt return path and role scope

Difficulty: Medium. Execution sequence: 329. Description sections: 19, 20, 23.4.

Preconditions/data: Successful patient payment

1. Open receipt
2. Return to portal bills
3. Inspect available claim links

Acceptance criteria:

- C1: Portal return is prominent
- C2: Staff-only claim detail is not exposed to patient
- C3: Receipt offers print action

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-328 — Print receipt preview

Difficulty: Medium. Execution sequence: 330. Description sections: 19, 20, 23.4.

Preconditions/data: Successful simulated payment receipt

1. Activate Print
2. Inspect browser print preview
3. Cancel printing

Acceptance criteria:

- C1: Preview contains correct patient-safe amount date and transaction reference
- C2: No extra payment is posted

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-329 — Money formatting across billing

Difficulty: Medium. Execution sequence: 331. Description sections: 19, 20, 23.4.

Preconditions/data: Claim/statement/receipt values including 1234.50 and zero

1. Open financial views
2. Inspect amount labels

Acceptance criteria:

- C1: Amounts display currency symbol thousands separator and two decimals
- C2: Zero uses $0.00 where currency is displayed

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-330 — Payment allocated to intended claim

Difficulty: Hard. Execution sequence: 332. Description sections: 19, 20, 23.4.

Preconditions/data: Patient with two claims A balance 200 and B balance 300

1. Post 50 to A
2. Open both claim histories and account balance

Acceptance criteria:

- C1: A becomes 150 B stays 300
- C2: Account outstanding sum decreases by exactly 50

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-331 — Statement and payment history reconciliation

Difficulty: Medium. Execution sequence: 333. Description sections: 19, 20, 23.4.

Preconditions/data: Patient with known charges payments and confirmed responsibility

1. Open statement and payment history
2. Compare to claims

Acceptance criteria:

- C1: Statement totals reconcile with displayed records and scope
- C2: Confirmed patient amount is distinguishable from payer balance

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-332 — Other patient's receipt inaccessible

Difficulty: Hard. Execution sequence: 334. Description sections: 19, 20, 23.4.

Preconditions/data: Receipt for B; patient A session; URL observed by authorized user

1. Navigate to B receipt URL

Acceptance criteria:

- C1: B receipt and payment details are withheld
- C2: No print view bypass exposes them

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

## Patient portal workflows (18)

### AF3-333 — Portal health overview shortcuts

Difficulty: Easy. Execution sequence: 335. Description sections: 20, 20.1, 20.3.

Preconditions/data: Patient with upcoming visit results medications messages and bills

1. Open dashboard
2. Inspect and follow primary shortcuts

Acceptance criteria:

- C1: Messages appointments results medications and bills are discoverable
- C2: Health overview is not displaced by large empty forms

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-334 — Upcoming appointment detail

Difficulty: Medium. Execution sequence: 336. Description sections: 20, 20.1, 20.3.

Preconditions/data: Patient with future appointment

1. Open upcoming appointment
2. Inspect provider time location/type and status

Acceptance criteria:

- C1: Details match staff scheduling record
- C2: Only own appointment is shown

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-335 — Request new appointment

Difficulty: Medium. Execution sequence: 337. Description sections: 20, 20.1, 20.3.

Preconditions/data: Patient A; requested provider/date/reason

1. Submit appointment request
2. Open staff scheduling workflow

Acceptance criteria:

- C1: Request persists with A and requested preferences
- C2: Staff can find request without it being falsely presented as confirmed booking

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-336 — Cancel eligible portal appointment

Difficulty: Medium. Execution sequence: 338. Description sections: 20, 20.1, 20.3.

Preconditions/data: Own appointment eligible under documented cancellation rules

1. Cancel
2. Confirm
3. Reload portal and staff schedule

Acceptance criteria:

- C1: Cancelled status appears consistently
- C2: No unrelated appointment changes

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-337 — Ineligible portal cancellation denied

Difficulty: Hard. Execution sequence: 339. Description sections: 20, 20.1, 20.3.

Preconditions/data: Own completed or otherwise ineligible appointment

1. Try cancellation through exposed action or recorded cancellation page

Acceptance criteria:

- C1: Cancellation is blocked with clear status/rule
- C2: Historical completed appointment remains intact

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-338 — Complete simulated pre-check-in

Difficulty: Medium. Execution sequence: 340. Description sections: 20, 20.1, 20.3.

Preconditions/data: Upcoming appointment with portal pre-check-in

1. Complete required contact consent and intake steps
2. Submit
3. Open staff check-in

Acceptance criteria:

- C1: Submitted information persists
- C2: Staff can see pre-check-in progress without falsely starting physician care

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-339 — Visit summary accessible

Difficulty: Medium. Execution sequence: 341. Description sections: 20, 20.1, 20.3.

Preconditions/data: Own encounter with patient-visible signed visit summary

1. Open recent visit summary

Acceptance criteria:

- C1: Correct visit date instructions and permitted clinical summary appear
- C2: No other patient's documentation is included

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-340 — Released results shortcut

Difficulty: Easy. Execution sequence: 342. Description sections: 20, 20.1, 20.3.

Preconditions/data: Patient with one released and one unreleased result

1. Open results shortcut
2. Inspect recent list

Acceptance criteria:

- C1: Released result is discoverable
- C2: Unreleased result is absent from patient list

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-341 — Renewal action adjacent to medication

Difficulty: Easy. Execution sequence: 343. Description sections: 20, 20.1, 20.3.

Preconditions/data: Patient with two active medications

1. Open medication section
2. Inspect each medication card

Acceptance criteria:

- C1: Each eligible medication has an adjacent clearly named Request medication renewal action
- C2: Buttons identify the relevant medication context

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-342 — Submit medication renewal request

Difficulty: Medium. Execution sequence: 344. Description sections: 20, 20.1, 20.3.

Preconditions/data: Own active medication eligible for renewal

1. Request renewal with synthetic comment
2. Submit
3. Open staff renewal queue

Acceptance criteria:

- C1: Request identifies correct medication and patient
- C2: No prescription is automatically signed

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-343 — Renewal request status discoverable

Difficulty: Medium. Execution sequence: 345. Description sections: 20, 20.1, 20.3.

Preconditions/data: Existing submitted renewal request

1. Return to medication/request area
2. Inspect status/history

Acceptance criteria:

- C1: Submitted request is acknowledged and distinguishable from a completed prescription
- C2: Patient is not misled that refill was transmitted

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-344 — Contact update permitted fields

Difficulty: Medium. Execution sequence: 346. Description sections: 20, 20.1, 20.3.

Preconditions/data: Patient A with known phone/address

1. Update permitted contact fields
2. Save
3. Open staff demographics

Acceptance criteria:

- C1: Changed contact fields persist consistently
- C2: Protected clinical identifiers are not silently edited

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-345 — Portal does not allow protected demographic edits

Difficulty: Hard. Execution sequence: 347. Description sections: 20, 20.1, 20.3.

Preconditions/data: Patient account; protected MRN or role field visible only to staff

1. Open personal-information form
2. Try recorded staff edit URL if available

Acceptance criteria:

- C1: Patient cannot alter MRN staff role or another patient's identity
- C2: Permitted contact editing remains separate

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-346 — Portal narrow layout and compact summaries

Difficulty: Medium. Execution sequence: 348. Description sections: 20, 20.1, 20.3.

Preconditions/data: 390x844 viewport; populated patient dashboard

1. Inspect health cards appointment request and contact sections
2. Use one shortcut

Acceptance criteria:

- C1: Cards stack readably
- C2: Actions and fields remain visible with adequate spacing
- C3: No oversized empty block obscures main health actions

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-347 — Portal empty clinical sections

Difficulty: Medium. Execution sequence: 349. Description sections: 20, 20.1, 20.3.

Preconditions/data: Synthetic patient with no released results and no upcoming appointment

1. Open portal overview results and appointments

Acceptance criteria:

- C1: Explicit empty states appear
- C2: No invented visit/result is shown
- C3: Request/contact actions remain discoverable

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-348 — Other patient's appointment denied

Difficulty: Hard. Execution sequence: 350. Description sections: 20, 20.1, 20.3.

Preconditions/data: Patient A session; B appointment URL observed while authorized

1. Navigate to B appointment detail/request-edit page

Acceptance criteria:

- C1: B appointment information is withheld
- C2: No cancellation or modification of B appointment is possible

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-349 — Other patient's medication denied

Difficulty: Hard. Execution sequence: 351. Description sections: 20, 20.1, 20.3.

Preconditions/data: Patient A session; B medication/renewal URL observed as staff

1. Open B medication or renewal page

Acceptance criteria:

- C1: B medication data are withheld
- C2: A cannot submit renewal for B

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-350 — Portal bills distinguish financial categories

Difficulty: Medium. Execution sequence: 352. Description sections: 20, 20.1, 20.3.

Preconditions/data: Own claim balance 200 confirmed responsibility 50 and payer portion 150

1. Open bill summary
2. Inspect payable amount and explanation

Acceptance criteria:

- C1: Patient payable amount is 50
- C2: Total claim balance is not mislabeled as confirmed patient responsibility

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

## Messaging unread state and privacy (18)

### AF3-351 — Compose subject and first body atomically

Difficulty: Medium. Execution sequence: 8. Description sections: 22, 20.2.

Preconditions/data: Patient A; empty compose form

1. Enter unique subject and initial body
2. Send
3. Open thread

Acceptance criteria:

- C1: One thread contains both subject and first message
- C2: No empty orphan thread is created

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-352 — Compose error preserves content

Difficulty: Hard. Execution sequence: 353. Description sections: 22, 20.2.

Preconditions/data: Compose with subject entered but required body blank

1. Submit
2. Inspect error
3. Enter body
4. Send

Acceptance criteria:

- C1: Subject survives error
- C2: Successful send creates one complete thread rather than an empty draft artifact

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-353 — Staff reply stays in patient thread

Difficulty: Medium. Execution sequence: 354. Description sections: 22, 20.2.

Preconditions/data: Existing patient A message thread

1. Reply as authorized staff
2. Open as patient

Acceptance criteria:

- C1: Reply appears in same thread with correct patient scope
- C2: No separate unrelated thread is created

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-354 — Sender names timestamps and receipts

Difficulty: Medium. Execution sequence: 355. Description sections: 22, 20.2.

Preconditions/data: Thread containing patient and staff messages

1. Open conversation
2. Inspect messages and read indicators

Acceptance criteria:

- C1: Readable sender names timestamps and available read receipts distinguish each message

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-355 — Navigation unread count updates on incoming message

Difficulty: Medium. Execution sequence: 356. Description sections: 22, 20.2.

Preconditions/data: Staff signed in on active page; patient in separate browser session

1. Patient sends new thread/message
2. Observe staff Messages navigation

Acceptance criteria:

- C1: Incoming unread count increases appropriately within recorded refresh window
- C2: Always discoverable message entry point shows new activity

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-356 — Unread thread visual label

Difficulty: Medium. Execution sequence: 357. Description sections: 22, 20.2.

Preconditions/data: Staff has unread incoming thread

1. Open message list without opening thread

Acceptance criteria:

- C1: Unread thread has explicit label/dot and bold subject
- C2: Read thread is visually distinguishable

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-357 — Opening thread marks displayed messages read

Difficulty: Medium. Execution sequence: 358. Description sections: 22, 20.2.

Preconditions/data: Current user with known unread count and unread thread

1. Open thread
2. Read rendered messages
3. Return to list

Acceptance criteria:

- C1: Displayed incoming messages become read for current user
- C2: Count decreases by corresponding unread unit defined in UI

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-358 — Read-state isolation across authorized staff

Difficulty: Expert. Execution sequence: 359. Description sections: 22, 20.2.

Preconditions/data: Same incoming thread visible to staff A and B; both unread in separate sessions

1. A opens thread
2. Inspect B's list/count without opening thread

Acceptance criteria:

- C1: A's read state clears
- C2: B remains unread
- C3: One staff reader does not clear another's state

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-359 — Own sent messages do not increase unread count

Difficulty: Medium. Execution sequence: 360. Description sections: 22, 20.2.

Preconditions/data: User with known unread baseline

1. Send new message or reply
2. Inspect own count

Acceptance criteria:

- C1: Own outgoing message does not increase sender's unread count

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-360 — New incoming reply restores unread

Difficulty: Hard. Execution sequence: 361. Description sections: 22, 20.2.

Preconditions/data: Thread previously read by staff A

1. Patient replies
2. Observe active staff page
3. Open list

Acceptance criteria:

- C1: Thread becomes unread for A again
- C2: Unread count/marker updates without external push setup

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-361 — Active page refresh without full reload

Difficulty: Hard. Execution sequence: 362. Description sections: 22, 20.2.

Preconditions/data: Staff on non-messages authenticated page; known baseline

1. Send incoming message from patient session
2. Observe staff badge without manual page reload

Acceptance criteria:

- C1: Badge refreshes while page is active within documented or bounded observation window
- C2: No email/SMS is required

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-362 — Unread count respects patient scope

Difficulty: Hard. Execution sequence: 363. Description sections: 22, 20.2.

Preconditions/data: Patients A/B with separate new messages; A portal session

1. Send staff reply only to B
2. Inspect A badge and list

Acceptance criteria:

- C1: A count does not reflect B's message
- C2: No B thread metadata appears

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-363 — Direct other-patient thread denied

Difficulty: Hard. Execution sequence: 364. Description sections: 22, 20.2.

Preconditions/data: Patient A; B thread URL observed by authorized staff

1. Navigate to B thread URL

Acceptance criteria:

- C1: B subject body participants and timestamps are withheld
- C2: No read receipt is falsely attributed to A

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-364 — Direct unauthorized reply denied

Difficulty: Hard. Execution sequence: 365. Description sections: 22, 20.2.

Preconditions/data: Patient A; B reply page URL observed by authorized staff

1. Open B reply page
2. Attempt any exposed reply

Acceptance criteria:

- C1: No message from A is added to B thread
- C2: Unauthorized action is rejected

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-365 — Unread state persists across logout

Difficulty: Medium. Execution sequence: 366. Description sections: 22, 20.2.

Preconditions/data: User opens and reads a thread

1. Sign out
2. Sign in same user
3. Reopen message list

Acceptance criteria:

- C1: Read state persists
- C2: Thread is not reset to unread without new incoming message

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-366 — Message history survives refresh

Difficulty: Medium. Execution sequence: 367. Description sections: 22, 20.2.

Preconditions/data: Thread with three distinct messages

1. Reload conversation
2. Navigate away and back

Acceptance criteria:

- C1: Messages retain content order authors and times
- C2: No duplicate is appended by refresh

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-367 — Read only displayed messages

Difficulty: Hard. Execution sequence: 368. Description sections: 22, 20.2.

Preconditions/data: Thread fixture supports pagination/lazy loading with unread messages not yet displayed

1. Open initial visible segment
2. Inspect count
3. Load remaining messages through UI

Acceptance criteria:

- C1: Only displayed messages are marked read until more are displayed
- C2: If UI displays entire thread at once, all rendered messages may be read and limitation is recorded

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-368 — Messages discoverable by permitted role

Difficulty: Medium. Execution sequence: 369. Description sections: 22, 20.2.

Preconditions/data: Nurse account with authorized patient conversation

1. Locate Messages from role-aware navigation
2. Compose or reply through allowed action

Acceptance criteria:

- C1: Message entry is discoverable with unread indicator
- C2: Permitted conversation can be reached without hidden URL knowledge

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

## AI assistance and unsigned documentation (24)

### AF3-369 — Deterministic demo mode without API key

Difficulty: Medium. Execution sequence: 370. Description sections: 21.

Preconditions/data: Documented local demo mode; synthetic chart

1. Open AI assistant
2. Generate patient summary

Acceptance criteria:

- C1: Summary workflow works without requesting paid API key
- C2: Mode is clearly identified as demo/simulated where appropriate

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-370 — Patient summary grounded in chart

Difficulty: Hard. Execution sequence: 371. Description sections: 21.

Preconditions/data: A chart with known problems medications allergies labs and pending orders

1. Generate summary
2. Compare each factual statement to visible chart

Acceptance criteria:

- C1: Summary covers available major categories
- C2: No unsupported patient facts or another patient's data are asserted

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-371 — Missing chart information not invented

Difficulty: Hard. Execution sequence: 372. Description sections: 21.

Preconditions/data: Synthetic chart lacking allergy/history detail

1. Generate summary
2. Inspect statements about absent categories

Acceptance criteria:

- C1: Absent information is identified as unavailable/unknown rather than fabricated normal or negative findings

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-372 — Encounter preparation from selected appointment

Difficulty: Medium. Execution sequence: 373. Description sections: 21.

Preconditions/data: A future appointment with recent changes and pending tasks

1. Generate encounter preparation
2. Compare visit reason chart changes and tasks

Acceptance criteria:

- C1: Preparation reflects selected appointment context
- C2: Source facts and generated suggestions are distinguishable

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-373 — SOAP drafting from synthetic transcript

Difficulty: Medium. Execution sequence: 374. Description sections: 21.

Preconditions/data: In-progress A encounter; supplied synthetic transcript and chart context

1. Paste transcript
2. Generate SOAP draft

Acceptance criteria:

- C1: Draft has Subjective Objective Assessment and Plan
- C2: Transcript and chart facts are represented without automatic signing

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-374 — Editable AI output correction

Difficulty: Medium. Execution sequence: 375. Description sections: 21.

Preconditions/data: Generated draft with editable text

1. Change one generated sentence to correction marker
2. Save draft output if offered
3. Reopen

Acceptance criteria:

- C1: Clinician correction is retained
- C2: Editable output remains unapproved/unsigned until explicit action

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-375 — Generation application saving signing labels

Difficulty: Easy. Execution sequence: 376. Description sections: 21.

Preconditions/data: Generated note draft ready for application

1. Inspect available actions and explanatory text

Acceptance criteria:

- C1: Apply to unsigned draft or equivalent explicit label appears
- C2: Generation application save and signing are visibly distinct
- C3: Apply explicitly states it does not sign

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-376 — Apply AI output leaves note unsigned

Difficulty: Hard. Execution sequence: 9. Description sections: 21.

Preconditions/data: Unsigned encounter note; reviewed generated draft

1. Apply to unsigned draft
2. Inspect note and encounter status

Acceptance criteria:

- C1: Content transfers to unsigned draft
- C2: No signing clinician timestamp or Signed state is created

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-377 — Save applied draft leaves note unsigned

Difficulty: Hard. Execution sequence: 377. Description sections: 21.

Preconditions/data: Applied AI draft requiring clinician review

1. Complete missing details
2. Save Draft
3. Reload

Acceptance criteria:

- C1: Content persists
- C2: Save is not treated as signature

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-378 — Explicit human review before signing

Difficulty: Hard. Execution sequence: 378. Description sections: 21.

Preconditions/data: AI-applied complete draft and all ordinary sign-off prerequisites

1. Review content and acknowledge required checks
2. Explicitly Sign

Acceptance criteria:

- C1: Signature occurs only after clinician action
- C2: Signing metadata identifies acting clinician

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-379 — AI cannot overwrite signed note

Difficulty: Hard. Execution sequence: 379. Description sections: 21.

Preconditions/data: Signed note with recorded text; generated alternative draft

1. Open AI workflow
2. Attempt Apply to same signed note

Acceptance criteria:

- C1: Signed original is unchanged
- C2: Application is blocked or routed to auditable correction workflow

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-380 — AI objectives include all recorded vitals

Difficulty: Hard. Execution sequence: 380. Description sections: 21.

Preconditions/data: Complete vitals fixture: BP120/80 HR72 RR16 T36.8 SpO2 98 H65in W150lb BMI25.0 pain2

1. Generate SOAP draft
2. Inspect Objective

Acceptance criteria:

- C1: All recorded measurements are present with labels and units
- C2: BMI is consistent with recorded values and pain is included

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-381 — AI missing vitals remain missing

Difficulty: Hard. Execution sequence: 381. Description sections: 21.

Preconditions/data: Encounter with no respiratory rate or pain recorded

1. Generate draft
2. Inspect Objective

Acceptance criteria:

- C1: Absent respiratory rate/pain are not invented
- C2: Present measurements remain accurate

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-382 — AI draft respects selected measurement units

Difficulty: Hard. Execution sequence: 382. Description sections: 21.

Preconditions/data: Encounter saved at 65.37in and 147.29lb

1. Generate draft
2. Compare height/weight to saved vitals

Acceptance criteria:

- C1: Units and represented measurements agree with chart
- C2: No unexplained inches/cm or pounds/kg swap appears

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-383 — Text scribe works without audio backend

Difficulty: Medium. Execution sequence: 383. Description sections: 21.

Preconditions/data: No configured transcription provider; demo text workflow

1. Enter supplied transcript
2. Generate note

Acceptance criteria:

- C1: Text-based workflow remains functional
- C2: UI does not falsely claim recorded/transcribed audio

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-384 — AI preparation does not create diagnoses

Difficulty: Hard. Execution sequence: 384. Description sections: 21.

Preconditions/data: Unsigned encounter; baseline diagnosis list captured

1. Generate encounter preparation
2. Inspect any diagnosis suggestions
3. Reopen encounter diagnosis list without accepting suggestions

Acceptance criteria:

- C1: Generation alone creates no diagnosis
- C2: Any suggestions that are shown remain distinguishable from approved diagnoses

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-385 — AI preparation does not create orders

Difficulty: Hard. Execution sequence: 385. Description sections: 21.

Preconditions/data: Unsigned encounter; baseline order list captured

1. Generate encounter preparation
2. Inspect any suggested orders
3. Reopen order list without approving suggestions

Acceptance criteria:

- C1: No signed or active order is created by generation alone
- C2: Any suggestions remain separate from explicitly accepted orders

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-386 — Documentation gap assistance

Difficulty: Medium. Execution sequence: 386. Description sections: 21.

Preconditions/data: Encounter intentionally missing plan detail; demo assistant supports gap review

1. Generate preparation/gap review
2. Inspect output

Acceptance criteria:

- C1: Missing information is highlighted as a documentation gap
- C2: Assistant does not manufacture missing plan as established fact

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-387 — Source versus suggestion presentation

Difficulty: Medium. Execution sequence: 387. Description sections: 21.

Preconditions/data: Chart fact and generated follow-up suggestion available

1. Generate preparation or summary
2. Inspect organization

Acceptance criteria:

- C1: Known facts and suggested next steps are distinguishable
- C2: Suggestions are not labeled completed care

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-388 — AI patient switch resets context

Difficulty: Hard. Execution sequence: 388. Description sections: 21.

Preconditions/data: Generate summary for A; B has distinct allergy and medication markers

1. Switch to B via visible selector
2. Generate new summary

Acceptance criteria:

- C1: B summary uses B data
- C2: A-specific markers do not leak into B output

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-389 — AI draft persistence and provenance

Difficulty: Medium. Execution sequence: 389. Description sections: 21.

Preconditions/data: Generated draft applied and saved; AI history available

1. Reload encounter
2. Open AI/draft history

Acceptance criteria:

- C1: Saved content persists
- C2: Generated origin and available request/model/prompt information are traceable without invented metadata

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-390 — Empty transcript validation

Difficulty: Medium. Execution sequence: 390. Description sections: 21.

Preconditions/data: Text scribe form with no transcript and insufficient structured content

1. Attempt generate
2. Inspect feedback

Acceptance criteria:

- C1: Input requirement is explained or output explicitly reflects only available chart data
- C2: No fictitious conversation is invented

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-391 — Clinical approval cannot be granted by front desk

Difficulty: Hard. Execution sequence: 391. Description sections: 21.

Preconditions/data: frontdesk.demo; AI apply/sign URL observed as physician

1. Open recorded AI application/signing page
2. Attempt exposed action

Acceptance criteria:

- C1: Front desk cannot approve/sign physician documentation
- C2: Unsigned and signed notes remain unchanged

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-392 — AI draft fact audit using fixed transcript

Difficulty: Expert. Execution sequence: 392. Description sections: 21.

Preconditions/data: A chart explicitly has penicillin allergy; transcript says headache two days and no vitals supplied

1. Generate draft from fixed transcript
2. Compare every asserted symptom measurement medication and plan to sources

Acceptance criteria:

- C1: Headache duration and known allergy are accurate
- C2: No unprovided fever normal exam or treatment is asserted as completed fact
- C3: Any proposals are marked suggestions

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

## Clinical inbox and tasks (10)

### AF3-393 — Shared inbox categories and task context

Difficulty: Easy. Execution sequence: 393. Description sections: 22, 26.

Preconditions/data: Tasks from results notes orders renewals messages authorizations documentation and billing fixtures

1. Open shared inbox
2. Inspect representative rows

Acceptance criteria:

- C1: Categories are distinguishable
- C2: Assigned user patient related record priority status creation time and due date are available

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-394 — Assign unassigned task

Difficulty: Medium. Execution sequence: 394. Description sections: 22, 26.

Preconditions/data: Unassigned task; authorized assigner

1. Assign to permitted staff A
2. Save
3. Open A inbox

Acceptance criteria:

- C1: Task appears for A
- C2: Assignment persists

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-395 — Reassign task

Difficulty: Medium. Execution sequence: 395. Description sections: 22, 26.

Preconditions/data: Task assigned to A; authorized assigner; staff B eligible

1. Reassign to B
2. Open both inboxes

Acceptance criteria:

- C1: B sees assignment
- C2: A is no longer incorrectly shown as sole active assignee

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-396 — Complete task

Difficulty: Medium. Execution sequence: 396. Description sections: 22, 26.

Preconditions/data: Open assigned task with prerequisites satisfied

1. Mark Complete
2. Reload inbox and task detail

Acceptance criteria:

- C1: Completed status persists
- C2: Active task queue reflects completion

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-397 — Task priority edit

Difficulty: Medium. Execution sequence: 397. Description sections: 22, 26.

Preconditions/data: Editable task with normal priority

1. Change to supported high priority
2. Save
3. Filter high priority

Acceptance criteria:

- C1: Priority persists
- C2: Task is discoverable under correct filter

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-398 — Task status and category filters

Difficulty: Medium. Execution sequence: 398. Description sections: 22, 26.

Preconditions/data: Mixed open/completed tasks from two categories

1. Filter open results tasks
2. Inspect list
3. Clear category

Acceptance criteria:

- C1: Results follow active status/category
- C2: Clearing category retains status filter

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-399 — Task search by patient/context

Difficulty: Medium. Execution sequence: 399. Description sections: 22, 26.

Preconditions/data: Two tasks for different patients and related records

1. Search A name/MRN or supported task text
2. Open result

Acceptance criteria:

- C1: Matching task points to correct patient and record
- C2: Search does not silently select B

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-400 — Task link preserves patient context

Difficulty: Hard. Execution sequence: 400. Description sections: 22, 26.

Preconditions/data: Result-review task for A result R

1. Open task
2. Follow related record
3. Return to inbox

Acceptance criteria:

- C1: Linked result is R for A
- C2: Completion does not change unrelated task

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-401 — Unauthorized task modification denied

Difficulty: Hard. Execution sequence: 401. Description sections: 22, 26.

Preconditions/data: User outside documented task management scope; task URL observed by authorized staff

1. Open task edit/assignment page
2. Attempt exposed change

Acceptance criteria:

- C1: Out-of-scope assignment/completion is denied
- C2: Original task remains unchanged

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-402 — Completed task updates dashboard count

Difficulty: Hard. Execution sequence: 402. Description sections: 22, 26.

Preconditions/data: Known active task count N and one independently completable task

1. Complete task
2. Reload dashboard

Acceptance criteria:

- C1: Active count decreases by one within same scope
- C2: Completed task is not still counted as pending

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

## Analytics cohorts filters and CSV parity (24)

### AF3-403 — Physician dashboard real queue counts

Difficulty: Medium. Execution sequence: 403. Description sections: 6, 23.

Preconditions/data: Assigned physician; UI-countable visits unsigned notes pending orders and results

1. Open dashboard
2. Follow each corresponding queue and compare same-scope counts

Acceptance criteria:

- C1: Counts reconcile with records in their stated scope
- C2: No static unrelated totals are displayed

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-404 — Front desk dashboard operations

Difficulty: Medium. Execution sequence: 404. Description sections: 6, 23.

Preconditions/data: Known arriving checked-in cancelled and unverified appointments

1. Open front desk dashboard
2. Follow relevant worklists

Acceptance criteria:

- C1: Cards reflect current operational records
- C2: Patient status labels match schedule/check-in

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-405 — Billing dashboard balances and queues

Difficulty: Medium. Execution sequence: 405. Description sections: 6, 23.

Preconditions/data: Known unbilled rejected denied and outstanding claim records

1. Open billing dashboard
2. Compare filtered workqueues

Acceptance criteria:

- C1: Counts and balances match stated scope
- C2: Queue navigation is correct

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-406 — Admin dashboard operational totals

Difficulty: Medium. Execution sequence: 406. Description sections: 6, 23.

Preconditions/data: Known active patients and daily visits; selected date

1. Open admin dashboard
2. Follow source lists

Acceptance criteria:

- C1: Active-patient and daily-visit figures reconcile with matching UI lists
- C2: Selected day is clear

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-407 — Report date range and active filters visible

Difficulty: Medium. Execution sequence: 407. Description sections: 6, 23.

Preconditions/data: Report with selectable period provider and department

1. Set date range provider A department A
2. Apply

Acceptance criteria:

- C1: Page clearly shows selected period and filters
- C2: No stale previous scope label remains

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-408 — Appointment cohort uses scheduled dates

Difficulty: Medium. Execution sequence: 408. Description sections: 6, 23.

Preconditions/data: Fixture appointments created earlier but scheduled inside/outside selected period

1. Filter period
2. Inspect appointment metrics and source list

Acceptance criteria:

- C1: In-period scheduled visits are included
- C2: Out-of-period scheduled visits are excluded regardless of creation date

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-409 — Encounter cohort uses encounter creation dates

Difficulty: Hard. Execution sequence: 409. Description sections: 6, 23.

Preconditions/data: Encounters with creation dates inside/outside selected period and distinct appointment dates

1. Filter period
2. Inspect encounter count and linked rows

Acceptance criteria:

- C1: Encounter inclusion follows creation date
- C2: Appointment date does not silently substitute

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-410 — Submitted claim from older encounter included

Difficulty: Expert. Execution sequence: 410. Description sections: 6, 23.

Preconditions/data: Encounter created before range; claim latest submitted_at inside range

1. Filter range
2. Inspect claims-submitted metric and source record

Acceptance criteria:

- C1: Claim is included in submitted cohort despite old encounter
- C2: Displayed date basis names latest submission date

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-411 — Latest resubmission determines submitted cohort

Difficulty: Expert. Execution sequence: 411. Description sections: 6, 23.

Preconditions/data: Claim submitted in range then latest resubmission outside range; immutable fixture dates

1. Filter original range
2. Inspect submitted cohort
3. Filter latest range

Acceptance criteria:

- C1: Claim follows latest submitted_at
- C2: It is not counted as currently submitted in both ranges using historical first date

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-412 — Acceptance uses current submitted-cohort state

Difficulty: Hard. Execution sequence: 412. Description sections: 6, 23.

Preconditions/data: Two claims submitted in period; one currently Accepted and one Rejected

1. Filter period
2. Inspect acceptance metric and cohort rows

Acceptance criteria:

- C1: Acceptance numerator reflects current accepted state of selected submitted cohort
- C2: Denominator follows displayed submitted cohort definition

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-413 — Payment metrics use posting dates

Difficulty: Hard. Execution sequence: 413. Description sections: 6, 23.

Preconditions/data: Older encounter with payment posted inside range; second payment outside range

1. Filter period
2. Compare payment list and metric

Acceptance criteria:

- C1: In-range posting is included regardless of encounter creation
- C2: Out-of-range posting is excluded

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-414 — Provider-filtered unlinked check-in copay

Difficulty: Expert. Execution sequence: 414. Description sections: 6, 23.

Preconditions/data: Appointment provider A with unlinked copay 25; provider B copay 40; same posting period

1. Filter financial report to A
2. Inspect payment total and CSV

Acceptance criteria:

- C1: A unlinked copay contributes 25
- C2: B copay is excluded
- C3: Appointment provider supplies scope for unlinked copay

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-415 — Linked copay counted exactly once

Difficulty: Expert. Execution sequence: 415. Description sections: 6, 23.

Preconditions/data: 25 copay initially unlinked then linked to claim via supported workflow; other payments total 100

1. Open payment/revenue report before and after linkage within same period

Acceptance criteria:

- C1: Total remains 125
- C2: Linking does not duplicate copay revenue

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-416 — Department filter independently scopes payments

Difficulty: Hard. Execution sequence: 416. Description sections: 6, 23.

Preconditions/data: Payments on encounters/appointments in two departments

1. Filter department A only
2. Inspect payment rows/total

Acceptance criteria:

- C1: Only department A payments are counted
- C2: Unlinked appointment copays use appointment department where defined

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-417 — Provider and department intersection

Difficulty: Hard. Execution sequence: 417. Description sections: 6, 23.

Preconditions/data: Provider A with visits in departments X/Y; provider B in X

1. Filter provider A and department X

Acceptance criteria:

- C1: Only intersection records contribute in each applicable cohort
- C2: Neither filter silently overrides the other

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-418 — Current charge balance denial cohort

Difficulty: Hard. Execution sequence: 418. Description sections: 6, 23.

Preconditions/data: Encounter creation dates inside/outside range; current charge/balance/denial fixtures

1. Filter period
2. Inspect current financial cohort metrics

Acceptance criteria:

- C1: These metrics follow encounter-creation cohort
- C2: Current values are not mislabeled as historical as-of values

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-419 — Zero encounter-cohort balance is not practice zero

Difficulty: Expert. Execution sequence: 419. Description sections: 6, 23.

Preconditions/data: No outstanding balance in selected encounter cohort but older practice claim remains unpaid

1. Filter selected period
2. Inspect A/R explanation and total

Acceptance criteria:

- C1: Cohort zero is explained as scoped current balance
- C2: UI does not assert practice-wide receivables are zero

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-420 — A/R aging uses documented current balance basis

Difficulty: Hard. Execution sequence: 420. Description sections: 6, 23.

Preconditions/data: Outstanding claims with documented aging dates and amounts

1. Open aging table
2. Compare each bucket to source claim ages and balances

Acceptance criteria:

- C1: Bucket sums equal current scoped receivable balance
- C2: Date basis is visible and consistent

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-421 — No-show rate denominator explicit and reproducible

Difficulty: Hard. Execution sequence: 421. Description sections: 6, 23.

Preconditions/data: Selected schedule cohort with known no-shows and total eligible visits

1. Inspect no-show rate and source rows

Acceptance criteria:

- C1: Numerator denominator and exclusions follow visible/documented definition
- C2: Computed percentage matches records

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-422 — Encounter completion and unsigned metrics

Difficulty: Hard. Execution sequence: 422. Description sections: 6, 23.

Preconditions/data: Selected encounter cohort with completed signed and unsigned notes

1. Open clinical report
2. Compare linked records

Acceptance criteria:

- C1: Completion and unsigned counts reconcile with cohort
- C2: Signed/closed documents are not counted as unsigned

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-423 — Empty cohort metrics

Difficulty: Medium. Execution sequence: 423. Description sections: 6, 23.

Preconditions/data: Date/provider combination with zero eligible records

1. Apply filters
2. Inspect metrics and charts

Acceptance criteria:

- C1: Counts and money are zero where appropriate
- C2: Rates use explicit zero/no-data handling without NaN infinity or fabricated percentage

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-424 — CSV matches filtered page

Difficulty: Expert. Execution sequence: 424. Description sections: 6, 23.

Preconditions/data: Selected period provider A department X; nonzero mixed metrics

1. Download CSV through visible Export
2. Open downloaded file in browser/system viewer
3. Compare values

Acceptance criteria:

- C1: CSV matches page scope and values
- C2: Date-basis column and selected provider/department are explicit

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-425 — Financial trend formatting

Difficulty: Medium. Execution sequence: 425. Description sections: 6, 23.

Preconditions/data: Report with amount 1234.50 and aging buckets

1. Inspect summary chart labels tooltips where present and table

Acceptance criteria:

- C1: Money consistently uses currency symbol thousands separators and two decimals
- C2: Labels do not drop cents or misstate unit

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-426 — Invalid or reversed report dates recover safely

Difficulty: Hard. Execution sequence: 426. Description sections: 6, 23.

Preconditions/data: Report date controls; start after end

1. Submit reversed range
2. Correct dates
3. Apply

Acceptance criteria:

- C1: Invalid interval yields clear validation or explicitly documented normalization
- C2: No misleading unlabeled scope is rendered

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

## Read-only interoperability through browser (10)

### AF3-427 — Patient JSON mapping

Difficulty: Medium. Execution sequence: 427. Description sections: 24, 32.

Preconditions/data: Documented UI/help link to selected synthetic Patient endpoint; authorized staff

1. Navigate to endpoint using browser address bar
2. Compare displayed JSON with chart

Acceptance criteria:

- C1: Patient identifier/name/birth date match documented mapping
- C2: Output is labeled inspired/demo rather than formally certified FHIR

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-428 — Appointment JSON mapping

Difficulty: Medium. Execution sequence: 428. Description sections: 24, 32.

Preconditions/data: Documented Appointment resource URL for known appointment

1. Open resource in browser
2. Compare patient provider time and status to schedule

Acceptance criteria:

- C1: Mapped fields correspond to selected appointment
- C2: Patient reference is correct

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-429 — Encounter JSON mapping

Difficulty: Medium. Execution sequence: 429. Description sections: 24, 32.

Preconditions/data: Documented Encounter resource for known encounter

1. Open browser JSON view
2. Compare patient and lifecycle state

Acceptance criteria:

- C1: Resource identity patient and mapped status agree with encounter
- C2: Appointment/document states are not conflated

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-430 — Condition JSON mapping

Difficulty: Medium. Execution sequence: 430. Description sections: 24, 32.

Preconditions/data: Documented Condition endpoint for known diagnosis

1. Open resource
2. Compare code label status and subject to chart

Acceptance criteria:

- C1: Curated diagnosis fields and subject reference match documented mapping

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-431 — Observation JSON units

Difficulty: Medium. Execution sequence: 431. Description sections: 24, 32.

Preconditions/data: Known saved height 65in equivalent canonical metric observation; documented Observation endpoint

1. Open resource
2. Compare quantity/unit with documented export mapping and UI

Acceptance criteria:

- C1: Value and unit represent same measurement
- C2: Imperial display is not incorrectly labeled metric in export

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-432 — MedicationRequest JSON mapping

Difficulty: Medium. Execution sequence: 432. Description sections: 24, 32.

Preconditions/data: Known simulated prescription; documented resource endpoint

1. Open resource
2. Compare medication dose subject and status

Acceptance criteria:

- C1: Mapped prescription details agree
- C2: Unsigned draft is not exported as a signed real pharmacy transmission

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-433 — ServiceRequest JSON mapping

Difficulty: Medium. Execution sequence: 433. Description sections: 24, 32.

Preconditions/data: Known lab order with diagnosis; documented endpoint

1. Open resource
2. Compare service subject encounter and status

Acceptance criteria:

- C1: Order data and references match documented mapping
- C2: Cancelled order is not represented as active without mapping explanation

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-434 — DiagnosticReport JSON mapping

Difficulty: Medium. Execution sequence: 434. Description sections: 24, 32.

Preconditions/data: Known published result; documented endpoint

1. Open resource
2. Compare test values/links status and patient

Acceptance criteria:

- C1: Result references and patient agree with source
- C2: JSON does not fabricate diagnostic interpretations

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-435 — Coverage JSON mapping

Difficulty: Medium. Execution sequence: 435. Description sections: 24, 32.

Preconditions/data: Known policy; documented endpoint

1. Open resource
2. Compare payer member status and subject

Acceptance criteria:

- C1: Export matches policy and documented mapping
- C2: Another patient's member ID does not appear

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-436 — Resource access control and read-only surface

Difficulty: Hard. Execution sequence: 436. Description sections: 24, 32.

Preconditions/data: Documented endpoint URLs; authorized staff and patient A; B resource known

1. View permitted resource
2. Sign out and reopen
3. Sign in as A and open B resource
4. Inspect any rendered mutation controls

Acceptance criteria:

- C1: Protected resource scope is enforced
- C2: No public mutation UI is offered
- C3: Browser GET alone does not prove PUT/POST/DELETE rejection; protocol-level checks remain excluded

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

## Administration and safe demo management (12)

### AF3-437 — Create synthetic staff account

Difficulty: Medium. Execution sequence: 437. Description sections: 5.1, 27, 28, 29.

Preconditions/data: Admin; unused test username and permitted role

1. Create account with public-demo-only test credentials
2. Sign in as new account

Acceptance criteria:

- C1: Account creation persists
- C2: Assigned role governs accessible workflow

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-438 — Change staff role and verify session permissions

Difficulty: Medium. Execution sequence: 438. Description sections: 5.1, 27, 28, 29.

Preconditions/data: Test staff account initially front desk; admin

1. Change account to permitted nurse role
2. Sign out/in test user
3. Open worklist and old restricted area

Acceptance criteria:

- C1: New role is effective
- C2: Permissions reflect new role rather than stale front desk access

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-439 — Deactivate test staff account

Difficulty: Medium. Execution sequence: 439. Description sections: 5.1, 27, 28, 29.

Preconditions/data: Synthetic test staff account; admin

1. Disable account through supported UI
2. Attempt fresh login as that account

Acceptance criteria:

- C1: Disabled account cannot authenticate
- C2: Other demo users still work

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-440 — Manage department

Difficulty: Medium. Execution sequence: 440. Description sections: 5.1, 27, 28, 29.

Preconditions/data: Admin; unused fictional department name

1. Create/edit test department
2. Save
3. Open applicable department selector

Acceptance criteria:

- C1: Department configuration persists
- C2: Selector shows current label

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-441 — Manage provider assignment

Difficulty: Medium. Execution sequence: 441. Description sections: 5.1, 27, 28, 29.

Preconditions/data: Admin; test provider and department

1. Assign provider to department
2. Save
3. Open scheduling selector

Acceptance criteria:

- C1: Provider department relationship appears correctly
- C2: Existing appointments are not reassigned silently

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-442 — Configure appointment type

Difficulty: Medium. Execution sequence: 442. Description sections: 5.1, 27, 28, 29.

Preconditions/data: Admin; test visit type

1. Set name and default duration 20 minutes
2. Save
3. Reopen configuration

Acceptance criteria:

- C1: Type settings persist
- C2: Duration field remains readable and valid

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-443 — Practice settings persist

Difficulty: Medium. Execution sequence: 443. Description sections: 5.1, 27, 28, 29.

Preconditions/data: Admin; non-sensitive fictional practice display setting

1. Edit supported practice display field
2. Save
3. Reload header/settings

Acceptance criteria:

- C1: Changed setting persists where applicable
- C2: No unrelated practice identity is substituted

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-444 — Demo account documentation covers all roles

Difficulty: Medium. Execution sequence: 444. Description sections: 5.1, 27, 28, 29.

Preconditions/data: Repository README accessible in browser or supplied local rendered document

1. Inspect documented nine demo usernames and role descriptions
2. Compare with sign-in entry points

Acceptance criteria:

- C1: All required roles have usable documented public demo account identities
- C2: No production credentials are needed

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-445 — Reset warning and cancel path

Difficulty: Medium. Execution sequence: 445. Description sections: 5.1, 27, 28, 29.

Preconditions/data: Admin on designated synthetic demo instance; evidence checkpoint saved

1. Open reset page
2. Read warning
3. Cancel without confirming
4. Reload patient count

Acceptance criteria:

- C1: Warning identifies destructive demo reset and requires explicit confirmation
- C2: Cancellation preserves current data

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-446 — Non-admin reset denied

Difficulty: Hard. Execution sequence: 446. Description sections: 5.1, 27, 28, 29.

Preconditions/data: frontdesk.demo; observed reset page URL

1. Navigate to reset page
2. Attempt exposed reset action

Acceptance criteria:

- C1: Reset is denied
- C2: Existing synthetic records remain unchanged

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-447 — Confirmed reset restores consistent demo state

Difficulty: Expert. Execution sequence: 472. Description sections: 5.1, 27, 28, 29.

Preconditions/data: Isolated designated demo database only; baseline captured; evidence exported; run last

1. Create one disposable marker through UI
2. Confirm reset as admin
3. Sign in and inspect baseline patients appointments claims and demo accounts

Acceptance criteria:

- C1: Marker is removed
- C2: Consistent baseline and role logins are restored
- C3: Reset event is recorded or retained as documented
- C4: Only designated demo database is affected

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-448 — Manager operational settings boundaries

Difficulty: Hard. Execution sequence: 447. Description sections: 5.1, 27, 28, 29.

Preconditions/data: manager.demo; authorized operational settings and admin role-management URL known

1. Edit one permitted operational setting
2. Open admin-only role management

Acceptance criteria:

- C1: Allowed operational setting saves
- C2: Manager cannot grant arbitrary staff privileges

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

## Audit trails and readable activity (10)

### AF3-449 — Registration audit event

Difficulty: Medium. Execution sequence: 448. Description sections: 26, 31, 32.

Preconditions/data: Newly registered synthetic patient with unique marker

1. Open audit search as authorized user
2. Locate registration by patient marker

Acceptance criteria:

- C1: Event identifies creation patient actor and timestamp
- C2: No unrelated patient is attributed

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-450 — Demographic edit audit event

Difficulty: Medium. Execution sequence: 449. Description sections: 26, 31, 32.

Preconditions/data: Patient phone changed through UI

1. Open audit/history
2. Locate edit

Acceptance criteria:

- C1: Event records edit actor/time and relevant change context
- C2: Patient association is correct

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-451 — State transition human-readable

Difficulty: Medium. Execution sequence: 450. Description sections: 26, 31, 32.

Preconditions/data: Appointment Confirmed to Arrived transition

1. Open activity history

Acceptance criteria:

- C1: Business label and prior/new states with arrow or equally clear transition rendering are readable
- C2: Actor and timestamp persist
- C3: No raw dictionary is shown

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-452 — Eligibility history human-readable

Difficulty: Medium. Execution sequence: 451. Description sections: 26, 31, 32.

Preconditions/data: Policy with Active verification event

1. Open coverage activity history

Acceptance criteria:

- C1: Coverage status actor/time are readable
- C2: Structured eligibility object is not dumped as JSON

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-453 — Financial audit for responsibility confirmation

Difficulty: Medium. Execution sequence: 452. Description sections: 26, 31, 32.

Preconditions/data: Billing staff confirmed 75.00 responsibility

1. Open claim audit/history

Acceptance criteria:

- C1: Confirmation amount actor and time are recorded
- C2: Confirmation is distinguishable from payment posting

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-454 — Signed-note audit traceability

Difficulty: Medium. Execution sequence: 453. Description sections: 26, 31, 32.

Preconditions/data: Note signed with recorded clinician/time/version

1. Open audit event and note

Acceptance criteria:

- C1: Event correlates with signed note clinician and version
- C2: Signing event is not confused with draft save

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-455 — Audit filtering by actor and action

Difficulty: Medium. Execution sequence: 454. Description sections: 26, 31, 32.

Preconditions/data: At least two actors and creation/update events

1. Filter actor A and update action
2. Inspect results
3. Clear action filter

Acceptance criteria:

- C1: Rows obey both filters
- C2: Clearing action retains actor scope

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-456 — Audit access denied to patient

Difficulty: Hard. Execution sequence: 455. Description sections: 26, 31, 32.

Preconditions/data: Patient session; audit page URL observed as admin

1. Navigate to audit page

Acceptance criteria:

- C1: Staff audit events and other-patient metadata are withheld
- C2: No unauthorized export control works

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-457 — Rendered special-character activity values

Difficulty: Medium. Execution sequence: 456. Description sections: 26, 31, 32.

Preconditions/data: Synthetic patient preferred name contains literal <b>AF_TEST</b> entered as plain text

1. Save permitted field
2. Inspect activity/history

Acceptance criteria:

- C1: Value is safely rendered as text rather than executable markup
- C2: History remains readable without template failure

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-458 — No raw containers in ordinary histories

Difficulty: Medium. Execution sequence: 457. Description sections: 26, 31, 32.

Preconditions/data: Representative check-in eligibility claim validation and encounter events

1. Open each ordinary history/validation list

Acceptance criteria:

- C1: Business statements replace Python dictionaries JSON objects and empty arrays
- C2: Actor/time and useful meaning are retained

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

## Integrated multi-role workflows (14)

### AF3-459 — New patient to completed clinical visit

Difficulty: Expert. Execution sequence: 458. Description sections: 26, 36.

Preconditions/data: Fresh synthetic patient identity; free slot; front desk nurse assigned physician

1. Register
2. Schedule
3. Arrive and check in
4. Record intake and room
5. Start as physician
6. Add diagnosis and SOAP
7. Sign and close

Acceptance criteria:

- C1: Same patient/appointment/encounter lineage persists across roles
- C2: Vitals and note survive session changes
- C3: Final visit states and audit trail are coherent

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-460 — Clinical order to patient-visible result

Difficulty: Expert. Execution sequence: 459. Description sections: 26, 36.

Preconditions/data: A open encounter; lab service; processing role; patient account linked

1. Create and sign order
2. Collect/process specimen
3. Enter and publish result
4. Review and release
5. Open patient portal

Acceptance criteria:

- C1: Same order/result lineage is preserved
- C2: Portal shows released value only after release
- C3: Review and release states are distinct

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-461 — Encounter to settled claim

Difficulty: Expert. Execution sequence: 460. Description sections: 26, 36.

Preconditions/data: Completed signed encounter; coder billing roles; valid insurance

1. Create/approve charges
2. Generate validate submit claim
3. Run accepted/adjudicated simulation
4. Post full allowed payment
5. Close

Acceptance criteria:

- C1: Charges claim total payments and zero balance reconcile
- C2: Clinical note remains signed and unmodified

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-462 — Denial correction to acceptance

Difficulty: Expert. Execution sequence: 461. Description sections: 26, 36.

Preconditions/data: Claim with deterministic correctable denial scenario

1. Submit
2. Simulate denial
3. Investigate and correct
4. Revalidate and resubmit
5. Run accepted response

Acceptance criteria:

- C1: Claim moves through correction path
- C2: Original denial and resubmission histories remain
- C3: No duplicate active charge is created

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-463 — Authorization-required service to valid claim

Difficulty: Expert. Execution sequence: 462. Description sections: 26, 36.

Preconditions/data: Service requiring authorization; patient policy; pending service order

1. Create authorization
2. Submit and approve
3. Link matching service
4. Create/revalidate claim

Acceptance criteria:

- C1: Approved unexpired matching authorization clears appropriate claim gate
- C2: Wrong-patient/service context never appears

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-464 — Portal message through staff resolution

Difficulty: Expert. Execution sequence: 463. Description sections: 26, 36.

Preconditions/data: Patient A and authorized nurse/physician sessions

1. Patient sends message
2. Staff observes unread
3. Staff replies
4. Patient reads
5. Inspect both read states

Acceptance criteria:

- C1: Conversation stays patient-scoped
- C2: Incoming counts update for respective readers
- C3: Reply does not count as sender's unread

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-465 — Renewal request through physician prescription

Difficulty: Expert. Execution sequence: 464. Description sections: 26, 36.

Preconditions/data: Patient active medication; renewal request workflow

1. Patient requests renewal
2. Staff finds task
3. Physician reviews and signs simulated prescription
4. Inspect portal medications/request

Acceptance criteria:

- C1: Request and prescription refer to correct medication/patient
- C2: Human signature gate is preserved
- C3: No real pharmacy transmission occurs

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-466 — Copay to claim linkage and report reconciliation

Difficulty: Expert. Execution sequence: 465. Description sections: 26, 36.

Preconditions/data: Appointment with 25 copay; resulting eligible 200 claim; report period includes payment

1. Check in and pay copay
2. Complete encounter and create claim
3. Link copay through supported UI
4. Inspect report and balance

Acceptance criteria:

- C1: Copay is allocated once
- C2: Claim balance reflects documented allocation rules
- C3: Report revenue counts 25 exactly once

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-467 — Adjudication to partial portal payment

Difficulty: Expert. Execution sequence: 466. Description sections: 26, 36.

Preconditions/data: Adjudicated claim balance 200; billing and linked patient sessions

1. Confirm responsibility 80
2. Patient pays 30
3. Open staff claim portal bills receipt and report

Acceptance criteria:

- C1: Claim balance 170 and responsibility 50 agree across views
- C2: Payment history has one 30 transaction
- C3: Report adds 30 once

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-468 — Unit conversion through AI and signed note

Difficulty: Expert. Execution sequence: 467. Description sections: 26, 36.

Preconditions/data: Nurse and physician; A encounter; height65.37in weight147.29lb plus complete vitals

1. Save intake
2. Toggle units and reload
3. Generate/apply AI draft
4. Review save and sign
5. Open chart and note

Acceptance criteria:

- C1: Measurements remain consistent across intake chart AI and signed note
- C2: No unit drift or automatic AI signing occurs

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-469 — Wrong-patient prevention across clinical workflow

Difficulty: Expert. Execution sequence: 468. Description sections: 26, 36.

Preconditions/data: Similar-name A/B with distinct MRN/DOB and different allergies

1. Select A by MRN
2. Create encounter diagnosis order and draft medication
3. Review B chart

Acceptance criteria:

- C1: All new records belong to A
- C2: B receives none of the mutations
- C3: A/B identities remain visible at selection points

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-470 — Persisted workflow after logout and new session

Difficulty: Expert. Execution sequence: 469. Description sections: 26, 36.

Preconditions/data: New appointment intake note order and payment records created through UI for one synthetic patient

1. Record IDs
2. Sign out all sessions
3. Sign back in appropriate roles
4. Reopen records

Acceptance criteria:

- C1: Each saved record remains with correct state and relationships
- C2: No action must be repeated to restore saved data

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-471 — Multi-cohort reporting with old encounter and new money

Difficulty: Expert. Execution sequence: 470. Description sections: 26, 36.

Preconditions/data: Old encounter; claim latest submitted in current period; payment posted in current period; no new encounter

1. Open current-period report
2. Export CSV
3. Compare source claim/payment and encounter cohort

Acceptance criteria:

- C1: Submitted/payment cohorts include their new activity
- C2: Encounter cohort may be zero without erasing financial activity
- C3: CSV and page explain different date bases

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

### AF3-472 — Post-evaluation role privacy regression

Difficulty: Expert. Execution sequence: 471. Description sections: 26, 36.

Preconditions/data: A/B with distinct new clinical and financial records; patient A login

1. Open own portal
2. Navigate recorded B chart result message bill and receipt URLs one at a time

Acceptance criteria:

- C1: Own authorized data remains usable
- C2: All five other-patient surfaces deny disclosure
- C3: No completed test grants lasting elevated patient privileges

Evidence: before state, decisive action/error, final state and criterion observations. Verify specified persistence and cross-role views.

