"""V2 regression cases use isolated databases, never the local acceptance records."""
from datetime import date, datetime
from decimal import Decimal
from io import StringIO
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.utils import timezone
from core.models import Patient, Appointment, AppointmentType, CheckIn, AuditEvent
from clinical.models import Encounter, ClinicalNote, VitalSign, MedicalOrder
from revenue.models import Claim, Payment
from engagement.models import MessageThread, Message, MessageRead
from core.forms import VitalForm
from core.services import complete_checkin, transition_appointment, post_payment
from engagement.messaging import unread_messages


@override_settings(STORAGES={'default':{'BACKEND':'django.core.files.storage.FileSystemStorage'},'staticfiles':{'BACKEND':'django.contrib.staticfiles.storage.StaticFilesStorage'}})
class V2Tests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('seed_demo', anchor_date='2026-11-16', stdout=StringIO())

    def setUp(self):
        self.doctor = User.objects.get(username='physician.demo')
        self.nurse = User.objects.get(username='nurse.demo')
        self.patient_user = User.objects.get(username='patient.demo')
        self.patient = Patient.objects.get(user=self.patient_user)
        self.billing = User.objects.get(username='billing.demo')

    def vitals(self, **changes):
        data = dict(systolic=120,diastolic=80,heart_rate=72,respiratory_rate=16,temperature='36.7',oxygen=98,height='175',weight='70',pain=0,height_unit='cm',weight_unit='kg')
        data.update(changes)
        return VitalForm(data)

    def test_new_intake_defaults_imperial(self):
        form = VitalForm()
        self.assertEqual(form['height_unit'].value(), 'in')
        self.assertEqual(form['weight_unit'].value(), 'lb')

    def test_both_unit_systems_save_same_bmi(self):
        for kwargs in [{},dict(height='68.9',weight='154.32',height_unit='in',weight_unit='lb',height_canonical='175',weight_canonical='70')]:
            form = self.vitals(**kwargs)
            self.assertTrue(form.is_valid(), form.errors)
            v = form.save(commit=False)
            self.assertEqual(v.height,Decimal('175.0'))
            self.assertEqual(v.weight,Decimal('70.0'))
            self.assertEqual(v.bmi,Decimal('22.9'))

    def test_units_and_normalized_ranges_validated(self):
        for changes in [dict(height_unit='ft'),dict(weight_unit='stone'),dict(height='200',height_unit='in'),dict(weight='2000',weight_unit='lb')]:
            self.assertFalse(self.vitals(**changes).is_valid(),changes)

    def test_invalid_vitals_keep_typed_units_and_values(self):
        form=self.vitals(height='68.897638',height_unit='in',systolic=1)
        self.assertFalse(form.is_valid())
        self.assertEqual(form['height'].value(),'68.897638')
        self.assertEqual(form['height_unit'].value(),'in')

    def test_legacy_metric_post_and_existing_vitals_preserved(self):
        data=dict(self.vitals().data); data.pop('height_unit'); data.pop('weight_unit')
        form=VitalForm(data); self.assertTrue(form.is_valid(),form.errors)
        self.assertEqual(form.save(commit=False).height,175)
        existing=VitalSign.objects.first()
        self.assertEqual(existing.height_unit,'cm');self.assertEqual(existing.weight_unit,'kg')

    def test_patient_search_choices_scoped_and_identified(self):
        self.client.force_login(self.nurse)
        response=self.client.get('/records/messages/new/')
        field=response.context['form'].fields['patient']
        self.assertTrue(all(p.provider.department_id==self.nurse.profile.department_id for p in field.queryset))
        self.assertIn(self.patient.mrn,field.label_from_instance(self.patient))
        self.assertContains(response,'data-search-select="patient"')

    def test_checkbox_false_and_true_persist_on_order(self):
        self.client.force_login(self.doctor)
        e=Encounter.objects.filter(provider__user=self.doctor,status='Documentation Pending').first()
        data=dict(encounter=e.pk,diagnosis=e.diagnoses.first().pk,category='Laboratory',test='V2 checkbox test',priority='Routine')
        response=self.client.post('/records/orders/new/',data)
        self.assertEqual(response.status_code,302)
        order=MedicalOrder.objects.get(test='V2 checkbox test');self.assertFalse(order.authorization_required)
        data['authorization_required']='on'
        self.client.post(f'/records/orders/{order.pk}/edit/',data);order.refresh_from_db();self.assertTrue(order.authorization_required)
        data.pop('authorization_required')
        self.client.post(f'/records/orders/{order.pk}/edit/',data);order.refresh_from_db();self.assertFalse(order.authorization_required)

    def test_checkin_waits_for_physician_start(self):
        a=Appointment.objects.create(patient=self.patient,provider=self.patient.provider,department=self.patient.provider.department,appointment_type=AppointmentType.objects.first(),start=timezone.make_aware(datetime(2027,1,4,9)),duration=30,reason='V2',status='Arrived')
        policy=self.patient.policies.first();policy.status='Active';policy.effective=date(2020,1,1);policy.expiration=date(2035,1,1);policy.save()
        record=CheckIn(appointment=a,identity=True,demographics=True,insurance=True,consent=True,intake_forms=True)
        e=complete_checkin(User.objects.get(username='frontdesk.demo'),record)
        self.assertEqual(e.status,'Scheduled')
        transition_appointment(self.nurse,a.pk,'Roomed')
        with self.assertRaises(PermissionDenied):transition_appointment(self.nurse,a.pk,'In Progress')
        transition_appointment(self.doctor,a.pk,'In Progress');e.refresh_from_db();self.assertEqual(e.status,'In Progress')

    def test_structured_audit_readable_in_detail_and_audit_list(self):
        self.client.force_login(User.objects.get(username='admin.demo'))
        claim=Claim.objects.first()
        AuditEvent.objects.create(actor=self.billing,entity=claim._meta.label,object_id=str(claim.pk),action='Claim Close',detail={'before':'Paid','after':'Closed','copay':'25'})
        for url in [f'/records/claims/{claim.pk}/','/records/audit/']:
            response=self.client.get(url)
            self.assertContains(response,'Paid → Closed');self.assertContains(response,'$25.00')
            self.assertNotContains(response,'&#x27;before&#x27;')

    def test_claim_validation_empty_states(self):
        self.client.force_login(self.billing)
        c=Claim.objects.first();c.status='Draft';c.validation_errors=[];c.validation_warnings=[];c.save()
        self.assertContains(self.client.get(f'/records/claims/{c.pk}/'),'Not yet validated')
        c.status='Validated';c.save()
        response=self.client.get(f'/records/claims/{c.pk}/')
        self.assertContains(response,'No validation errors');self.assertContains(response,'No validation warnings');self.assertNotContains(response,'[]')

    def thread(self):
        Message.objects.all().delete()
        thread=MessageThread.objects.create(patient=self.patient,subject='V2 unread test')
        Message.objects.create(thread=thread,sender=self.patient_user,body='Patient request')
        return thread

    def test_compose_subject_and_body_atomic(self):
        self.client.force_login(self.patient_user)
        self.client.post('/records/messages/new/',{'patient':self.patient.pk,'subject':'V2 compose','body':'First body'})
        thread=MessageThread.objects.get(subject='V2 compose')
        self.assertEqual(thread.messages.get().body,'First body')
        response=self.client.post('/records/messages/new/',{'patient':self.patient.pk,'subject':'V2 invalid','body':''})
        self.assertEqual(response.status_code,200);self.assertFalse(MessageThread.objects.filter(subject='V2 invalid').exists())
        self.assertContains(response,'V2 invalid')

    def test_read_state_is_per_user_and_new_reply_is_unread(self):
        thread=self.thread()
        self.assertEqual(unread_messages(self.patient_user).count(),0)
        self.assertEqual(unread_messages(self.doctor).count(),1)
        self.client.force_login(self.doctor)
        self.client.get(f'/records/messages/{thread.pk}/')
        self.assertEqual(unread_messages(self.doctor).count(),0)
        self.assertEqual(unread_messages(self.nurse).count(),1)
        self.client.post(f'/records/messages/{thread.pk}/',{'body':'Received'})
        self.assertEqual(unread_messages(self.patient_user).count(),1)
        self.client.force_login(self.patient_user);self.client.get(f'/records/messages/{thread.pk}/')
        self.assertEqual(unread_messages(self.patient_user).count(),0)
        Message.objects.create(thread=thread,sender=self.doctor,body='New reply')
        response=self.client.get('/messages/notifications/')
        self.assertEqual(response.json()['count'],1);self.assertEqual(response['Cache-Control'],'no-store')

    def test_notification_scoping_and_list_does_not_mark_read(self):
        thread=self.thread()
        self.client.force_login(self.doctor)
        response=self.client.get('/records/messages/')
        self.assertContains(response,'unread-thread');self.assertEqual(unread_messages(self.doctor).count(),1)
        self.client.force_login(self.patient_user)
        other=Patient.objects.exclude(pk=self.patient.pk).first()
        t=MessageThread.objects.create(patient=other,subject='Other private thread')
        Message.objects.create(thread=t,sender=self.doctor,body='Hidden')
        self.assertEqual(self.client.get('/messages/notifications/').json()['count'],0)
        self.assertEqual(self.client.get(f'/records/messages/{t.pk}/').status_code,404)
        self.assertEqual(self.client.get(f'/patients/{other.pk}/').status_code,404)
        self.assertEqual(self.client.get('/administration/').status_code,403)

    def test_closed_claim_payment_hidden_and_post_blocked(self):
        self.client.force_login(self.billing)
        c=Claim.objects.first();c.status='Closed';c.save()
        response=self.client.get(f'/records/claims/{c.pk}/')
        self.assertNotContains(response,'Post simulated payment')
        self.assertEqual(self.client.get(f'/claims/{c.pk}/payment/').status_code,403)
        with self.assertRaises(ValidationError):post_payment(self.billing,c,1)

    def test_denial_is_not_patient_responsibility(self):
        c=Claim.objects.filter(encounter__patient=self.patient).first();c.status='Denied';c.patient_responsibility=None;c.save()
        self.client.force_login(self.patient_user)
        self.assertFalse(c.can_patient_pay)
        self.assertContains(self.client.get('/portal/'),'not a confirmed amount you owe')
        self.assertEqual(self.client.post(f'/claims/{c.pk}/payment/',{'amount':'1','source':'Patient'}).status_code,403)
        with self.assertRaises(ValidationError):post_payment(self.patient_user,c,1)

    def test_confirmed_patient_share_allows_only_that_amount(self):
        c=Claim.objects.filter(encounter__patient=self.patient).first();c.status='Denied';c.save()
        self.client.force_login(self.billing)
        self.client.post(f'/claims/{c.pk}/responsibility/',{'amount':'20.00'})
        c.refresh_from_db();self.assertEqual(c.patient_due,20)
        with self.assertRaises(ValidationError):post_payment(self.patient_user,c,21)
        post_payment(self.patient_user,c,5);c.refresh_from_db();self.assertEqual(c.patient_due,15)
        self.client.force_login(self.patient_user)
        self.assertEqual(self.client.post(f'/claims/{c.pk}/responsibility/',{'amount':'100'}).status_code,403)

    def test_reporting_csv_filter_parity(self):
        self.client.force_login(User.objects.get(username='manager.demo'))
        query=f'?start=2026-11-01&end=2026-11-30&provider={self.patient.provider_id}'
        report=self.client.get('/reports/'+query)
        export=self.client.get('/reports/'+query+'&export=csv')
        import csv
        rows=list(csv.reader(StringIO(export.content.decode())))
        exported={row[0]:row[1] for row in rows[1:]}
        for label,value in report.context['metrics']:self.assertEqual(exported[label],str(value))
        expected=Appointment.objects.filter(start__date__range=(date(2026,11,1),date(2026,11,30)),provider=self.patient.provider).count()
        self.assertEqual(dict(report.context['metrics'])['Appointments'],expected)

    def test_zero_balance_rejects_duplicate_payment(self):
        c=Claim.objects.first();c.payments.all().delete();c.status='Adjudicated';c.save()
        post_payment(self.billing,c,c.balance,'Insurance');c.refresh_from_db()
        self.assertEqual(c.balance,0);self.assertFalse(c.can_post_payment)
        with self.assertRaises(ValidationError):post_payment(self.billing,c,1)
