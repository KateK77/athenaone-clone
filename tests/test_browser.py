"""Browser tests exercise visible UI; these are not Computer Use Agent evaluations."""
import os
from pathlib import Path
from datetime import datetime,timedelta
from io import StringIO
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command
from django.test import override_settings
from django.utils import timezone
from playwright.sync_api import sync_playwright,expect
from core.models import Patient
from clinical.models import Encounter

@override_settings(STORAGES={'default':{'BACKEND':'django.core.files.storage.FileSystemStorage'},'staticfiles':{'BACKEND':'django.contrib.staticfiles.storage.StaticFilesStorage'}})
class BrowserTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser_errors=[]
    def setUp(self):
        call_command('seed_demo',stdout=StringIO())
        self.encounter_id=Encounter.objects.filter(provider__user__username='physician.demo',status='Documentation Pending').first().pk
        self.v2_patient_id=Patient.objects.get(mrn='AF-100001').pk
        self.v2_encounter_id=Encounter.objects.filter(patient__provider__department__name='Family Medicine',status='Documentation Pending').first().pk
        self.v3_schedule_date=timezone.localtime(Encounter.objects.get(pk=self.encounter_id).appointment.start).date().isoformat()
        if self._testMethodName == 'test_v2_unread_notifications_and_single_compose':
            from engagement.models import Message
            Message.objects.all().delete()
        self.playwright=sync_playwright().start()
        self.browser=self.playwright.chromium.launch(headless=True)
        self.context=self.browser.new_context(viewport={'width':1536,'height':1100})
        self.page=self.context.new_page()
        self.errors=[]
        import traceback
        from django.core.signals import got_request_exception
        self.capture_server_error=lambda **kwargs: self.errors.append(traceback.format_exc())
        got_request_exception.connect(self.capture_server_error)
        self.page.on('pageerror',lambda e:self.errors.append(str(e)))
        self.page.on('dialog',lambda d:d.accept())
    def tearDown(self):
        self.context.close(); self.browser.close(); self.playwright.stop()
        from django.core.signals import got_request_exception
        got_request_exception.disconnect(self.capture_server_error)
        self.assertEqual(self.errors,[],'Browser JavaScript or server errors')
    def go(self,path):
        response=self.page.goto(self.live_server_url+path)
        self.assertLess(response.status,500,f'Server error at {path}: {self.errors}')
        return response
    def sign_in(self,role):
        self.go('/login/')
        if self.page.url.endswith('/dashboard/') or self.page.url.endswith('/portal/'):
            self.page.locator('details.profile summary').click(); self.page.get_by_role('button',name='Sign out',exact=True).click()
        self.page.locator('#username').fill(role+'.demo'); self.page.locator('#password').fill('DemoCare2026!')
        self.page.get_by_role('button',name='Sign in to AthenaFlow').click()
        expect(self.page.locator('h1')).to_be_visible()
    def snap(self,name):
        if os.getenv('CAPTURE_SCREENSHOTS')=='1':
            folder=Path(__file__).resolve().parent.parent/'docs'/'screenshots'; folder.mkdir(parents=True,exist_ok=True)
            self.page.screenshot(path=str(folder/(name+'.png')),full_page=True)
    def save(self): self.page.get_by_role('button',name='Save changes',exact=True).click()
    def action(self,name): self.page.get_by_role('button',name=name+' →',exact=True).click()

    def v3_snap(self,name):
        if os.getenv('CAPTURE_V3_SCREENSHOTS')=='1':
            self.page.evaluate('window.scrollTo(0,0)')
            self.page.evaluate('Promise.all(document.getAnimations().map(a=>a.finished.catch(()=>{})))')
            self.page.screenshot(path=str(Path(__file__).resolve().parent.parent/'docs'/'screenshots'/('v3-'+name+'.png')),full_page=True)

    def assert_no_page_overflow(self):
        self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'),self.page.viewport_size['width']+1)

    def test_v3_readability_and_complete_selected_patient(self):
        self.go('/login/')
        role=self.page.get_by_role('button',name='Front Desk',exact=True)
        self.assertGreaterEqual(role.bounding_box()['height'],44)
        self.assertGreaterEqual(role.evaluate('e=>parseFloat(getComputedStyle(e).fontSize)'),16)
        self.v3_snap('login')
        self.sign_in('frontdesk'); self.go('/records/schedule/new/')
        self.page.get_by_label('Search patient by name or MRN',exact=True).fill('AF-100001')
        self.page.locator('#id_patient').select_option(str(self.v2_patient_id))
        summary=self.page.locator('.selected-record').first
        expect(summary).to_contain_text('Jamie Alder'); expect(summary).to_contain_text('AF-100001')
        expect(summary).to_contain_text('DOB')
        for width in [1280,390]:
            self.page.set_viewport_size({'width':width,'height':900});self.assert_no_page_overflow()
            field=self.page.locator('#id_patient')
            self.assertGreaterEqual(field.evaluate('e=>parseFloat(getComputedStyle(e).fontSize)'),16)
            self.assertGreaterEqual(field.evaluate('e=>parseFloat(getComputedStyle(e).borderTopWidth)'),2)
        self.v3_snap('patient-selection-mobile')

    def test_v3_schedule_auto_date_and_responsive_appointments(self):
        self.sign_in('frontdesk'); self.go('/schedule/')
        field=self.page.get_by_label('Schedule date',exact=True)
        field.fill(self.v3_schedule_date)
        expect(self.page).to_have_url(__import__('re').compile('date='+self.v3_schedule_date))
        expect(self.page.locator('.appointment-block').first).to_be_visible()
        self.assertGreaterEqual(self.page.locator('.appointment-block strong').first.evaluate('e=>parseFloat(getComputedStyle(e).fontSize)'),18)
        self.v3_snap('schedule')
        self.page.set_viewport_size({'width':390,'height':844});self.assert_no_page_overflow();self.v3_snap('schedule-mobile')
        self.page.get_by_role('link',name='Next date',exact=True).click()
        self.assertNotEqual(self.page.get_by_label('Schedule date',exact=True).input_value(),self.v3_schedule_date)

    def test_v3_portal_prominent_actions_and_contact_editing(self):
        self.sign_in('patient');self.v3_snap('portal')
        shortcuts=self.page.get_by_role('navigation',name='Patient portal shortcuts')
        expect(shortcuts).to_be_visible()
        shortcuts.get_by_role('link',name='Medications & renewals',exact=True).click()
        renewal=self.page.get_by_role('button',name='Request medication renewal',exact=True).first
        expect(renewal).to_be_visible();self.assertGreaterEqual(renewal.bounding_box()['height'],44)
        self.page.get_by_text('Update contact information',exact=True).click()
        self.page.get_by_label('Phone',exact=True).fill('202-555-0123')
        self.page.get_by_role('button',name='Save information',exact=True).click()
        self.page.get_by_text('Update contact information',exact=True).click()
        expect(self.page.get_by_label('Phone',exact=True)).to_have_value('202-555-0123')
        self.page.set_viewport_size({'width':390,'height':844});self.assert_no_page_overflow();self.v3_snap('portal-mobile')

    def test_v3_conversion_and_receipt_return_after_browser_back(self):
        self.sign_in('nurse');self.go(f'/encounters/{self.v2_encounter_id}/intake/')
        p=self.page
        for name,value in [('Systolic:','120'),('Diastolic:','79'),('Heart rate:','72'),('Respiratory rate:','16'),('Temperature:','36.7'),('Oxygen:','98'),('Height:','70'),('Weight:','150'),('Pain:','0')]:p.get_by_label(name,exact=True).fill(value)
        for _ in range(5):
            p.get_by_label('Weight unit:',exact=True).select_option('kg');expect(p.get_by_label('Weight:',exact=True)).to_have_value('68.04')
            p.get_by_label('Weight unit:',exact=True).select_option('lb');expect(p.get_by_label('Weight:',exact=True)).to_have_value('150')
        p.get_by_label('Height unit:',exact=True).select_option('cm');p.get_by_label('Weight unit:',exact=True).select_option('kg')
        self.v3_snap('intake');self.save()
        expect(p).to_have_url(self.live_server_url+f'/encounters/{self.v2_encounter_id}/')
        expect(p.locator('.encounter-patient')).to_contain_text('68.04 kg')
        p.reload();expect(p.locator('.encounter-patient')).to_contain_text('68.04 kg');self.v3_snap('encounter')
        self.sign_in('billing');self.go('/records/claims/?status=Partially%20Paid');p.locator('tbody tr').first.get_by_role('link').last.click()
        claim_url=p.url;self.v3_snap('claim')
        p.get_by_role('link',name='Post simulated payment',exact=True).click()
        p.get_by_label('Amount:',exact=True).fill('1.00');p.get_by_role('button',name='Post simulated payment',exact=True).click()
        expect(p.get_by_role('heading',name='Payment recorded',exact=True)).to_be_visible()
        expect(p.get_by_role('link',name='← Return to claim',exact=True)).to_have_attribute('href',claim_url.replace(self.live_server_url,''))
        self.v3_snap('receipt');p.go_back();expect(p).to_have_url(claim_url)
        expect(p.locator('.workflow-panel')).to_be_visible()

    def test_login_navigation_and_screenshots(self):
        self.go('/login/'); self.snap('login')
        self.sign_in('physician'); expect(self.page.get_by_role('heading',name='Practice overview',exact=True)).to_be_visible(); self.snap('dashboard')
        self.page.get_by_role('link',name='Schedule',exact=True).click(); expect(self.page.locator('.calendar-columns')).to_be_visible(); self.snap('schedule')
        self.go(f'/encounters/{self.encounter_id}/'); expect(self.page.get_by_role('heading',name='Encounter documentation')).to_be_visible(); self.snap('encounter')
        self.go('/ai/'); expect(self.page.get_by_role('heading',name='Clinical assistant',exact=True)).to_be_visible()

    def test_search_filter_and_patient_chart(self):
        self.sign_in('admin')
        self.page.get_by_role('textbox',name='Search patients by name or MRN').fill('AF-100001')
        self.page.get_by_role('textbox',name='Search patients by name or MRN').press('Enter')
        expect(self.page.locator('tbody tr')).to_have_count(1)
        self.page.get_by_role('link',name='AF-100001',exact=True).click()
        expect(self.page.get_by_role('heading',name='Jamie Alder',exact=True).first).to_be_visible(); self.snap('patient')
        self.page.get_by_role('link',name='Results',exact=True).last.click(); expect(self.page.locator('.chart-grid')).to_contain_text('HbA1c')
        self.go('/records/patients/?page=2'); expect(self.page.locator('.pagination')).to_contain_text('Page 2')

    def test_registration_to_encounter_signoff(self):
        p=self.page
        self.sign_in('frontdesk'); self.go('/records/patients/new/')
        p.get_by_label('First name:',exact=True).fill('Browser'); p.get_by_label('Last name:',exact=True).fill('Fictional')
        p.get_by_label('Date of birth:').fill('1990-01-02'); p.get_by_label('Sex:',exact=True).select_option('Female')
        p.get_by_label('Phone:',exact=True).fill('202-555-0188'); p.get_by_label('Address:',exact=True).fill('101 Synthetic Street')
        p.get_by_label('Provider:',exact=True).select_option(label='Dr. Alex Morgan'); p.get_by_label('Consent:',exact=True).check(); self.save()
        expect(p.locator('.alert.success')).to_contain_text('saved')
        patient_url=p.url; patient_id=patient_url.rstrip('/').split('/')[-1]
        p.get_by_role('link',name='+ Add insurance',exact=True).click()
        p.get_by_label('Payer:',exact=True).fill('Synthetic Test Health'); p.get_by_label('Plan:',exact=True).fill('Demo PPO')
        p.get_by_label('Member id:').fill('NS999999'); p.get_by_label('Subscriber:',exact=True).fill('Browser Fictional')
        p.get_by_label('Effective:',exact=True).fill('2020-01-01'); p.get_by_label('Expiration:',exact=True).fill('2035-12-31'); self.save(); self.action('Verify eligibility')
        expect(p.locator('.detail-fields')).to_contain_text('Active')
        self.go(f'/records/schedule/new/?patient={patient_id}')
        p.get_by_label('Provider:',exact=True).select_option(label='Dr. Alex Morgan'); p.get_by_label('Department:',exact=True).select_option(label='Family Medicine')
        p.get_by_label('Appointment type:',exact=True).select_option(label='Follow-up')
        day=timezone.localdate()+timedelta(days=30)
        while day.weekday()>4: day+=timedelta(days=1)
        p.get_by_label('Start:',exact=True).fill(str(day)+'T14:00'); p.get_by_label('Duration:',exact=True).fill('30'); p.get_by_label('Reason:',exact=True).fill('Synthetic follow-up'); self.save()
        appointment_url=p.url
        self.action('Confirmed'); self.action('Arrived'); p.get_by_role('link',name='Complete check-in',exact=True).click()
        for name in ['Identity:','Demographics:','Insurance:','Consent:','Intake forms:']: p.get_by_label(name,exact=True).check()
        p.get_by_label('Copay:',exact=True).fill('25'); self.save()
        expect(p.locator('.alert.success')).to_contain_text('clinical intake worklist')
        encounter_url=p.get_by_role('link',name='Open encounter',exact=True).get_attribute('href')
        self.sign_in('nurse'); self.go(encounter_url); p.get_by_role('link',name='Record intake & vitals',exact=True).click()
        p.get_by_label('Intake:',exact=True).fill('Medication, allergy, and history review completed for this synthetic visit.')
        for name in ['Medications reviewed:','Allergies reviewed:','History reviewed:']: p.get_by_label(name,exact=True).check()
        p.get_by_label('Height unit:',exact=True).select_option('cm'); p.get_by_label('Weight unit:',exact=True).select_option('kg')
        for name,val in [('Systolic:','120'),('Diastolic:','80'),('Heart rate:','72'),('Respiratory rate:','16'),('Temperature:','36.7'),('Oxygen:','98'),('Height:','175'),('Weight:','70'),('Pain:','0')]: p.get_by_label(name,exact=True).fill(val)
        self.save(); expect(p.locator('.alert.success')).to_contain_text('vital signs saved')
        p.goto(appointment_url); self.action('Roomed')
        self.sign_in('physician'); p.goto(appointment_url); self.action('In Progress'); self.go(encounter_url)
        expect(p.get_by_role('link',name='+ Add diagnosis',exact=True)).to_be_visible()
        p.get_by_role('link',name='+ Add diagnosis',exact=True).click(); p.get_by_label('Code:',exact=True).select_option(label='I10 · Essential hypertension'); p.get_by_label('Primary:',exact=True).check(); self.save()
        self.go(encounter_url)
        for field,text in [('Subjective','Patient reports follow-up for blood pressure.'),('Objective','Recorded vitals reviewed. Synthetic exam documented.'),('Assessment','Hypertension follow-up; clinician reviewed.'),('Plan','Follow-up in the demonstration clinic. Patient instructions recorded.')]: p.get_by_label(field+':',exact=True).fill(text)
        p.get_by_role('button',name='Save draft',exact=True).click(); expect(p.locator('.alert.success')).to_contain_text('Save draft completed')
        p.get_by_label('I reviewed the note, diagnoses, reconciliation, and orders.').check(); p.get_by_role('button',name='Sign saved note',exact=True).click()
        expect(p.locator('.signed-banner')).to_contain_text('Signed by physician.demo')
        p.get_by_role('button',name='Close encounter',exact=True).click(); expect(p.locator('.heading-actions .status')).to_have_text('Closed')
        p.reload(); expect(p.locator('.note-preview')).to_contain_text('Patient instructions recorded.')
        self.sign_in('coder'); self.go(encounter_url); p.get_by_role('link',name='+ Add charge',exact=True).click()
        p.get_by_label('Procedure:',exact=True).select_option(label='99213 · Demo established outpatient visit'); p.get_by_label('Diagnosis:',exact=True).select_option(label='I10 · Essential hypertension'); p.get_by_label('Amount:',exact=True).fill('125'); self.save(); self.action('Approve charge')
        self.go(encounter_url); p.get_by_role('button',name='Generate claim',exact=True).click(); claim_url=p.url
        self.action('Review'); self.action('Validate'); expect(p.locator('.card-header .status').first).to_have_text('Validated')
        self.sign_in('billing'); p.goto(claim_url)
        for action in ['Submit','Payer response','Adjudicate']: self.action(action)
        expect(p.locator('.card-header .status').first).to_have_text('Paid'); expect(p.locator('.detail-fields')).to_contain_text('0.00')

    def test_ai_draft_and_preview(self):
        self.sign_in('physician'); self.go(f'/encounters/{self.encounter_id}/')
        self.page.get_by_label('Synthetic transcript',exact=True).fill('Synthetic visit: patient requests review of recorded blood pressure.')
        self.page.get_by_role('button',name='Generate draft',exact=True).click()
        expect(self.page.locator('.ai-card')).to_contain_text('Unreviewed draft')
        self.page.get_by_label('I reviewed this draft and will complete missing details.').check()
        self.page.get_by_role('button',name='Apply to unsigned draft',exact=True).click()
        expect(self.page.get_by_label('Subjective:',exact=True)).to_contain_text('Synthetic visit')
        self.page.get_by_role('button',name='Preview note',exact=True).click()
        expect(self.page.locator('#note-dialog')).to_be_visible(); self.page.get_by_role('button',name='Close preview',exact=True).click()
        expect(self.page.get_by_role('button',name='Sign saved note',exact=True)).to_be_visible()

    def test_claim_denial_and_payment(self):
        self.sign_in('billing'); self.go('/records/claims/?status=Denied'); self.snap('claims')
        self.page.locator('tbody tr').first.get_by_role('link').last.click(); claim_url=self.page.url
        self.page.get_by_role('link',name='Review denial / appeal',exact=True).click(); self.page.get_by_role('link',name='Edit record',exact=True).click()
        self.page.get_by_label('Appeal:',exact=True).fill('Synthetic authorization documentation supplied for reprocessing.'); self.save(); self.page.goto(claim_url); self.action('Correct')
        expect(self.page.locator('.card-header .status').first).to_have_text('Draft')
        self.go('/records/claims/?status=Partially%20Paid'); self.page.locator('tbody tr').first.get_by_role('link').last.click()
        self.page.get_by_role('link',name='Post simulated payment',exact=True).click(); self.page.get_by_label('Amount:',exact=True).fill('1.00'); self.page.get_by_role('button',name='Post simulated payment',exact=True).click()
        expect(self.page.get_by_role('heading',name='Payment recorded',exact=True)).to_be_visible(); expect(self.page.locator('.receipt-amount')).to_have_text('$1.00')

    def test_patient_portal_messages_and_requests(self):
        self.sign_in('patient'); expect(self.page.get_by_role('heading',name='Your health, in one place',exact=True)).to_be_visible(); self.snap('portal')
        self.page.get_by_label('Preferred date',exact=True).fill('2027-03-08'); self.page.get_by_label('Reason for visit',exact=True).fill('Browser synthetic request')
        self.page.get_by_role('button',name='Send request',exact=True).click(); expect(self.page.locator('main')).to_contain_text('Browser synthetic request')
        self.page.get_by_role('link',name='+ Message care team',exact=False).click(); self.page.get_by_label('Subject:',exact=True).fill('Browser portal question'); self.page.get_by_label('Message:',exact=True).fill('Initial portal message.'); self.page.get_by_role('button',name='Send message',exact=True).click()
        self.page.get_by_label('Your message',exact=True).fill('Synthetic question about visit preparation.'); self.page.get_by_role('button',name='Send message →',exact=True).click()
        self.page.reload(); expect(self.page.locator('.message-history')).to_contain_text('Synthetic question about visit preparation.')
        response=self.go('/records/claims/'); self.assertEqual(response.status,403)

    def test_mobile_layout_and_accessible_navigation(self):
        self.sign_in('physician'); self.page.set_viewport_size({'width':390,'height':844}); self.page.reload()
        self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'),391)
        self.page.get_by_role('button',name='Toggle navigation',exact=True).click()
        expect(self.page.locator('.sidebar')).to_be_in_viewport(); self.snap('mobile')

    def test_invalid_form_retains_values(self):
        self.sign_in('frontdesk'); self.go('/records/patients/new/')
        p=self.page
        for field,value in [('First name:','Invalid'),('Last name:','Synthetic'),('Date of birth:','2099-01-01'),('Phone:','202-555-0188'),('Address:','Demo Ave')]: p.get_by_label(field,exact=True).fill(value)
        p.get_by_label('Sex:',exact=True).select_option('Male'); p.get_by_label('Provider:',exact=True).select_option(label='Dr. Alex Morgan'); self.save()
        expect(p.locator('.errorlist')).to_contain_text('Birth date cannot be in the future.'); expect(p.get_by_label('First name:',exact=True)).to_have_value('Invalid')

    def v2_snap(self, name):
        if os.getenv('CAPTURE_V2_SCREENSHOTS') == '1':
            self.page.locator('.sidebar').evaluate('(el) => Promise.all(el.getAnimations().map(a => a.finished.catch(() => {})))')
            folder=Path(__file__).resolve().parent.parent/'docs'/'screenshots'
            self.page.screenshot(path=str(folder/(name+'.png')),full_page=True)

    def test_v2_patient_search_and_empty_results(self):
        self.sign_in('frontdesk');self.go('/records/schedule/new/')
        search=self.page.get_by_label('Search patient by name or MRN',exact=True)
        search.fill('Jamie Alder')
        expect(self.page.locator('#id_patient')).to_contain_text('AF-100001')
        expect(self.page.locator('#id_patient-search-status')).to_contain_text('1 matching choices')
        search.fill('AF-100001');search.press('Enter')
        expect(self.page.locator('#id_patient')).to_be_focused()
        self.page.locator('#id_patient').select_option(str(self.v2_patient_id))
        search.fill('No such patient 12345')
        expect(self.page.locator('#id_patient-search-status')).to_contain_text('No matches')
        expect(self.page.locator('#id_patient')).to_have_value(str(self.v2_patient_id))
        search.press('Escape');self.v2_snap('v2-patient-search')

    def test_v2_unit_switching_and_saved_mobile_vitals(self):
        self.sign_in('nurse')
        self.go(f'/encounters/{self.v2_encounter_id}/intake/')
        p=self.page
        expect(p.get_by_label('Height unit:',exact=True)).to_have_value('in')
        expect(p.get_by_label('Weight unit:',exact=True)).to_have_value('lb')
        p.get_by_label('Height unit:',exact=True).select_option('cm');p.get_by_label('Weight unit:',exact=True).select_option('kg')
        for name,val in [('Systolic:','120'),('Diastolic:','80'),('Heart rate:','72'),('Respiratory rate:','16'),('Temperature:','36.7'),('Oxygen:','98'),('Height:','175'),('Weight:','70'),('Pain:','0')]:p.get_by_label(name,exact=True).fill(val)
        for _ in range(4):
            p.get_by_label('Height unit:',exact=True).select_option('in');p.get_by_label('Weight unit:',exact=True).select_option('lb')
            expect(p.locator('#bmi-preview')).to_contain_text('22.9')
            p.get_by_label('Height unit:',exact=True).select_option('cm');p.get_by_label('Weight unit:',exact=True).select_option('kg')
        expect(p.get_by_label('Height:',exact=True)).to_have_value('175');expect(p.get_by_label('Weight:',exact=True)).to_have_value('70')
        p.get_by_label('Height unit:',exact=True).select_option('in');p.get_by_label('Weight unit:',exact=True).select_option('lb')
        self.v2_snap('v2-unit-selection');self.save()
        expect(p).to_have_url(self.live_server_url+f'/encounters/{self.v2_encounter_id}/')
        expect(p.locator('.encounter-patient')).to_contain_text('154.32 lb')
        p.reload()
        p.set_viewport_size({'width':390,'height':844})
        expect(p.locator('.encounter-patient .card')).to_be_visible()
        expect(p.locator('.encounter-patient')).to_contain_text('68.9 in')
        expect(p.locator('.encounter-patient')).to_contain_text('154.32 lb')
        expect(p.locator('.encounter-patient')).to_contain_text('BMI 22.9')
        self.assertLessEqual(p.evaluate('document.documentElement.scrollWidth'),391)
        self.v2_snap('v2-mobile-vitals')

    def test_v2_patient_logout_menu_stays_in_viewport(self):
        self.sign_in('patient')
        for width in [390,700,1280]:
            self.page.set_viewport_size({'width':width,'height':844})
            self.page.locator('details.profile').evaluate('(el)=>el.open=true')
            button=self.page.get_by_role('button',name='Sign out',exact=True)
            expect(button).to_be_in_viewport()
            bounds=self.page.locator('.profile-menu').bounding_box()
            self.assertGreaterEqual(bounds['x'],0);self.assertLessEqual(bounds['x']+bounds['width'],width)
            self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'),width+1)
        self.page.set_viewport_size({'width':390,'height':844});self.v2_snap('v2-patient-logout')
        self.page.get_by_role('button',name='Sign out',exact=True).click()
        expect(self.page.locator('#username')).to_be_visible()

    def test_v2_unread_notifications_and_single_compose(self):
        self.sign_in('patient');self.go('/records/messages/new/')
        p=self.page
        p.get_by_label('Subject:',exact=True).fill('V2 message notification')
        p.get_by_label('Message:',exact=True).fill('Synthetic initial body from compose form.')
        p.get_by_role('button',name='Send message',exact=True).click()
        thread_url=p.url
        expect(p.locator('.message-history')).to_contain_text('Synthetic initial body')
        self.sign_in('physician');self.go('/records/messages/')
        expect(p.locator('.message-notification .unread-count')).to_have_text('1')
        row=p.locator('tr').filter(has=p.get_by_role('link',name='V2 message notification',exact=True))
        expect(row.locator('.unread-label')).to_be_visible();self.v2_snap('v2-unread-messages')
        row.get_by_role('link',name='V2 message notification',exact=True).click()
        expect(p.locator('.message-notification .unread-count')).to_be_hidden()

        p.get_by_label('Your message',exact=True).fill('Synthetic clinician reply.')
        p.get_by_role('button',name='Send message →',exact=True).click()
        self.sign_in('patient');expect(p.locator('.message-notification .unread-count')).to_have_text('1')
        p.goto(thread_url);expect(p.locator('.message-history')).to_contain_text('Synthetic clinician reply.')
        expect(p.locator('.message-notification .unread-count')).to_be_hidden()

    def test_v2_new_reply_updates_badge_without_reload(self):
        self.page.clock.install()
        self.sign_in('patient');self.go('/records/messages/new/')
        p=self.page
        p.get_by_label('Subject:',exact=True).fill('V2 live badge')
        p.get_by_label('Message:',exact=True).fill('Synthetic notification check.')
        p.get_by_role('button',name='Send message',exact=True).click()
        thread_url=p.url
        self.go('/records/messages/')
        staff_context=self.browser.new_context()
        try:
            staff=staff_context.new_page();staff.goto(self.live_server_url+'/login/')
            staff.locator('#username').fill('physician.demo');staff.locator('#password').fill('DemoCare2026!')
            staff.get_by_role('button',name='Sign in to AthenaFlow').click();staff.goto(thread_url)
            staff.get_by_label('Your message',exact=True).fill('A newly received reply.')
            staff.get_by_role('button',name='Send message →',exact=True).click()
            expect(staff.locator('.message-history')).to_contain_text('A newly received reply.')
            p.bring_to_front();p.clock.fast_forward(21000)
            row=p.locator('tr').filter(has=p.get_by_role('link',name='V2 live badge',exact=True))
            expect(row.locator('.unread-label')).to_be_visible()
            expect(p.locator('.message-notification .unread-count')).to_be_visible()
        finally:
            staff_context.close()
