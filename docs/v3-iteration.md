# V3 implementation and validation record

## Specification and version history

[Description V3](../description_v3.md) is the complete, standalone English specification, retaining all 39 original product sections and integrating this iteration's requirements into the relevant sections. [Description V1](../description_v1.md), [Description V2](../description_v2.md), and the original brief remain unchanged. V2 is preserved at commit `22a4781ef65d9583a73a0f2d0717f0f459560988` in the same [repository](https://github.com/KateK77/athenaone-clone).

The full enterprise specification remains broader than the research implementation. The inherited gaps in [limitations](limitations.md) are still tracked; this release does not claim to implement the entire commercial product.

## Feedback coverage

| Area | V3 behavior | Evidence |
|---|---|---|
| Readability and borders | 16px body and form text, 14px supporting text, 20–32px headings, visible input/button outlines, 44–48px action targets; applied to sign-in, clinical, financial and portal screens | Desktop/mobile screenshots; computed font and control size checks |
| Patient selection | Persistent wrapping selected identity displays full name, MRN and DOB while preserving authorized native select behavior | Search/selection browser checks at 1280px and 390px |
| Measurements | At most two visible decimals; eight-decimal metric storage; exact conversion factors; round trips preserve the canonical value; stale or inconsistent hidden values cannot override edited input | Backend bounds/metadata/save-reload cases; five browser unit round trips with 70in/150lb |
| Schedule | Date/filter changes update the schedule directly; previous/next retain filters; responsive populated groups replace the wide empty canvas; empty groups remain available | Date synchronization and appointment visibility checks; desktop/mobile screenshots |
| Portal | Prominent shortcuts, medication-adjacent renewal actions, compact contact editing, clear section labels and adequate form/action spacing | Portal request/message regression; contact save/reload; 390px layout |
| AI documentation | Explicit “Apply to unsigned draft” action and unsigned success message; generated objectives label all recorded vital units; no retrospective note rewrite | Application remains unsigned; recorded facts/units assertions |
| Claim workflow | Current stage, explanation and authorized next action at the top; denial detail/edit return directly to the related claim; full-width amount field | State/role workflow regression; denial navigation checks |
| Payment completion | Receipt shows current remaining balance, links to claim/history for finance staff or portal bills for patients, and print action; restored forms return to a fresh balance | Payment replay and browser-back checks; patient receipt scope test |
| Reports | Submission cohort uses `submitted_at`; payment provider/department filters include older claims and unlinked check-in copays; visible date basis per metric | Older-encounter submission regression; filtered payment check; CSV parity |
| Existing behavior | Registration, scheduling, intake, notes, orders/results, messages, prescribing, billing and ownership restrictions remain in the suite | Full regression suite |

## Validation

- Full local suite: **129 passed, 0 failed, 0 skipped**; 112 backend/integration cases and 17 Chromium browser cases. See [raw output](v3-test-output.txt) and [machine-readable results](v3-validation.json).
- Django system checks and migration drift check: PASS.
- Local HTTP health: 200, application `AthenaFlow`, simulated external transactions.
- Additional read-only checks against the running demonstration: 8 pages × 4 widths (1536, 1280, 768, 390px), no horizontal document overflow and no JavaScript errors.
- Existing acceptance data: on Nov 25, submissions now show **1**, acceptance **100.0%**, payments remain **$151.00**. CLM-00130 remains at **$53.00**; CLM-00081 is Paid, CLM-00161 Closed, ENC-0202 Documentation Pending, and the synthetic discontinued prescription remains in history.
- The GitHub workflow runs the same suite independently on SQLite and PostgreSQL 16. The exact pushed commit's status is recorded by [GitHub Actions](https://github.com/KateK77/athenaone-clone/actions), separately from local validation.
- Browser automation is Playwright, not a Computer Use Agent evaluation. No independent accessibility audit or load test was performed.

Screenshots: [sign-in](screenshots/v3-login.png), [portal](screenshots/v3-portal.png), [mobile portal](screenshots/v3-portal-mobile.png), [schedule](screenshots/v3-schedule.png), [mobile schedule](screenshots/v3-schedule-mobile.png), [intake](screenshots/v3-intake.png), [physician workspace](screenshots/v3-physician-workspace.png), [receipt](screenshots/v3-receipt.png), [report](screenshots/v3-report.png).

## Data migration and compatibility

`clinical.0005_preserve_measurement_precision` widens height and weight decimal storage without changing recorded values. Before migration, a SQLite backup was taken outside the repository. All **35 application tables and 1,936 rows** were compared by named column and primary key after migration; no values changed. SQLite may reorder columns during table rebuild, so ordinal-column hashes are not a valid comparison. No reset or reseed was performed. Local database files, backups and secrets are excluded from Git and source archives.

Previously rounded values cannot be recovered: the existing ENC-0202 weight remains the recorded 68kg. New 150lb entries retain 68.03885550kg internally and display 68.04kg when selected. Existing signed or unsigned notes are not silently regenerated to add units; newly generated drafts use the improved objective representation.

Without JavaScript, native selectors and Apply controls remain usable; automatic unit conversion, inline selection summaries and browser history restoration handling require JavaScript. Server-side unit/range validation, authorization and duplicate payment protection remain active.

## Reporting semantics and remaining boundaries

Submission metrics count claims by their **latest** submission timestamp; they do not count all historical submission attempts. Charges, current balance, denial rate and aging remain an explicitly labeled encounter-creation cohort. They are not a historical ledger or practice-wide receivables snapshot. CSV exports add Date basis, Provider and Department columns while retaining the original Metric, Value, Start and End columns. Consumers relying on an exact four-column schema must allow the new columns.

The calendar remains grouped appointment cards, not a time-proportional grid or a full availability engine. Portal renewal requests still create staff tasks; no real pharmacy transaction is sent. Clinical assistant, insurance and payments remain simulations. Public deployment was not changed by this local release.
