"""V3 regressions run only in Django's isolated test database."""
import csv
from datetime import datetime
from decimal import Decimal
from io import StringIO
from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.utils import timezone
from core.forms import VitalForm
from core.models import CheckIn
from clinical.models import Encounter, VitalSign
from revenue.models import Claim, Payment, Denial
from core.services import generate_ai


@override_settings(STORAGES={'default':{'BACKEND':'django.core.files.storage.FileSystemStorage'},'staticfiles':{'BACKEND':'django.contrib.staticfiles.storage.StaticFilesStorage'}})
class V3Tests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('seed_demo', anchor_date='2026-11-16', stdout=StringIO())

    def setUp(self):
        self.doctor=User.objects.get(username='physician.demo')
        self.billing=User.objects.get(username='billing.demo')
        self.encounter=Encounter.objects.filter(provider__user=self.doctor,status='Documentation Pending').first()

    def form(self, **overrides):
        data=dict(systolic=120,diastolic=79,heart_rate=72,respiratory_rate=16,
                  temperature='36.7',oxygen=98,height='70',weight='150',pain=0,height_unit='in',weight_unit='lb')
        data.update(overrides)
        return VitalForm(data)

    def test_imperial_save_retains_precision_and_readable_display(self):
        form=self.form()
        self.assertTrue(form.is_valid(),form.errors)
        v=form.save(commit=False); v.encounter=self.encounter; v.author=self.doctor; v.save(); v.refresh_from_db()
        self.assertEqual(v.height,Decimal('177.80000000'))
        self.assertEqual(v.weight,Decimal('68.03885550'))
        self.assertEqual(v.display_weight,'150')
        v.weight_unit='kg'; v.height_unit='cm'
        self.assertEqual(v.display_height,'177.8'); self.assertEqual(v.display_weight,'68.04')
        self.assertEqual(v.bmi,Decimal('21.5'))

    def test_roundtrip_metadata_preserves_original_measurement(self):
        form=self.form(height='177.8',weight='68.04',height_unit='cm',weight_unit='kg',
                       height_canonical='177.80000000',weight_canonical='68.03885550')
        self.assertTrue(form.is_valid(),form.errors)
        v=form.save(commit=False); v.encounter=self.encounter; v.author=self.doctor; v.save(); v.refresh_from_db()
        self.assertEqual(v.weight,Decimal('68.03885550'))
        initial=VitalForm(instance=v)
        self.assertEqual(initial['weight'].value(),'68.04')
        again=self.form(**{name:initial[name].value() for name in ['height','height_unit','weight','weight_unit','height_canonical','weight_canonical']})
        self.assertTrue(again.is_valid(),again.errors)
        self.assertEqual(again.save(commit=False).weight,v.weight)

    def test_changed_value_overrides_stale_or_invalid_metadata(self):
        for supplied in ['68.03885550','NaN','Infinity','1E999','bad','-3']:
            form=self.form(weight='80',weight_unit='kg',weight_canonical=supplied)
            self.assertTrue(form.is_valid(),form.errors)
            self.assertEqual(form.save(commit=False).weight,Decimal('80'))

    def test_precision_units_ranges_and_error_redisplay(self):
        for data in [dict(weight='68.038855'),dict(weight_unit='stone'),dict(weight='500.01',weight_unit='kg')]:
            self.assertFalse(self.form(**data).is_valid(),data)
        form=self.form(systolic=1,weight='68.04',weight_unit='kg',weight_canonical='68.03885550')
        self.assertFalse(form.is_valid())
        self.assertEqual(form['weight'].value(),'68.04')
        self.assertEqual(form['weight_canonical'].value(),'68.03885550')

    def test_ai_objective_units_and_application_remains_unsigned(self):
        form=self.form(); self.assertTrue(form.is_valid(),form.errors)
        v=form.save(commit=False); v.encounter=self.encounter; v.author=self.doctor; v.save()
        draft=generate_ai(self.doctor,self.encounter,'Synthetic workflow follow-up.')
        for fact in ['120/79 mmHg','72 bpm','16 breaths/min','36.7 °C','98%','70 in','150 lb','BMI 21.5','Pain 0/10']:
            self.assertIn(fact,draft.output['objective'])
        self.client.force_login(self.doctor)
        r=self.client.post(f'/encounters/{self.encounter.pk}/',{'action':'Approve AI draft','draft':draft.pk,
            'version':self.encounter.note.version,'acknowledge':'on'},follow=True)
        self.assertContains(r,'The note remains unsigned')
        self.encounter.note.refresh_from_db(); self.assertIsNone(self.encounter.note.signed_at)

    def test_report_submission_date_is_independent_of_encounter_date(self):
        claim=Claim.objects.first()
        submitted=timezone.make_aware(datetime(2026,11,25,16,1))
        Claim.objects.filter(pk=claim.pk).update(submitted_at=submitted,status='Accepted')
        self.client.force_login(self.billing)
        query='?start=2026-11-25&end=2026-11-25&provider='+str(claim.encounter.provider_id)
        r=self.client.get('/reports/'+query)
        values=dict(r.context['metrics'])
        self.assertEqual(values['Claims submitted'],1); self.assertEqual(values['Encounters'],0)
        self.assertEqual(values['Acceptance rate'],'100.0%')
        self.assertContains(r,'Latest submission date')
        rows=list(csv.DictReader(StringIO(self.client.get('/reports/'+query+'&export=csv').content.decode())))
        row=next(row for row in rows if row['Metric']=='Claims submitted')
        self.assertEqual(row['Value'],'1'); self.assertEqual(row['Date basis'],'Latest submission date')
        for name,value in r.context['metrics']:
            self.assertEqual(next(row['Value'] for row in rows if row['Metric']==name),str(value))

    def test_provider_payment_filter_keeps_older_claim_and_unlinked_copay(self):
        claim=Claim.objects.first()
        now=timezone.make_aware(datetime(2026,11,25,16))
        Payment.objects.update(created_at=timezone.make_aware(datetime(2026,11,16,12)))
        p=Payment.objects.create(patient=claim.patient,claim=claim,amount=1,source='Insurance',reference='V3-older-claim')
        checkin=CheckIn.objects.filter(appointment__provider=claim.encounter.provider,payment__isnull=True).first()
        if checkin is None:
            from core.models import Appointment
            a=Appointment.objects.filter(provider=claim.encounter.provider,checkin__isnull=True).first()
            checkin=CheckIn.objects.create(appointment=a)
        copay=Payment.objects.create(patient=checkin.appointment.patient,checkin=checkin,amount=25,source='Copay',reference='V3-unlinked-copay')
        Payment.objects.filter(pk__in=[p.pk,copay.pk]).update(created_at=now)
        self.client.force_login(self.billing)
        r=self.client.get(f'/reports/?start=2026-11-25&end=2026-11-25&provider={claim.encounter.provider_id}')
        self.assertEqual(dict(r.context['metrics'])['Simulated payments'],'$26.00')

    def test_claim_next_action_and_denial_return(self):
        denial=Denial.objects.first(); self.client.force_login(self.billing)
        claim_url=f'/records/claims/{denial.claim_id}/'
        r=self.client.get(claim_url)
        self.assertContains(r,'CLAIM WORKFLOW'); self.assertContains(r,'Correct →',count=1)
        for path in [f'/records/denials/{denial.pk}/',f'/records/denials/{denial.pk}/edit/']:
            response=self.client.get(path)
            self.assertContains(response,'Back to related claim'); self.assertContains(response,claim_url)

    def test_receipt_return_balance_and_payment_replay(self):
        claim=Claim.objects.filter(status='Partially Paid').first()
        before=claim.balance; self.client.force_login(self.billing)
        url=f'/claims/{claim.pk}/payment/'
        r=self.client.get(url); self.assertIn('no-store',r['Cache-Control'])
        token=r.context['form']['token'].value()
        data={'amount':'1.00','source':'Insurance','token':token}
        r=self.client.post(url,data,follow=True)
        self.assertContains(r,'Return to claim'); self.assertContains(r,'View payment history')
        self.assertContains(r,f'${before-1:.2f}'); self.assertIn('no-store',r['Cache-Control'])
        self.client.post(url,data)
        claim.refresh_from_db(); self.assertEqual(claim.balance,before-1)
        self.assertEqual(Payment.objects.filter(reference='SIM-'+token.upper()).count(),1)

    def test_patient_receipt_only_links_to_portal_bills(self):
        patient=User.objects.get(username='patient.demo'); self.client.force_login(patient)
        p=Payment.objects.create(patient=patient.patient,claim=None,amount=1,source='Patient',reference='V3-patient-receipt')
        r=self.client.get(f'/payments/{p.pk}/receipt/')
        self.assertContains(r,'/portal/#bills'); self.assertNotContains(r,'/records/claims/')

    def test_schedule_groups_filters_and_accessible_form(self):
        self.client.force_login(self.doctor)
        appointment=self.encounter.appointment
        day=timezone.localtime(appointment.start).date()
        r=self.client.get(f'/schedule/?date={day}&provider={appointment.provider_id}')
        self.assertContains(r,'data-schedule-filters')
        self.assertIn(f'provider={appointment.provider_id}',r.context['next_query'])
        self.assertTrue(all(c['appointments'] for c in r.context['columns']))
        self.assertNotContains(r,'Available during office hours')
