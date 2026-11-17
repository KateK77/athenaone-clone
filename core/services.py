from datetime import timedelta
from decimal import Decimal
import re
import uuid
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from core.models import *
from core.access import *
from clinical.models import *
from revenue.models import *
from engagement.models import *

def audit(user, action, obj, **detail):
    return AuditEvent.objects.create(actor=user, action=action, entity=obj._meta.label, object_id=str(obj.pk), detail=detail)

def task(patient, title, category, role_name, url):
    return Task.objects.get_or_create(patient=patient, title=title, category=category, role=role_name, related_url=url, status='Open')[0]

APPOINTMENT_TRANSITIONS = {
    'Scheduled':['Confirmed','Arrived','Cancelled','No Show'],
    'Confirmed':['Arrived','Cancelled','No Show'],
    'Arrived':['Checked In','Cancelled'], 'Checked In':['Roomed'],
    'Roomed':['In Progress'], 'In Progress':['Completed'], 'Completed':['Checked Out'],
}

@transaction.atomic
def save_appointment(user, appointment):
    require(user, OPERATIONS)
    check_patient(user, appointment.patient)
    Provider.objects.select_for_update().get(pk=appointment.provider_id)
    appointment.full_clean()
    appointment.save()
    audit(user,'Schedule saved',appointment)
    return appointment

@transaction.atomic
def transition_appointment(user, pk, target):
    a = Appointment.objects.select_for_update().select_related('patient').get(pk=pk)
    check_patient(user,a.patient)
    if role(user)=='physician' and a.provider.user_id!=user.pk: raise PermissionDenied('This appointment is assigned to another clinician.')
    if target in ['Roomed','In Progress']: require(user,CLINICAL)
    elif target == 'Completed': require(user,{'admin','physician'})
    else: require(user,OPERATIONS | ({'patient'} if target=='Cancelled' else set()))
    if role(user)=='patient' and a.start <= timezone.now(): raise ValidationError('Past appointments cannot be cancelled.')
    if target not in APPOINTMENT_TRANSITIONS.get(a.status,[]): raise ValidationError(f'Cannot move {a.status} to {target}.')
    if target=='Checked In': raise ValidationError('Complete the check-in checklist first.')
    if target=='Completed' and (not hasattr(a,'encounter') or a.encounter.status not in ['Signed','Closed']): raise ValidationError('Sign the encounter before completing the visit.')
    before=a.status
    a.status=target
    a.save(update_fields=['status'])
    audit(user,'Appointment transition',a,before=before,after=target)
    return a

@transaction.atomic
def complete_checkin(user, record):
    require(user,OPERATIONS)
    a=Appointment.objects.select_for_update().get(pk=record.appointment_id)
    if a.status!='Arrived': raise ValidationError('Mark this appointment Arrived before check-in.')
    if not all([record.identity,record.demographics,record.insurance,record.consent,record.intake_forms]): raise ValidationError('Complete all five required check-in steps.')
    p=a.patient
    if not p.consent or not p.address or not p.phone: raise ValidationError('Patient registration and consent must be complete.')
    if not p.policies.filter(status='Active',expiration__gte=timezone.localdate(),effective__lte=timezone.localdate()).exists(): raise ValidationError('Verify active insurance before check-in.')
    record.completed_at=timezone.now()
    record.full_clean()
    record.save()
    if record.copay:
        Payment.objects.create(patient=p,checkin=record,amount=record.copay,source='Copay',reference=f'COPAY-{record.pk}')
    a.status='Checked In'; a.save(update_fields=['status'])
    e,_=Encounter.objects.get_or_create(appointment=a,defaults={'patient':p,'provider':a.provider,'complaint':a.reason})
    ClinicalNote.objects.get_or_create(encounter=e)
    task(p,'Complete intake','Intake','nurse',f'/encounters/{e.pk}/')
    audit(user,'Check-in completed',a,copay=str(record.copay))
    return e

@transaction.atomic
def save_note(user, encounter, data, version):
    require(user,{'admin','physician'})
    check_encounter(user,encounter)
    note=ClinicalNote.objects.select_for_update().get(encounter=encounter)
    if note.signed_at: raise ValidationError('This note is signed. Use an addendum.')
    if int(version)!=note.version: raise ValidationError('The note changed in another session. Reload before saving.')
    content={k:data.get(k,'').strip() for k in ['subjective','objective','assessment','plan']}
    NoteVersion.objects.create(note=note,author=user,version=note.version,content={k:getattr(note,k) for k in content})
    for k,v in content.items(): setattr(note,k,v)
    note.version+=1; note.save()
    encounter.status='Documentation Pending'; encounter.save(update_fields=['status'])
    task(encounter.patient,'Sign encounter note','Unsigned note','physician',f'/encounters/{encounter.pk}/')
    audit(user,'Note draft saved',note,version=note.version)
    return note

@transaction.atomic
def sign_note(user, encounter, acknowledged):
    require(user,{'admin','physician'})
    check_encounter(user,encounter)
    encounter=Encounter.objects.select_for_update().get(pk=encounter.pk)
    note=ClinicalNote.objects.select_for_update().get(encounter=encounter)
    if note.signed_at: raise ValidationError('Note already signed.')
    if not acknowledged: raise ValidationError('Confirm that you reviewed the note and orders.')
    if not all(getattr(note,k).strip() for k in ['subjective','objective','assessment','plan']): raise ValidationError('Complete all four SOAP sections.')
    if any('[' in getattr(note,k) or 'Clinician assessment required.' in getattr(note,k) for k in ['subjective','objective','assessment','plan']): raise ValidationError('Complete all template and AI review placeholders before signing.')
    if not encounter.diagnoses.exists(): raise ValidationError('Add at least one encounter diagnosis.')
    if not all([encounter.medications_reviewed,encounter.allergies_reviewed,encounter.history_reviewed]): raise ValidationError('Complete medication, allergy and history reconciliation.')
    if encounter.orders.filter(status='Draft').exists(): raise ValidationError('Sign or cancel draft orders before signing the encounter.')
    note.signed_at=timezone.now(); note.signed_by=user; note.save()
    encounter.status='Signed'; encounter.save(update_fields=['status'])
    Task.objects.filter(related_url=f'/encounters/{encounter.pk}/',category='Unsigned note',status='Open').update(status='Completed')
    task(encounter.patient,'Capture charges for signed encounter','Charge capture','coder',f'/encounters/{encounter.pk}/')
    audit(user,'Note signed',note,version=note.version)

@transaction.atomic
def order_action(user, order, target):
    require(user, {'admin','physician'} if target in ['Signed','Cancelled'] else {'admin','physician','nurse'})
    order=MedicalOrder.objects.select_for_update().get(pk=order.pk)
    check_encounter(user,order.encounter)
    allowed={'Draft':['Signed','Cancelled'],'Signed':['Processing','Cancelled'],'Processing':['Completed','Failed','Cancelled']}
    if target not in allowed.get(order.status,[]): raise ValidationError('Invalid order transition.')
    order.full_clean()
    if target=='Completed' and order.category=='Laboratory' and not hasattr(order,'result'): raise ValidationError('Enter a laboratory result first.')
    order.status=target; order.save()
    if target=='Signed': task(order.patient,'Process '+order.test,'Order','nurse',f'/records/orders/{order.pk}/')
    if target in ['Completed','Cancelled','Failed']: Task.objects.filter(related_url=f'/records/orders/{order.pk}/',category='Order').update(status='Completed')
    audit(user,'Order '+target,order)

@transaction.atomic
def result_action(user, result, target):
    require(user, {'admin','physician','nurse'} if target=='Published' else {'admin','physician'})
    result=LabResult.objects.select_for_update().get(pk=result.pk)
    check_encounter(user,result.order.encounter)
    if target=='Published' and result.status=='Entered':
        result.status='Published'
        task(result.patient,'Review '+result.order.test,'Result','physician',f'/records/results/{result.pk}/')
    elif target=='Reviewed' and result.status=='Published':
        result.status='Reviewed'; result.reviewed_by=user
        Task.objects.filter(related_url=f'/records/results/{result.pk}/',category='Result').update(status='Completed')
    elif target=='Released' and result.status=='Reviewed': result.released=True
    else: raise ValidationError('Publish, review, then release results in order.')
    result.save(); audit(user,'Result '+target,result)

def medication_warnings(med):
    warnings=[]
    if Medication.objects.filter(patient=med.patient,name__iexact=med.name,status='Active').exclude(pk=med.pk).exists(): warnings.append('An active medication with the same name already exists.')
    if med.patient.allergies.filter(substance__iexact=med.name).exists() or (med.name.lower()=='amoxicillin' and med.patient.allergies.filter(substance__iexact='Penicillin').exists()): warnings.append('Synthetic allergy rule matched. Review the recorded allergy before prescribing.')
    return warnings

def scrub(claim):
    errors=[]; warnings=[]
    e=claim.encounter; p=e.patient
    if e.status not in ['Signed','Closed']: errors.append('Encounter must be signed.')
    if not e.diagnoses.exists(): errors.append('Missing encounter diagnosis.')
    if not e.charges.exists(): errors.append('Missing procedure charges.')
    if e.charges.filter(approved=False).exists(): errors.append('All charges require coding approval.')
    if not claim.policy_id: errors.append('Missing insurance policy.')
    else:
        policy=claim.policy
        if policy.patient_id!=p.pk: errors.append('Insurance belongs to another patient.')
        if not re.fullmatch(r'[A-Z]{2}[0-9]{6,12}',policy.member_id): errors.append('Member ID must contain two uppercase letters and 6–12 digits.')
        if policy.status!='Active': errors.append('Insurance eligibility must be Active.')
        if not policy.effective <= timezone.localtime(e.created_at).date() <= policy.expiration: errors.append('Coverage does not include the service date.')
    if not p.address or not p.phone: errors.append('Incomplete patient demographics.')
    for order in e.orders.filter(authorization_required=True).exclude(status='Cancelled'):
        if not order.authorization_id or order.authorization.status!='Approved' or order.authorization.expiration<timezone.localdate(): errors.append('Missing approved, unexpired authorization for '+order.test)
    if not e.diagnoses.filter(primary=True).exists(): warnings.append('No primary diagnosis designated.')
    return errors,warnings

@transaction.atomic
def create_claim(user, encounter):
    require(user,FINANCE)
    encounter=Encounter.objects.select_for_update().get(pk=encounter.pk)
    if encounter.status not in ['Signed','Closed']: raise ValidationError('Only signed encounters can be billed.')
    claim,created=Claim.objects.get_or_create(encounter=encounter,defaults={'policy':encounter.patient.policies.filter(primary=True).first()})
    if not created: raise ValidationError('A claim already exists for this encounter.')
    if encounter.appointment_id and hasattr(encounter.appointment,'checkin'):
        payment=Payment.objects.filter(checkin=encounter.appointment.checkin,claim__isnull=True).first()
        if payment and payment.amount<=claim.balance: payment.claim=claim; payment.save()
    audit(user,'Claim created',claim)
    return claim

@transaction.atomic
def post_payment(user, claim, amount, source='Patient', reference=None):
    require(user,{'admin','billing','patient'})
    claim=Claim.objects.select_for_update().get(pk=claim.pk)
    check_patient(user,claim.patient)
    if role(user)=='patient' and source!='Patient': raise ValidationError('Only patient payments are permitted.')
    if claim.status not in ['Adjudicated','Partially Paid','Denied','Paid']: raise ValidationError('Payments require an adjudicated claim.')
    amount=Decimal(amount)
    if not amount.is_finite() or amount<=0 or amount.as_tuple().exponent < -2 or amount>claim.balance: raise ValidationError('Payment must be positive, at most two decimals, and no greater than the balance.')
    payment=Payment.objects.create(patient=claim.patient,claim=claim,amount=amount,source=source,reference=reference or 'SIM-'+uuid.uuid4().hex[:16].upper())
    claim.status='Paid' if claim.balance==0 else 'Partially Paid'; claim.save()
    audit(user,'Simulated payment posted',payment,amount=str(amount))
    return payment

@transaction.atomic
def claim_action(user, claim, action):
    require(user, {'admin','billing','coder'} if action in ['Review','Validate','Correct'] else {'admin','billing'})
    claim=Claim.objects.select_for_update().get(pk=claim.pk)
    before=claim.status
    if action=='Review' and before in ['Draft','Validation Failed']: claim.status='Ready for Review'
    elif action=='Validate' and before in ['Ready for Review','Validation Failed']:
        claim.validation_errors,claim.validation_warnings=scrub(claim)
        claim.status='Validation Failed' if claim.validation_errors else 'Validated'
    elif action=='Submit' and before=='Validated':
        errors,warnings=scrub(claim)
        if errors: raise ValidationError(errors)
        claim.status='Submitted'; claim.submitted_at=timezone.now()
    elif action=='Payer response' and before=='Submitted': claim.status='Rejected' if claim.scenario=='Reject' else 'Accepted'
    elif action=='Adjudicate' and before=='Accepted':
        claim.status='Adjudicated'; claim.save()
        if claim.scenario=='Deny':
            claim.status='Denied'
            Denial.objects.get_or_create(claim=claim,defaults={'reason':'Simulated authorization documentation missing','due_date':timezone.localdate()+timedelta(days=30)})
            task(claim.patient,'Resolve '+str(claim),'Denial','billing',f'/records/claims/{claim.pk}/')
        elif claim.balance>0:
            amount=claim.balance if claim.scenario=='Pay' else (claim.balance*Decimal('0.70')).quantize(Decimal('0.01'))
            post_payment(user,claim,amount,'Insurance')
            claim.refresh_from_db()
        else: claim.status='Paid'
    elif action=='Correct' and before in ['Denied','Rejected']:
        if hasattr(claim,'denial') and not claim.denial.appeal.strip(): raise ValidationError('Record an appeal before correcting this denial.')
        claim.status='Draft'; claim.scenario='Pay'; claim.validation_errors=[]
        if hasattr(claim,'denial'):
            claim.denial.status='Corrected'; claim.denial.save()
            Task.objects.filter(related_url=f'/records/claims/{claim.pk}/',category='Denial').update(status='Completed')
    elif action=='Close' and before=='Paid' and claim.balance==0: claim.status='Closed'
    else: raise ValidationError('Invalid claim transition.')
    claim.save(); audit(user,'Claim '+action,claim,before=before,after=claim.status)

@transaction.atomic
def verify_insurance(user, policy):
    require(user,OPERATIONS|{'billing'})
    today=timezone.localdate()
    policy.status='Inactive' if not policy.effective<=today<=policy.expiration else ('Coverage Not Found' if not policy.member_id else ('Verification Error' if policy.member_id.startswith('ERR') else 'Active'))
    policy.verified_at=timezone.now(); policy.save()
    audit(user,'Synthetic eligibility verified',policy,status=policy.status)

@transaction.atomic
def generate_ai(user, encounter, transcript):
    require(user,{'admin','physician'})
    check_encounter(user,encounter)
    if encounter.note.signed_at: raise ValidationError('Cannot draft for a signed encounter.')
    if not transcript.strip(): raise ValidationError('Enter a synthetic transcript.')
    v=encounter.vitals.order_by('-created_at').first()
    diagnoses='; '.join(str(p.code) for p in encounter.diagnoses.all())
    output={'subjective':f'Chief complaint: {encounter.complaint}\nClinician-provided transcript (unverified): {transcript.strip()}', 'objective':str(v) if v else 'No vitals recorded. Clinician review required.', 'assessment':diagnoses or 'No encounter diagnosis recorded. Clinician assessment required.', 'plan':'[Clinician to complete treatment, testing, follow-up, and patient instructions.]'}
    draft=AIDraft.objects.create(encounter=encounter,author=user,transcript=transcript,output=output)
    audit(user,'AI demo draft generated',draft,model=draft.model,prompt=draft.prompt_version)
    return draft
