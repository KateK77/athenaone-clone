#!/usr/bin/env python3
"""Offline integrity/ledger validator. Never executes the application or awards CUA PASS."""
from pathlib import Path
import argparse,collections,hashlib,json,sys

def digest(b): return hashlib.sha256(b).hexdigest()
def canonical(v): return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def validate(root,results_path=None):
 errors=[]
 def check(ok,msg):
  if not ok: errors.append(msg)
 manifest=json.loads((root/'suite_manifest.json').read_text())
 for name,expected in manifest['files'].items():
  p=root/name
  check(p.is_file(),f'Missing frozen file: {name}')
  if p.is_file():check(digest(p.read_bytes())==expected,f'File hash mismatch: {name}')
 for line in (root/'SHA256SUMS').read_text().splitlines():
  checksum,name=line.split('  ',1);p=root/name
  check(p.is_file() and digest(p.read_bytes())==checksum,f'Checksum mismatch: {name}')
 suite=json.loads((root/'frozen/all_tests.json').read_text());ts=suite['tests']
 ids=[t['test_id'] for t in ts]
 check(len(ts)==472,'Expected 472 cases')
 check(ids==[f'AF3-{i:03d}' for i in range(1,473)],'IDs missing, duplicated, or reordered')
 check(len({t['title'] for t in ts})==472,'Duplicate case titles')
 check(digest('\n'.join(ids).encode())==manifest['ordered_ids_sha256'],'ID list hash mismatch')
 for t in ts:
  check(t['difficulty'] in ['Easy','Medium','Hard','Expert'],f'Unknown difficulty {t["test_id"]}')
  check(t['steps'] and t['preconditions'] and t['acceptance_criteria'],f'Empty definition {t["test_id"]}')
  check(all(x['action'].strip() for x in t['steps']),f'Empty action {t["test_id"]}')
  check(all(x['expected'].strip() for x in t['acceptance_criteria']),f'Empty criterion {t["test_id"]}')
  check(digest(canonical(t))==manifest['case_sha256'].get(t['test_id']),f'Case hash mismatch {t["test_id"]}')
 order=json.loads((root/'frozen/execution_order.json').read_text())
 check(len(order['order'])==472 and set(order['order'])==set(ids),'Execution order must contain all IDs exactly once')
 check(order['order'][:10]==order['pilot'],'Pilot mismatch')
 check(order['order'][-1]==order['final_test']=='AF3-447','Isolated reset must be last')
 check(dict(collections.Counter(t['difficulty'] for t in ts))==manifest['difficulty_counts'],'Difficulty counts mismatch')
 if results_path:
  rows=json.loads(results_path.read_text());byid={t['test_id']:t for t in ts}
  check(len(rows)==472 and len({r['test_id'] for r in rows})==472 and {r['test_id'] for r in rows}==set(ids),'Results must contain every frozen ID exactly once')
  for r in rows:
   tid=r['test_id'];status=r['status']
   if tid not in byid:
    errors.append(f'Unknown result ID {tid}');continue
   check(status in ['PASS','FAIL','BLOCKED','NOT_RUN'],f'Invalid result status {tid}')
   if status=='NOT_RUN':continue
   check(bool(r.get('reason_code')) and bool(r.get('observed_result')),f'Outcome explanation missing {tid}')
   check(r.get('attempt_number',0)>0 and r.get('started_at') and r.get('ended_at'),f'Attempt/time missing {tid}')
   checks=r.get('criteria_results',[])
   expected={x['criterion_id'] for x in byid[tid]['acceptance_criteria']}
   check({x['criterion_id'] for x in checks}==expected and len(checks)==len(expected),f'Criterion observations incomplete {tid}')
   check(all(x.get('verdict') in ['SATISFIED','VIOLATED','UNOBSERVED'] for x in checks),f'Bad criterion verdict {tid}')
   if status=='PASS':
    check(all(x.get('verdict')=='SATISFIED' and x.get('observation') and x.get('evidence_paths') for x in checks),f'PASS lacks satisfied evidence {tid}')
   if status=='FAIL':check(any(x.get('verdict')=='VIOLATED' for x in checks),f'FAIL lacks observed violation {tid}')
   if status=='BLOCKED':check(bool(r.get('reason')),f'BLOCKED lacks blocker {tid}')
   if status in ['PASS','FAIL']:
    check(bool(r.get('evidence')) and bool(r.get('action_log_path')),f'Missing evidence/action log {tid}')
   referenced=set()
   for e in r.get('evidence',[]):
    if e.get('path'):
     referenced.add(e['path'])
     ep=(root/e['path']).resolve()
     if ep.is_relative_to(root.resolve()) and ep.is_file():
      check(digest(ep.read_bytes())==e.get('sha256'),f'Evidence hash missing or incorrect {tid}: {e["path"]}')
   for c in checks:referenced.update(c.get('evidence_paths',[]))
   if r.get('action_log_path'):referenced.add(r['action_log_path'])
   for name in referenced:
    p=(root/name).resolve()
    check(p.is_relative_to(root.resolve()) and p.is_file(),f'Evidence file absent or outside package {tid}: {name}')
 if results_path:
  attempts=json.loads((root/'results/attempts.json').read_text())
  keys=[(a['test_id'],a.get('attempt_number')) for a in attempts]
  check(len(keys)==len(set(keys)),'Duplicate test/attempt IDs in history')
  latest={}
  for a in attempts:
   check(a['test_id'] in set(ids),'Unknown ID in attempt history')
   latest[a['test_id']]=a
  for r in rows:
   if r['status']!='NOT_RUN':
    a=latest.get(r['test_id'])
    check(a is not None and a.get('attempt_number')==r.get('attempt_number') and a.get('status')==r.get('status'),f'Current result missing matching latest attempt {r["test_id"]}')
 if errors:
  print(json.dumps({'valid':False,'errors':errors},indent=2));return 1
 print(json.dumps({'valid':True,'frozen_cases':472,'file_hashes_checked':len(manifest['files']),'results_checked':bool(results_path),'application_tests_executed_by_this_script':0},indent=2));return 0
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--results',type=Path)
 a=p.parse_args();sys.exit(validate(a.root.resolve(),a.results.resolve() if a.results else None))
