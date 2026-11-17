from datetime import datetime,timedelta,date
from decimal import Decimal
from io import StringIO
from unittest.mock import patch
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError,PermissionDenied
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import IntegrityError,transaction
from django.test import TestCase,Client,override_settings
from django.utils import timezone
from core.models import *
from clinical.models import *
from revenue.models import *
from engagement.models import *
from core.services import *
from core.access import patients_for
from core.registry import R

@override_settings(STORAGES={'default':{'BACKEND':'django.core.files.storage.FileSystemStorage'},'staticfiles':{'BACKEND':'django.contrib.staticfiles.storage.StaticFilesStorage'}})
class WorkflowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('seed_demo',anchor_date='2026-11-16',stdout=StringIO())
    def setUp(self):
        self.users={r:User.objects.get(username=r+'.demo') for r,_ in ROLES}
        self.admin=self.users['admin']; self.doctor=self.users['physician']; self.patient=Patient.objects.get(user=self.users['patient'])
        self.e=Encounter.objects.filter(provider__user=self.doctor,status='Documentation Pending').first()
    def login(self,role_name): self.client.force_login(self.users[role_name])
    def appointment(self,patient=None):
        p=patient or self.patient
        start=timezone.make_aware(datetime(2027,1,4,9,0))
        return Appointment(patient=p,provider=p.provider,department=p.provider.department,appointment_type=AppointmentType.objects.first(),start=start,duration=30,reason='Synthetic follow-up')
    def fresh_claim(self):
        e=self.e
        sign_note(self.doctor,e,True)
        Charge.objects.create(encounter=e,procedure=ProcedureCode.objects.first(),diagnosis=e.diagnoses.first().code,amount=100,approved=True)
        policy=e.patient.policies.first(); policy.status='Active'; policy.member_id='NS888888'; policy.effective=date(2020,1,1); policy.expiration=date(2030,1,1); policy.save()
        return create_claim(self.users['billing'],e)
    def test_seed_totals(self):
        expected={Patient:100,Provider:8,Appointment:150,Encounter:100,ClinicalNote:100,Problem:100,Medication:150,MedicalOrder:100,LabResult:100,Claim:80,Denial:20,Payment:30,Authorization:20,MessageThread:30}
        for model,count in expected.items(): self.assertEqual(model.objects.count(),count,model.__name__)
    def test_seed_idempotent(self):
        call_command('seed_demo',stdout=StringIO()); self.assertEqual(Patient.objects.count(),100)
    def test_fixture_schedule_and_clinical_consistency(self):
        for appointment in Appointment.objects.all():
            with self.subTest(appointment=appointment.pk): appointment.full_clean()
        for note in ClinicalNote.objects.exclude(signed_at=None): self.assertEqual(note.signed_by_id,note.encounter.provider.user_id)
        for claim in Claim.objects.all(): self.assertGreaterEqual(claim.balance,0)
    def test_sign_rejects_template_placeholders(self):
        note=self.e.note; note.plan='[Clinician to complete]'; note.save()
        with self.assertRaises(ValidationError): sign_note(self.doctor,self.e,True)
    def test_claim_edit_preserves_empty_validation_lists(self):
        self.login('billing'); claim=Claim.objects.filter(status='Draft').first()
        response=self.client.post(f'/records/claims/{claim.pk}/edit/',{'policy':claim.policy_id,'scenario':'Partial'})
        self.assertEqual(response.status_code,302); claim.refresh_from_db(); self.assertEqual(claim.scenario,'Partial')
    def test_seed_disabled_outside_demo(self):
        with override_settings(DEMO_MODE=False),self.assertRaises(CommandError): call_command('seed_demo',stdout=StringIO())
    def test_reset_requires_local_flag(self):
        with self.assertRaises(CommandError): call_command('seed_demo',reset=True,confirm='RESET SYNTHETIC DEMO',stdout=StringIO())
    def test_all_demo_accounts_authenticate(self):
        for r,_ in ROLES:
            c=Client(); self.assertTrue(c.login(username=r+'.demo',password='DemoCare2026!'))
    def test_login_logout_post(self):
        r=self.client.post('/login/',{'username':'physician.demo','password':'DemoCare2026!'})
        self.assertEqual(r.status_code,302); self.assertEqual(self.client.get('/logout/').status_code,405)
        self.assertEqual(self.client.post('/logout/').status_code,302)
    def test_anonymous_redirect(self): self.assertEqual(self.client.get('/records/patients/').status_code,302)
    def test_invalid_login(self): self.assertContains(self.client.post('/login/',{'username':'physician.demo','password':'bad'}),'Unable to sign in')
    def test_csrf_enforced(self):
        c=Client(enforce_csrf_checks=True); c.force_login(self.admin)
        self.assertEqual(c.post('/records/patients/new/',{}).status_code,403)
    def test_admin_pages_render(self):
        self.login('admin')
        for url in ['/dashboard/','/schedule/','/schedule/?view=week','/schedule/?view=department','/reports/','/ai/','/administration/','/help/']+[f'/records/{k}/' for k in R]:
            with self.subTest(url=url): self.assertEqual(self.client.get(url).status_code,200)
    def test_all_record_details_render(self):
        self.login('admin')
        for key,spec in R.items():
            obj=spec.model.objects.first()
            if obj:
                with self.subTest(key=key): self.assertEqual(self.client.get(f'/records/{key}/{obj.pk}/').status_code,200)
    def test_creation_forms_render(self):
        self.login('admin')
        for key,spec in R.items():
            if spec.write and key not in ['claims','denials']:
                with self.subTest(key=key): self.assertEqual(self.client.get(f'/records/{key}/new/').status_code,200)
    def test_every_role_dashboard(self):
        for r,_ in ROLES:
            self.login(r); self.assertEqual(self.client.get('/dashboard/',follow=True).status_code,200)
    def test_role_restrictions(self):
        checks=[('patient','/records/patients/'),('frontdesk','/records/orders/'),('billing','/records/medications/'),('nurse','/administration/'),('assistant','/records/claims/')]
        for r,url in checks:
            self.login(r); self.assertEqual(self.client.get(url).status_code,403,(r,url))
    def test_patient_isolation_fhir(self):
        self.login('patient'); other=Patient.objects.exclude(pk=self.patient.pk).first()
        self.assertEqual(self.client.get(f'/fhir/Patient/{other.pk}/').status_code,403)
        self.assertEqual(self.client.get(f'/fhir/Patient/{self.patient.pk}/').status_code,200)
    def test_physician_assigned_scope(self):
        other=Patient.objects.exclude(provider__user=self.doctor).exclude(appointments__provider__user=self.doctor).first()
        self.login('physician'); self.assertEqual(self.client.get(f'/patients/{other.pk}/').status_code,404)
    def test_patient_message_isolation(self):
        self.login('patient'); other=MessageThread.objects.exclude(patient=self.patient).first()
        self.assertEqual(self.client.get(f'/records/messages/{other.pk}/').status_code,404)
        self.assertEqual(self.client.post(f'/records/messages/{other.pk}/',{'body':'unauthorized'}).status_code,404)
    def test_patient_form_choices_scoped(self):
        self.login('patient'); response=self.client.get('/records/messages/new/')
        self.assertEqual(list(response.context['form'].fields['patient'].queryset),[self.patient])
    def test_future_birth_rejected(self):
        self.patient.dob=timezone.localdate()+timedelta(days=1)
        with self.assertRaises(ValidationError): self.patient.full_clean()
    def test_duplicate_patient_rejected(self):
        p=Patient(first_name=self.patient.first_name.lower(),last_name=self.patient.last_name.upper(),dob=self.patient.dob,sex='Male',phone='202-555-0199',address='Demo',provider=self.patient.provider)
        with self.assertRaises(ValidationError): p.full_clean()
    def test_registration_persists(self):
        self.login('frontdesk')
        data={'first_name':'Test','last_name':'Fictional','dob':'1990-02-03','sex':'Female','phone':'202-555-0188','address':'Synthetic Ave','provider':self.patient.provider_id,'consent':'on','active':'on','language':'English'}
        response=self.client.post('/records/patients/new/',data)
        self.assertEqual(response.status_code,302); p=Patient.objects.get(first_name='Test',last_name='Fictional')
        self.assertTrue(p.mrn.startswith('AF-')); self.assertTrue(AuditEvent.objects.filter(object_id=str(p.pk),action='Record created').exists())
    def test_search_and_pagination(self):
        self.login('admin'); r=self.client.get('/records/patients/?q=AF-100001')
        self.assertEqual(r.context['page'].paginator.count,1)
        self.assertEqual(self.client.get('/records/patients/?page=2').context['page'].number,2)
    def test_appointment_overlap_rejected(self):
        a=self.appointment(); save_appointment(self.admin,a)
        b=self.appointment(); b.start+=timedelta(minutes=15)
        with self.assertRaises(ValidationError): save_appointment(self.admin,b)
    def test_adjacent_appointments_allowed(self):
        a=self.appointment(); save_appointment(self.admin,a)
        b=self.appointment(); b.start+=timedelta(minutes=30); save_appointment(self.admin,b)
        self.assertNotEqual(a.pk,b.pk)
    def test_cancelled_slot_reusable(self):
        a=self.appointment(); save_appointment(self.admin,a); transition_appointment(self.admin,a.pk,'Cancelled')
        b=self.appointment(); save_appointment(self.admin,b); self.assertTrue(b.pk)
    def test_outside_availability_rejected(self):
        a=self.appointment(); a.start=timezone.make_aware(datetime(2027,1,3,9))
        with self.assertRaises(ValidationError): save_appointment(self.admin,a)
    def test_department_mismatch_rejected(self):
        a=self.appointment(); a.department=Department.objects.exclude(pk=a.department_id).first()
        with self.assertRaises(ValidationError): save_appointment(self.admin,a)
    def test_invalid_appointment_transition(self):
        a=self.appointment(); save_appointment(self.admin,a)
        with self.assertRaises(ValidationError): transition_appointment(self.admin,a.pk,'Completed')
    def test_frontdesk_cannot_room(self):
        a=self.appointment(); a.status='Checked In'; a.save()
        with self.assertRaises(PermissionDenied): transition_appointment(self.users['frontdesk'],a.pk,'Roomed')
    def test_checkin_to_encounter_and_copay(self):
        a=self.appointment(); a.status='Arrived'; a.save()
        policy=self.patient.policies.first(); policy.effective=timezone.localdate()-timedelta(days=2); policy.expiration=timezone.localdate()+timedelta(days=90); policy.save()
        record=CheckIn(appointment=a,identity=True,demographics=True,insurance=True,consent=True,intake_forms=True,copay=25)
        e=complete_checkin(self.users['frontdesk'],record)
        a.refresh_from_db(); self.assertEqual(a.status,'Checked In'); self.assertEqual(e.patient,self.patient)
        self.assertTrue(hasattr(e,'note')); self.assertTrue(Task.objects.filter(patient=self.patient,category='Intake').exists()); self.assertEqual(Payment.objects.get(checkin=record).amount,25)
    def test_incomplete_checkin_rolls_back(self):
        a=self.appointment(); a.status='Arrived'; a.save()
        with self.assertRaises(ValidationError): complete_checkin(self.admin,CheckIn(appointment=a,identity=True,copay=25))
        self.assertFalse(Encounter.objects.filter(appointment=a).exists()); self.assertFalse(CheckIn.objects.filter(appointment=a).exists())
    def test_intake_vitals_bmi(self):
        self.login('nurse')
        r=self.client.post(f'/encounters/{self.e.pk}/intake/',{'complaint':'Follow-up','intake':'Reviewed','medications_reviewed':'on','allergies_reviewed':'on','history_reviewed':'on','systolic':120,'diastolic':80,'heart_rate':70,'respiratory_rate':16,'temperature':'36.7','oxygen':98,'height':180,'weight':81,'pain':0})
        self.assertEqual(r.status_code,302); self.assertEqual(self.e.vitals.order_by('-pk').first().bmi,Decimal('25.0'))
    def test_vital_range_rejected(self):
        v=self.e.vitals.first(); v.oxygen=120
        with self.assertRaises(ValidationError): v.full_clean()
    def test_note_version_conflict(self):
        n=self.e.note
        save_note(self.doctor,self.e,{'subjective':'New','objective':'Exam','assessment':'Assessment','plan':'Plan'},n.version)
        with self.assertRaises(ValidationError): save_note(self.doctor,self.e,{},n.version)
        self.assertEqual(NoteVersion.objects.filter(note=n).count(),1)
    def test_nurse_cannot_sign(self):
        with self.assertRaises(PermissionDenied): sign_note(self.users['nurse'],self.e,True)
    def test_sign_requires_documentation(self):
        n=self.e.note; n.plan=''; n.save()
        with self.assertRaises(ValidationError): sign_note(self.doctor,self.e,True)
    def test_sign_requires_acknowledgment(self):
        with self.assertRaises(ValidationError): sign_note(self.doctor,self.e,False)
    def test_sign_requires_reconciliation(self):
        self.e.history_reviewed=False; self.e.save()
        with self.assertRaises(ValidationError): sign_note(self.doctor,self.e,True)
    def test_signed_note_immutable_and_addendum(self):
        sign_note(self.doctor,self.e,True); n=ClinicalNote.objects.get(encounter=self.e); original=n.plan; n.plan='Alteration'
        with self.assertRaises(ValidationError): n.save()
        self.login('physician'); r=self.client.post(f'/encounters/{self.e.pk}/',{'action':'Add addendum','text':'Auditable correction'})
        self.assertEqual(r.status_code,302); n.refresh_from_db(); self.assertEqual(n.plan,original); self.assertEqual(n.addenda.count(),1)
    def test_ai_draft_requires_approval_and_never_signs(self):
        before=self.e.note.subjective; draft=generate_ai(self.doctor,self.e,'Synthetic follow-up transcript')
        self.e.note.refresh_from_db(); self.assertEqual(self.e.note.subjective,before); self.assertFalse(self.e.note.signed_at)
        self.login('physician'); r=self.client.post(f'/encounters/{self.e.pk}/',{'action':'Approve AI draft','draft':draft.pk,'acknowledge':'on','version':self.e.note.version})
        self.assertEqual(r.status_code,302); self.e.note.refresh_from_db(); self.assertIn('Synthetic follow-up transcript',self.e.note.subjective); self.assertIsNone(self.e.note.signed_at)
    def test_ai_output_escapes_transcript(self):
        draft=generate_ai(self.doctor,self.e,'<script>alert(1)</script>')
        self.login('physician'); r=self.client.get(f'/encounters/{self.e.pk}/')
        self.assertContains(r,'&lt;script&gt;'); self.assertNotContains(r,'<script>alert(1)</script>')
    def test_order_task_and_result_portal_lifecycle(self):
        e=self.e
        o=MedicalOrder.objects.create(encounter=e,diagnosis=e.diagnoses.first(),category='Laboratory',test='HbA1c')
        order_action(self.doctor,o,'Signed'); self.assertTrue(Task.objects.filter(related_url=f'/records/orders/{o.pk}/').exists())
        order_action(self.users['nurse'],o,'Processing')
        result=LabResult.objects.create(order=o,value='6.5',unit='%',reference='4–5.6',flag='High')
        order_action(self.users['nurse'],o,'Completed'); result_action(self.users['nurse'],result,'Published')
        result_action(self.doctor,result,'Reviewed'); result_action(self.doctor,result,'Released')
        result.refresh_from_db(); self.assertTrue(result.released); self.assertEqual(result.reviewed_by,self.doctor)
    def test_result_cannot_release_before_review(self):
        result=LabResult.objects.filter(status='Published',order__encounter__provider__user=self.doctor).first()
        with self.assertRaises(ValidationError): result_action(self.doctor,result,'Released')
    def test_unreleased_result_hidden(self):
        result=LabResult.objects.filter(order__encounter__patient=self.patient).first(); result.released=False; result.save()
        self.login('patient'); self.assertEqual(self.client.get(f'/fhir/DiagnosticReport/{result.pk}/').status_code,403)
        self.assertNotIn(result,list(self.client.get('/portal/').context['results']))
    def test_cross_patient_order_diagnosis_rejected(self):
        o=MedicalOrder(encounter=self.e,diagnosis=Problem.objects.exclude(patient=self.e.patient).first(),category='Laboratory',test='CBC')
        with self.assertRaises(ValidationError): o.full_clean()
    def test_medication_warning(self):
        med=Medication(patient=self.patient,provider=self.patient.provider,name='Amoxicillin',strength='500 mg',dose='1 tablet',frequency='Daily')
        self.assertTrue(medication_warnings(med))
    def test_medication_requires_warning_acknowledgment(self):
        med=Medication.objects.create(patient=self.patient,provider=self.patient.provider,name='Amoxicillin',strength='500 mg',dose='1 tablet',frequency='Daily')
        self.login('physician'); self.client.post(f'/records/medications/{med.pk}/action/',{'action':'Sign prescription'})
        med.refresh_from_db(); self.assertEqual(med.status,'Draft')
        self.client.post(f'/records/medications/{med.pk}/action/',{'action':'Sign prescription','acknowledge':'on'}); med.refresh_from_db(); self.assertEqual(med.status,'Active')
    def test_billing_full_paid_workflow(self):
        claim=self.fresh_claim()
        for action in ['Review','Validate','Submit','Payer response','Adjudicate']: claim_action(self.users['billing'],claim,action)
        claim.refresh_from_db(); self.assertEqual(claim.status,'Paid'); self.assertEqual(claim.balance,0)
        claim_action(self.users['billing'],claim,'Close'); claim.refresh_from_db(); self.assertEqual(claim.status,'Closed')
    def test_claim_scrub_blocking(self):
        claim=self.fresh_claim(); claim.policy=None; claim.save()
        claim_action(self.users['billing'],claim,'Review'); claim_action(self.users['billing'],claim,'Validate'); claim.refresh_from_db()
        self.assertEqual(claim.status,'Validation Failed'); self.assertIn('Missing insurance policy.',claim.validation_errors)
        with self.assertRaises(ValidationError): claim_action(self.users['billing'],claim,'Submit')
    def test_claim_submit_revalidates(self):
        claim=self.fresh_claim(); claim_action(self.users['billing'],claim,'Review'); claim_action(self.users['billing'],claim,'Validate')
        policy=claim.policy; policy.status='Inactive'; policy.save()
        with self.assertRaises(ValidationError): claim_action(self.users['billing'],claim,'Submit')
    def test_duplicate_claim_rejected(self):
        claim=self.fresh_claim()
        with self.assertRaises(ValidationError): create_claim(self.users['billing'],claim.encounter)
    def test_missing_authorization_blocks(self):
        claim=self.fresh_claim(); MedicalOrder.objects.create(encounter=claim.encounter,diagnosis=claim.encounter.diagnoses.first(),category='Imaging',test='Synthetic MRI',authorization_required=True,status='Signed')
        self.assertTrue(any('authorization' in x for x in scrub(claim)[0]))
    def test_denial_correction_resubmission(self):
        claim=self.fresh_claim(); claim.scenario='Deny'; claim.save()
        for action in ['Review','Validate','Submit','Payer response','Adjudicate']: claim_action(self.users['billing'],claim,action)
        claim.refresh_from_db(); self.assertEqual(claim.status,'Denied'); self.assertTrue(hasattr(claim,'denial'))
        with self.assertRaises(ValidationError): claim_action(self.users['billing'],claim,'Correct')
        denial=claim.denial; denial.appeal='Synthetic supporting documentation supplied'; denial.save()
        claim_action(self.users['billing'],claim,'Correct'); claim.refresh_from_db(); self.assertEqual(claim.status,'Draft'); self.assertEqual(claim.scenario,'Pay')
        for action in ['Review','Validate','Submit','Payer response','Adjudicate']: claim_action(self.users['billing'],claim,action)
        claim.refresh_from_db(); self.assertEqual(claim.balance,0)
    def test_partial_payment_and_balance(self):
        claim=self.fresh_claim(); claim.scenario='Partial'; claim.save()
        for action in ['Review','Validate','Submit','Payer response','Adjudicate']: claim_action(self.users['billing'],claim,action)
        claim.refresh_from_db(); self.assertEqual(claim.status,'Partially Paid'); self.assertEqual(claim.balance,Decimal('30.00'))
        post_payment(self.users['billing'],claim,Decimal('30.00')); claim.refresh_from_db(); self.assertEqual(claim.balance,0)
    def test_overpayment_negative_and_precision_rejected(self):
        claim=Claim.objects.filter(status='Partially Paid').first()
        for amount in ['-1','0','99999','0.001','NaN']:
            with self.subTest(amount=amount),self.assertRaises(ValidationError): post_payment(self.users['billing'],claim,amount)
    def test_payment_database_positive_constraint(self):
        with self.assertRaises(IntegrityError),transaction.atomic(): Payment.objects.create(patient=self.patient,amount=-1,source='Patient',reference='NEGATIVE')
    def test_patient_cannot_pay_another_balance(self):
        claim=Claim.objects.exclude(encounter__patient=self.patient).filter(status='Partially Paid').first()
        self.login('patient'); self.assertEqual(self.client.get(f'/claims/{claim.pk}/payment/').status_code,404)
    def test_payment_duplicate_form_prevented(self):
        claim=Claim.objects.filter(status='Partially Paid').first(); self.login('billing')
        r=self.client.get(f'/claims/{claim.pk}/payment/'); token=r.context['form'].initial['token']; data={'amount':'1.00','source':'Patient','token':token}
        self.assertEqual(self.client.post(f'/claims/{claim.pk}/payment/',data).status_code,302)
        self.client.post(f'/claims/{claim.pk}/payment/',data)
        self.assertEqual(Payment.objects.filter(reference='SIM-'+token.upper()).count(),1)
    def test_portal_request_enters_frontdesk_queue(self):
        self.login('patient'); r=self.client.post('/portal/',{'action':'Request appointment','date':str(timezone.localdate()+timedelta(days=10)),'reason':'Synthetic follow-up'})
        self.assertEqual(r.status_code,302); self.assertTrue(AppointmentRequest.objects.filter(patient=self.patient).exists()); self.assertTrue(Task.objects.filter(category='Appointment request',patient=self.patient).exists())
    def test_portal_message_creates_staff_task(self):
        self.login('patient'); thread=self.patient.threads.first(); self.client.post(f'/records/messages/{thread.pk}/',{'body':'Synthetic message'})
        self.assertTrue(Task.objects.filter(patient=self.patient,category='Message').exists()); self.assertEqual(thread.messages.last().sender,self.users['patient'])
    def test_portal_renewal_creates_task(self):
        self.login('patient'); med=self.patient.medications.first(); self.client.post('/portal/',{'action':'Renew medication','id':med.pk})
        self.assertTrue(Task.objects.filter(patient=self.patient,category='Medication renewal').exists())
    def test_reports_csv(self):
        self.login('manager'); r=self.client.get('/reports/?start=2026-10-01&end=2026-12-01&export=csv')
        self.assertEqual(r.status_code,200); self.assertIn('text/csv',r['Content-Type']); self.assertIn(b'Total charges',r.content)
    def test_audit_after_transition(self):
        a=self.appointment(); save_appointment(self.admin,a); transition_appointment(self.admin,a.pk,'Confirmed')
        event=AuditEvent.objects.filter(entity='core.Appointment',object_id=str(a.pk),action='Appointment transition').first()
        self.assertEqual(event.detail,{'before':'Scheduled','after':'Confirmed'})
    def test_fhir_resource_exports(self):
        self.login('admin')
        examples={'Patient':Patient,'Appointment':Appointment,'Encounter':Encounter,'Condition':Problem,'Observation':VitalSign,'MedicationRequest':Medication,'ServiceRequest':MedicalOrder,'DiagnosticReport':LabResult,'Coverage':InsurancePolicy}
        for name,model in examples.items():
            r=self.client.get(f'/fhir/{name}/{model.objects.first().pk}/'); self.assertEqual(r.status_code,200); self.assertEqual(r.json()['resourceType'],name)
    def test_health(self): self.assertEqual(self.client.get('/health/').json()['status'],'ok')
    def test_waitlist_books_matching_slot(self):
        self.login('frontdesk')
        w=WaitlistEntry.objects.create(patient=self.patient,provider=self.patient.provider,earliest=date(2027,2,1),latest=date(2027,2,5),reason='Synthetic waitlist')
        r=self.client.post(f'/records/waitlist/{w.pk}/action/',{'action':'Find & book slot'})
        self.assertEqual(r.status_code,302); w.refresh_from_db(); self.assertEqual(w.status,'Booked'); self.assertEqual(w.appointment.patient,self.patient)
        self.assertTrue(Task.objects.filter(patient=self.patient,category='Notification').exists())
    def test_authorization_requires_support_and_transitions(self):
        auth=Authorization.objects.filter(status='Draft').first(); auth.supporting_notes=''; auth.save(); self.login('billing')
        self.client.post(f'/records/authorizations/{auth.pk}/action/',{'action':'Submit authorization'})
        auth.refresh_from_db(); self.assertEqual(auth.status,'Draft')
        auth.supporting_notes='Synthetic records reviewed'; auth.save()
        for action in ['Submit authorization','Pending Review','Approve authorization']: self.client.post(f'/records/authorizations/{auth.pk}/action/',{'action':action})
        auth.refresh_from_db(); self.assertEqual(auth.status,'Approved'); self.assertIsNotNone(auth.submitted_at)
    def test_patient_request_booking_integrates_schedule(self):
        req=AppointmentRequest.objects.create(patient=self.patient,preferred_date=date(2027,2,1),reason='Requested follow-up')
        self.login('frontdesk')
        response=self.client.post(f'/requests/{req.pk}/book/',{'patient':self.patient.pk,'provider':self.patient.provider_id,'department':self.patient.provider.department_id,'appointment_type':AppointmentType.objects.first().pk,'start':'2027-02-01T13:00','duration':30,'reason':req.reason})
        self.assertEqual(response.status_code,302); req.refresh_from_db(); self.assertEqual(req.status,'Booked'); self.assertEqual(req.appointment.patient,self.patient)
    def test_task_completion_changes_dashboard_count(self):
        self.login('physician'); before=self.client.get('/dashboard/').context['metrics'][-1][1]
        obj=Task.objects.filter(patient__in=patients_for(self.doctor),role='physician',status='Open').first()
        self.client.post(f'/records/tasks/{obj.pk}/action/',{'action':'Complete task'})
        after=self.client.get('/dashboard/').context['metrics'][-1][1]; self.assertEqual(after,before-1)
    def test_admin_cannot_remove_own_access(self):
        self.login('admin'); response=self.client.post(f'/administration/staff/{self.admin.pk}/',{'username':self.admin.username,'first_name':'Avery','last_name':'Brooks','role':'nurse','department':self.admin.profile.department_id,'is_active':'on'})
        self.assertContains(response,'cannot remove your own administrator access'); self.admin.profile.refresh_from_db(); self.assertEqual(self.admin.profile.role,'admin')
    def test_approved_charge_locked_after_validation(self):
        claim=self.fresh_claim()
        claim_action(self.users['billing'],claim,'Review'); claim_action(self.users['billing'],claim,'Validate')
        charge=claim.encounter.charges.first(); self.login('coder')
        response=self.client.post(f'/records/charges/{charge.pk}/edit/',{'encounter':charge.encounter_id,'procedure':charge.procedure_id,'diagnosis':charge.diagnosis_id,'units':1,'amount':'1.00'})
        self.assertContains(response,'Charges are locked after claim validation.'); charge.refresh_from_db(); self.assertEqual(charge.amount,100)
    def test_primary_coding_cannot_change_signed_diagnosis(self):
        problem=Problem.objects.filter(encounter__status='Closed').first(); self.login('coder')
        new_code=DiagnosisCode.objects.exclude(pk=problem.code_id).first()
        response=self.client.post(f'/records/problems/{problem.pk}/edit/',{'patient':problem.patient_id,'encounter':problem.encounter_id,'code':new_code.pk,'primary':'on','status':'Active','notes':'Change'})
        self.assertContains(response,'Signed encounter diagnoses and orders cannot be changed.'); problem.refresh_from_db(); self.assertNotEqual(problem.code_id,new_code.pk)
    def test_resolve_longitudinal_problem_preserves_signed_note(self):
        problem=Problem.objects.filter(encounter__provider__user=self.doctor,encounter__status='Closed').first(); original=problem.encounter.note.assessment
        self.login('physician'); response=self.client.post(f'/records/problems/{problem.pk}/edit/',{'patient':problem.patient_id,'encounter':problem.encounter_id,'code':problem.code_id,'primary':'on','status':'Resolved','notes':'Resolved at later follow-up'})
        self.assertEqual(response.status_code,302); problem.refresh_from_db(); self.assertEqual(problem.status,'Resolved'); self.assertEqual(problem.encounter.note.assessment,original)
    def test_reports_values_change_with_data(self):
        self.login('manager'); url='/reports/?start=2026-01-01&end=2035-01-01'
        response=self.client.get(url); before=dict(response.context['metrics'])['Appointments']
        a=self.appointment(); save_appointment(self.admin,a)
        after=dict(self.client.get(url).context['metrics'])['Appointments']; self.assertEqual(after,before+1)
    def test_checkin_replay_cannot_duplicate_copay(self):
        a=self.appointment(); a.status='Arrived'; a.save()
        record=CheckIn(appointment=a,identity=True,demographics=True,insurance=True,consent=True,intake_forms=True,copay=20)
        complete_checkin(self.admin,record)
        with self.assertRaises(ValidationError): complete_checkin(self.admin,record)
        self.assertEqual(Payment.objects.filter(checkin=record).count(),1)
    def test_generic_encounter_route_preserves_coding_boundary(self):
        self.e.intake='CLINICAL-INTAKE-SENSITIVE-TEST'; self.e.save()
        self.login('billing'); r=self.client.get(f'/records/encounters/{self.e.pk}/')
        self.assertTemplateUsed(r,'coding.html'); self.assertNotContains(r,'CLINICAL-INTAKE-SENSITIVE-TEST')
    def test_patient_cannot_export_unsigned_prescription(self):
        med=Medication.objects.create(patient=self.patient,provider=self.patient.provider,name='Demo medication',strength='Demo',dose='Demo',frequency='Demo')
        self.login('patient'); self.assertEqual(self.client.get(f'/fhir/MedicationRequest/{med.pk}/').status_code,403)
    def test_result_review_records_clinician_comment(self):
        result=LabResult.objects.filter(status='Published',order__encounter__provider__user=self.doctor).first()
        result_action(self.doctor,result,'Reviewed','Synthetic clinician review comment')
        result.refresh_from_db(); self.assertEqual(result.comment,'Synthetic clinician review comment')
    def test_blank_database_url_uses_sqlite_locally(self):
        import os,subprocess,sys
        env=os.environ.copy(); env.update(DATABASE_URL='',DEBUG='true')
        result=subprocess.run([sys.executable,'-c',"from config.settings import DATABASES; print(DATABASES['default']['ENGINE'])"],capture_output=True,text=True,env=env)
        self.assertEqual(result.returncode,0); self.assertIn('django.db.backends.sqlite3',result.stdout)
    def test_production_refuses_sqlite_fallback(self):
        import os,subprocess,sys,secrets
        env=os.environ.copy(); env.update(DATABASE_URL='',DEBUG='false',SECRET_KEY=secrets.token_urlsafe(64))
        result=subprocess.run([sys.executable,'-c','import config.settings'],capture_output=True,text=True,env=env)
        self.assertNotEqual(result.returncode,0); self.assertIn('Production requires an explicit PostgreSQL',result.stderr)
