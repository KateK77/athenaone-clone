#!/usr/bin/env python3
"""Calculate descriptive counts from recorded outcomes, never infer results."""
from pathlib import Path
import argparse,collections,csv,json
STATUSES=['PASS','FAIL','BLOCKED','NOT_RUN']
def stats(rows):
 c=collections.Counter(r['status'] for r in rows)
 if set(c)-set(STATUSES):raise ValueError('Invalid result status')
 n=len(rows);evaluated=c['PASS']+c['FAIL']
 return {'total':n,**{k:c[k] for k in STATUSES},'evaluated':evaluated,'evaluated_pass_rate':c['PASS']/evaluated if evaluated else None,'execution_coverage':evaluated/n if n else None,'suite_success_fraction':c['PASS']/n if n else None}
def summary(root,out):
 tests=json.loads((root/'frozen/all_tests.json').read_text())['tests'];rows=json.loads((root/'results/results.json').read_text());attempts=json.loads((root/'results/attempts.json').read_text())
 ids={t['test_id'] for t in tests};byid={r['test_id']:r for r in rows}
 if len(rows)!=472 or len(byid)!=472 or set(byid)!=ids:raise ValueError('Expected exactly all 472 result IDs')
 result={'suite_id':'AthenaFlow-V3-Independent-CUA-472','result_policy':'current_snapshot','overall':stats(rows),'by_difficulty':{},'by_module':{},'by_environment_segment':{},'attempts_recorded':len(attempts),'interrupted_attempts':sum(a.get('reason_code')=='INTERRUPTED' for a in attempts),'limitations':['Statistics reflect supplied ledgers, not independent verification of screenshots or execution.','UNVERIFIED commit/model fields must remain disclosed.']}
 for key in ['difficulty','module']:
  for value in dict.fromkeys(t[key] for t in tests):result['by_'+key][value]=stats([byid[t['test_id']] for t in tests if t[key]==value])
 for env in dict.fromkeys(str(r.get('environment_id') or 'UNBOUND') for r in rows):
  segment=[r for r in rows if str(r.get('environment_id') or 'UNBOUND')==env];result['by_environment_segment'][env]=stats(segment)
 first={}
 for a in attempts:
  if a['test_id'] not in ids:raise ValueError('Unknown attempt ID')
  if a.get('status') in ['PASS','FAIL','BLOCKED'] and a['test_id'] not in first:first[a['test_id']]=a
 first_rows=[first.get(t['test_id'],{'test_id':t['test_id'],'status':'NOT_RUN'}) for t in tests]
 result['first_final_outcome']=stats(first_rows)
 result['retry_disclosure']='First final outcome comes only from append-only attempts; interrupted NOT_RUN attempts are counted separately.'
 out.mkdir(parents=True,exist_ok=True)
 (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
 def rate(x):return 'N/A' if x is None else f'{x:.2%}'
 lines=['# AthenaFlow V3 CUA results','',f'Result policy: {result["result_policy"]}. Application execution is not performed by this reporting script.','', '| Group | Total | PASS | FAIL | BLOCKED | NOT_RUN | Evaluated pass rate | Execution coverage | Suite success fraction |','| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |']
 def row(label,s):return f'| {label} | {s["total"]} | {s["PASS"]} | {s["FAIL"]} | {s["BLOCKED"]} | {s["NOT_RUN"]} | {rate(s["evaluated_pass_rate"])} | {rate(s["execution_coverage"])} | {rate(s["suite_success_fraction"])} |'
 lines.append(row('Overall',result['overall']))
 for cat in ['by_difficulty','by_module']:
  for label,s in result[cat].items():lines.append(row(label,s))
 lines.extend(['','First-final-outcome summary: '+json.dumps(result['first_final_outcome']), '', 'N/A means no evaluated cases, not zero performance. BLOCKED and NOT_RUN are excluded from evaluated pass rate but remain in fixed suite coverage and success denominators.','', 'Application version segments, evidence gaps, exact model availability and actual upload status must accompany these numbers.'])
 (out/'summary.md').write_text('\n'.join(lines)+'\n')
 with (out/'results.csv').open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.writer(f);w.writerow(['Test ID','Module','Difficulty','Status','Attempt','Reason code','Observed result','Environment','Application commit'])
  for t in tests:
   r=byid[t['test_id']];w.writerow([t['test_id'],t['module'],t['difficulty'],r['status'],r.get('attempt_number',0),r.get('reason_code',''),r.get('observed_result') or '',r.get('environment_id') or '',r.get('application_commit') or 'UNVERIFIED'])
 print(json.dumps(result['overall']))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--out',type=Path);a=p.parse_args();root=a.root.resolve();summary(root,a.out or root/'reports/current')
