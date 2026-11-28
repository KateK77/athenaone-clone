# AthenaFlow V3 CUA evaluation — partial

Frozen suite: AthenaFlow-V3-Independent-CUA-472 v1.0.0. No case definitions or application code changed.

Source main: 2723877e8f52afe06c248ce21af5a5dcac4f059e. Running URL observed: http://127.0.0.1:18310/. Served SHA UNVERIFIED. Chrome screenshot-driven CUA,1440×900; browser version/model/reasoning/zoom UNKNOWN_UNEXPOSED.

Current outcome:6 PASS,0 FAIL,2 BLOCKED,464 NOT_RUN. Evaluated pass rate6/6=100%; execution coverage6/472=1.27%; suite success fraction6/472=1.27%. This is an incomplete pilot, not a completed472-case evaluation.

PASS: AF3-004,019,078,115,146,351. BLOCKED: AF3-039 (entered-MRN oracle conflicts with auto-generated MRN); AF3-261 (missing-diagnosis claim fixture unavailable through normal UI). AF3-376 interrupted during native Apply confirmation; AF3-314 not started.

Resume: inspect encounter203 and generated draft2 before repeating Apply. Do not repeat completed cases. See [checkpoint](results/checkpoint.json),[results](results/results.json),[attempts](results/attempts.json),[summary](reports/current/summary.md),[environment](results/environment.json),[evidence index](results/evidence_index.json),[partial pilot](reports/batch-001/batch_state.json).

Original screenshots are retained; action summaries are authored records, not native trace exports. Earlier interrupted sessions are retained. AF3-004 has an explicit append-only ledger reconciliation event which is not another execution. No paid API calls. No shared reset.

Evaluation branch remains unmerged: evaluation/athenaflow-v3-independent-cua-472. See [upload ledger](results/upload_ledger.json) for verified remote commits.
