# Test report

## Executed local results

Execution date: **November 16, 2026 (America/Chicago)**.

| Suite | Created | Executed | Passed | Failed | Skipped | Pass rate |
|---|---:|---:|---:|---:|---:|---:|
| Django backend, permissions and integration | 78 | 78 | 78 | 0 | 0 | 100% |
| Playwright Chromium browser | 8 | 8 | 8 | 0 | 0 | 100% |
| **Total** | **86** | **86** | **86** | **0** | **0** | **100%** |

Pass rate = Passed / Executed × 100%. Final combined run: **86 tests in 27.309 seconds**, exit code 0. This count is test methods; parameterized subtests and assertions are not inflated into additional tests. The unedited combined command output is retained in `docs/test-output.txt`.

Environment:

- Windows host, PowerShell
- Python 3.14.9
- Django 5.2.19
- SQLite test database, isolated in-memory Django live-server database for browser tests
- Playwright 1.65.2
- Chrome for Testing 159.0.8154.6, Playwright Chromium build v1255
- Desktop viewport 1536 × 1100; responsive test viewport 390 × 844
- Django timezone America/Chicago

The first browser invocation stalled under the restricted process sandbox and was interrupted. Chromium was then run with the required process permission. The reported final suite completed in that environment. No interrupted attempt is counted as a pass.

## Additional checks actually run

| Check | Result |
|---|---|
| `manage.py check` | Passed, no issues |
| `manage.py makemigrations --check --dry-run` | Passed, no changes detected |
| Python `compileall` for application/test modules | Passed |
| Migrate a new local SQLite database | Passed |
| `collectstatic --noinput` | Passed |
| `check --deploy --fail-level WARNING` using production environment settings | Passed, no warnings; did not connect to PostgreSQL |
| Render Blueprint against downloaded current JSON schema | Passed; structural validation only, no cloud apply |
| Confirmed local `seed_demo --reset` | Passed; rebuilt fixture and reset event |
| Screenshot inspection | Dashboard and encounter workspace inspected; browser captures saved for seven representative views |

## Coverage

Backend tests cover authentication for all nine required accounts; invalid login; POST logout; CSRF; all admin lists/detail/create forms; role dashboards; role and patient restrictions; physician scope; message isolation; scoped foreign-key choices; future DOB and duplicate registration; directory search/pagination; appointment overlaps, adjacency, cancellation reuse, availability and department consistency; check-in rollback, copay handoff and replay protection; intake/BMI/ranges; note version conflicts, reconciliation, acknowledgments, immutable signed notes, addenda and placeholders; deterministic AI approval and escaped transcript text; order/task/result/release workflows; medication warnings; complete paid and partially paid claim flows; missing insurance/authorization and revalidation; duplicate claims; denial correction; payment amount and ownership constraints, DB positivity and replay protection; portal tasks/messages/renewals; reports/CSV and changing data; audit transitions; all nine FHIR-inspired exports; health; waitlist booking; authorization transitions; booking patient requests; task completion; administrator self-lockout prevention; locked charges and signed coding protection; longitudinal problem resolution; and fixture consistency.

Browser tests use visible controls to exercise:

1. Login, navigation and representative screen captures.
2. Patient search, pagination and chart tabs.
3. A complete new-patient journey through insurance, appointment booking, check-in, nurse intake, physician documentation/signing, coding, claim validation and payment settlement.
4. AI text draft generation, explicit approval and note preview.
5. Denial appeal/correction and a simulated payment receipt.
6. Patient portal request, persistent message thread and a denied staff-only route.
7. Narrow-screen navigation and horizontal-overflow check.
8. Invalid form handling that preserves entered values.

All browser cases assert no page-level JavaScript errors. Screenshots are supporting evidence, not substitutes for persistence assertions.

## Failures found and corrected during development

- Initial syntax error in the summary view.
- Check-in timestamp missing during model validation.
- Claim creation reading stale encounter state after signing.
- New patient message form failing to select the owning patient by default.
- Sidebar task count using a broader scope than the visible workqueue.
- Claim edits validating empty JSON error lists as required content.

## Not run / not claimed

- PostgreSQL runtime and concurrent booking/payment stress tests were not run locally. The GitHub Actions matrix is configured for PostgreSQL and SQLite; consult the actual remote run before claiming those passed.
- Render platform-aware validation, paid cloud provisioning and deployed smoke tests were not performed.
- Genuine Computer Use Agent evaluation, independent accessibility audit, load testing, penetration testing and medical/regulatory validation were not performed.

These are distinct unexecuted evaluation tracks, not skipped passing tests in the 86-test suite.

## Reproduce

```bash
pip install -r requirements-dev.txt
python -m playwright install chromium
python manage.py test tests --verbosity 2
```

Use `python manage.py test tests.test_workflows` or `tests.test_browser` to select a suite. Set `PLAYWRIGHT_BROWSERS_PATH` only if using a non-default browser installation. Set `CAPTURE_SCREENSHOTS=1` to regenerate screenshot artifacts. Do not run tests against the user's working demo database; Django creates and destroys its own test database.
