"""Reproducible fictional fixtures. No fixture logic is used by workflow services."""
from datetime import date,datetime,timedelta
from decimal import Decimal
from pathlib import Path
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.sessions.models import Session
from django.core.management.base import BaseCommand,CommandError
from django.db import transaction
from django.utils import timezone
from core.models import *
from clinical.models import *
from revenue.models import *
from engagement.models import *

class Command(BaseCommand):
    help='Initialize the designated fictional demonstration practice. Idempotent unless --reset is specified.'
    def add_arguments(self,parser):
        parser.add_argument('--reset',action='store_true')
        parser.add_argument('--confirm',default='')
        parser.add_argument('--anchor-date',default='',help='YYYY-MM-DD; default local date. Fix this for repeatable research.')

    @transaction.atomic
    def handle(self,*args,**options):
        if not settings.DEMO_MODE: raise CommandError('DEMO_MODE must be true to seed fictional records.')
        if options['reset']:
            db=settings.DATABASES['default']
            if not settings.DEBUG or not settings.ALLOW_DEMO_RESET or db['ENGINE']!='django.db.backends.sqlite3' or Path(db['NAME']).resolve()!=(settings.BASE_DIR/'demo.sqlite3').resolve():
                raise CommandError('Reset is restricted to DEBUG + ALLOW_DEMO_RESET + the local demo.sqlite3 database.')
            if options['confirm']!='RESET SYNTHETIC DEMO': raise CommandError('Explicit confirmation phrase required.')
            if Practice.objects.filter(is_demo=False).exists(): raise CommandError('Non-demo practice found; reset refused.')
            # Dependency-ordered deletion; no production flush command is used.
            for model in [AuditEvent,Payment,Denial,Claim,Charge,LabResult,MedicalOrder,AIDraft,Addendum,NoteVersion,ClinicalNote,VitalSign,Problem,Encounter,CheckIn,WaitlistEntry,AppointmentRequest,Appointment,Message,MessageThread,Task,Medication,Allergy,History,Authorization,InsurancePolicy,Patient,Provider,Profile,AppointmentType,DiagnosisCode,ProcedureCode,Department,Practice,Session]:
                model.objects.all().delete()
            User.objects.filter(username__endswith='.demo').delete()
        if Practice.objects.exists():
            if not Practice.objects.filter(is_demo=True,name='Northstar Medical Group').exists(): raise CommandError('Existing non-demo practice; seeding refused.')
            self.stdout.write('Demo practice already exists; no changes made.'); return
        anchor=date.fromisoformat(options['anchor_date']) if options['anchor_date'] else timezone.localdate()
        practice=Practice.objects.create(name='Northstar Medical Group',is_demo=True)
        departments=[Department.objects.create(practice=practice,name=n) for n in ['Family Medicine','Internal Medicine','Preventive Care']]
        people=[('admin','Avery','Brooks'),('manager','Morgan','Ellis'),('frontdesk','Riley','Chen'),('physician','Alex','Morgan'),('nurse','Jordan','Reed'),('assistant','Casey','Lane'),('billing','Taylor','Park'),('coder','Cameron','Gray'),('patient','Jamie','Alder')]
        users={}; password=make_password('DemoCare2026!')
        for r,first,last in people:
            u=User.objects.create(username=r+'.demo',first_name=first,last_name=last,password=password)
            Profile.objects.create(user=u,role=r,department=departments[0]); users[r]=u
        provider_names=['Dr. Alex Morgan','Dr. Maya Sterling','Dr. Owen Vale','Dr. Nora Linden','Dr. Elias Wren','Dr. Leah Rowan','Dr. Theo Marlow','Dr. Iris West']
        providers=[Provider.objects.create(name=n,department=departments[i%3],user=users['physician'] if i==0 else None) for i,n in enumerate(provider_names)]
        for i,provider in enumerate(providers[1:],start=2):
            first,last=provider.name.removeprefix('Dr. ').split(' ',1)
            provider_user=User.objects.create(username=f'provider{i}.demo',first_name=first,last_name=last,password=password)
            Profile.objects.create(user=provider_user,role='physician',department=provider.department)
            provider.user=provider_user; provider.save()
        types=[AppointmentType.objects.create(name=n,duration=duration) for n,duration in [('Follow-up',30),('Annual Physical',45),('New Patient Visit',45),('Telehealth',30),('Laboratory Visit',15),('Procedure Visit',30),('Urgent Visit',30),('Established Patient Visit',30)]]
        codes=[DiagnosisCode.objects.create(code=code,description=text) for code,text in [('E11.9','Type 2 diabetes mellitus, without complications'),('I10','Essential hypertension'),('Z00.00','General adult medical examination'),('J06.9','Acute upper respiratory infection, unspecified'),('E78.5','Hyperlipidemia, unspecified'),('Z12.11','Screening for malignant neoplasm of colon'),('Z76.0','Issue of repeat prescription'),('R53.83','Other fatigue')]]
        procedures=[ProcedureCode.objects.create(code=c,description=d,amount=a) for c,d,a in [('99213','Demo established outpatient visit',125),('99214','Demo extended outpatient visit',180),('99395','Demo preventive visit',210),('83036','Demo glycated hemoglobin test',35),('80053','Demo metabolic panel',45)]]
        firsts=['Jamie','Amelia','Noah','Olivia','Liam','Sophia','Ethan','Isabella','Lucas','Mia','Harper','Oliver','Avery','Elijah','Charlotte','Henry','Evelyn','James','Aria','Benjamin']
        lasts=['Alder','Briar','Cedar','Dale','Elm']
        patients=[]
        for i in range(100):
            p=Patient.objects.create(mrn=f'AF-{100001+i}',user=users['patient'] if i==0 else None,first_name=firsts[i%20],last_name=lasts[i//20],dob=date(1950+i%50,1+i%12,1+i%27),sex='Female' if i%2 else 'Male',phone=f'202-555-{100+i:04d}',email=f'patient{i+1}@example.invalid',address=f'{100+i} Example Lane, Demo City, IL 60000',emergency_contact=f'Fictional contact · 202-555-{200+i:04d}',provider=providers[i%8],consent=True)
            patients.append(p)
            InsurancePolicy.objects.create(patient=p,payer=['Northstar Demo Health','Evergreen Demo Insurance','Community Demo Plan'][i%3],plan='Synthetic PPO',member_id=f'NS{100000+i}' if i%19 else f'ERR{100000+i}',subscriber=str(p),effective=anchor-timedelta(days=365),expiration=anchor+timedelta(days=365) if i%23 else anchor-timedelta(days=1),status='Active' if i%19 and i%23 else 'Unverified',verified_at=timezone.now() if i%19 and i%23 else None)
            if i%5==0: Allergy.objects.create(patient=p,substance='Penicillin',reaction='Reported rash',severity='Moderate')
            History.objects.create(patient=p,category='Medical',title='Synthetic medical history',detail='Routine preventive care documented; see active problem list.',date=anchor-timedelta(days=90))
            History.objects.create(patient=p,category='Social',title='Lifestyle history',detail='Fictional screening: no tobacco use reported. Regular walking.',date=anchor-timedelta(days=30))
            for k in range(1+(i%2==0)):
                Medication.objects.create(patient=p,provider=p.provider,name=['Metformin','Lisinopril','Atorvastatin'][(i+k)%3],strength=['500 mg','10 mg','20 mg'][(i+k)%3],dose='1 tablet',frequency='Once daily with meal' if (i+k)%3==0 else 'Once daily',status='Active',start_date=anchor-timedelta(days=90),signed_at=timezone.now()-timedelta(days=90))
        # Portal account has active coverage and predictable chronic care data.
        policy=patients[0].policies.first(); policy.member_id='NS100000'; policy.expiration=anchor+timedelta(days=365); policy.status='Active'; policy.verified_at=timezone.now(); policy.save()
        reasons=['Diabetes follow-up','Blood pressure review','Annual wellness visit','Respiratory symptoms','Lipid review','Preventive screening','Medication renewal','Lab review']
        encounters=[]
        for i in range(100):
            p=patients[i]; days=7+(i//8)*2
            visit_day=anchor-timedelta(days=days)
            while visit_day.weekday()>4: visit_day-=timedelta(days=1)
            start=timezone.make_aware(datetime.combine(visit_day,datetime.min.time()))+timedelta(hours=9,minutes=(i//8)%3*60)
            # Make fixture times collision-free even when weekend adjustments share a day.
            while Appointment.objects.filter(provider=p.provider,start=start).exists(): start+=timedelta(hours=1)
            signed=i<80
            a=Appointment.objects.create(patient=p,provider=p.provider,department=p.provider.department,appointment_type=types[i%len(types)],start=start,duration=30,reason=reasons[i%8],status='Checked Out' if signed else 'In Progress')
            e=Encounter.objects.create(patient=p,provider=p.provider,appointment=a,status='Closed' if signed else 'Documentation Pending',complaint=reasons[i%8],intake='Synthetic intake reviewed. Patient-reported medication and allergy history documented.',medications_reviewed=True,allergies_reviewed=True,history_reviewed=True,created_at=start)
            encounters.append(e)
            dx=Problem.objects.create(patient=p,encounter=e,code=codes[i%8],primary=True,notes='Curated synthetic demonstration diagnosis.')
            note=ClinicalNote.objects.create(encounter=e,subjective=f'Patient presents for {reasons[i%8].lower()}. Synthetic history reviewed.',objective='Synthetic examination documented. Vital signs recorded in the visit chart.',assessment=str(codes[i%8]),plan='Review recorded results with the care team. Follow-up visit requested. Patient instructions discussed in this synthetic scenario.',signed_at=start+timedelta(minutes=25) if signed else None,signed_by=p.provider.user if signed else None,provenance='Synthetic seed fixture v1')
            VitalSign.objects.create(encounter=e,author=users['nurse'],systolic=112+i%29,diastolic=70+i%16,heart_rate=65+i%24,respiratory_rate=16,temperature=Decimal('36.7'),oxygen=98,height=170,weight=65+i%30,pain=i%3)
            order=MedicalOrder.objects.create(encounter=e,diagnosis=dx,category='Laboratory',test=['HbA1c','CMP','Lipid Panel','CBC','TSH','Urinalysis'][i%6],status='Completed')
            values=[('7.2','%','4.0–5.6','High'),('93','mg/dL','70–99 (glucose component)','Normal'),('112','mg/dL','<100 (LDL component)','High'),('13.8','g/dL','12–17 (hemoglobin component)','Normal'),('2.1','mIU/L','0.4–4.0','Normal'),('Negative','qualitative','Negative','Normal')][i%6]
            LabResult.objects.create(order=order,value=values[0],unit=values[1],reference=values[2],flag=values[3],status='Reviewed' if i%3==0 else 'Published',reviewed_by=p.provider.user if i%3==0 else None,released=i%6==0,comment='Synthetic result. Panel displays one selected component only.')
            if i%3: Task.objects.create(patient=p,title='Review '+order.test,category='Result',role='physician',related_url=f'/records/results/{order.result.pk}/')
            if not signed: Task.objects.create(patient=p,title='Sign encounter note',category='Unsigned note',role='physician',related_url=f'/encounters/{e.pk}/')
            if signed:
                Charge.objects.create(encounter=e,procedure=procedures[i%3],diagnosis=codes[i%8],amount=procedures[i%3].amount,approved=True)
                status='Denied' if i<20 else 'Paid' if i<40 else 'Partially Paid' if i<50 else 'Draft' if i<65 else 'Submitted'
                claim=Claim.objects.create(encounter=e,policy=p.policies.first(),status=status,scenario='Deny' if i<20 else 'Partial' if i<50 and i>=40 else 'Pay',submitted_at=start+timedelta(days=1) if status!='Draft' else None)
                Claim.objects.filter(pk=claim.pk).update(created_at=start+timedelta(days=1))
                if i<20:
                    Denial.objects.create(claim=claim,reason='Simulated missing authorization documentation',due_date=anchor+timedelta(days=14+i),category='Authorization')
                    Task.objects.create(patient=p,title='Resolve '+str(claim),category='Denial',role='billing',related_url=f'/records/claims/{claim.pk}/')
                elif i<50:
                    Payment.objects.create(patient=p,claim=claim,amount=claim.total if i<40 else (claim.total*Decimal('0.70')).quantize(Decimal('0.01')),source='Insurance',reference=f'SEED-PAY-{i:04d}')
        for i in range(20):
            p=patients[i]
            Authorization.objects.create(patient=p,policy=p.policies.first(),provider=p.provider,service='Synthetic imaging referral',diagnosis=codes[i%8],supporting_notes='Synthetic documentation attached as text.',expiration=anchor+timedelta(days=90),status=['Approved','Draft','Pending Review','Denied'][i%4])
        # 50 additional current/future appointments, including a portal appointment.
        day=anchor
        while day.weekday()>4: day+=timedelta(days=1)
        for i in range(50):
            p=patients[(i*8)%100] if i<12 else patients[i]
            visit=day+timedelta(days=i//24)
            while visit.weekday()>4: visit+=timedelta(days=1)
            hour=8+(i%24)//8
            start=timezone.make_aware(datetime.combine(visit,datetime.min.time()))+timedelta(hours=hour,minutes=(i%2)*30)
            while Appointment.objects.filter(provider=p.provider,start=start).exists(): start+=timedelta(minutes=30)
            # Constrain synthetic active appointments to valid availability.
            if timezone.localtime(start).hour>=17:
                visit+=timedelta(days=1)
                while visit.weekday()>4: visit+=timedelta(days=1)
                start=timezone.make_aware(datetime.combine(visit,datetime.min.time()))+timedelta(hours=8)
                while Appointment.objects.filter(provider=p.provider,start=start).exists(): start+=timedelta(minutes=30)
            Appointment.objects.create(patient=p,provider=p.provider,department=p.provider.department,appointment_type=types[i%8],start=start,duration=30,reason=reasons[i%8],status=['Scheduled','Confirmed','Arrived'][i%3])
        for i in range(30):
            p=patients[i]; thread=MessageThread.objects.create(patient=p,subject=['Follow-up question','Visit preparation','Medication question'][i%3])
            Message.objects.create(thread=thread,sender=users['patient'] if i==0 else users['nurse'],body='Synthetic message: please confirm the next step for the upcoming follow-up visit.',read=i%2==0)
        for i in range(5):
            WaitlistEntry.objects.create(patient=patients[i],provider=patients[i].provider,earliest=day+timedelta(days=2),latest=day+timedelta(days=14),reason='Earlier follow-up requested')
        AuditEvent.objects.create(actor=users['admin'],action='Demo reset' if options['reset'] else 'Demo initialized',entity='core.Practice',object_id=str(practice.pk),detail={'fixture_version':'v1','anchor_date':str(anchor),'synthetic':True})
        self.stdout.write(self.style.SUCCESS('Created 100 patients, 150 appointments, 100 encounters/notes/results, 150 medications, 80 claims, 20 denials, 30 payments, 20 authorizations, and 30 message threads.'))
