import csv
import json
import uuid
from datetime import datetime,timedelta
from decimal import Decimal,InvalidOperation
from urllib.parse import urlencode
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied,ValidationError
from django.core.paginator import Paginator
from django.db import transaction,IntegrityError
from django.db.models import Q,Count,Sum
from django.http import JsonResponse,HttpResponse,Http404
from django.shortcuts import render,redirect,get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST
from core.models import *
from clinical.models import *
from revenue.models import *
from engagement.models import *
from core.access import *
from core.services import *
from core.forms import *
from core.registry import R,path_value
from core.presentation import readable, money
from engagement.messaging import unread_messages, mark_read, MESSAGE_ROLES

def error_text(exc): return ' '.join(exc.messages) if isinstance(exc,ValidationError) else str(exc)

def login_view(request):
    if request.user.is_authenticated: return redirect('dashboard')
    if request.method=='POST':
        username=request.POST.get('username','')
        user=authenticate(request,username=username,password=request.POST.get('password',''))
        if user and hasattr(user,'profile'):
            login(request,user); audit(user,'Login',user)
            return redirect('portal' if role(user)=='patient' else 'dashboard')
        messages.error(request,'Unable to sign in. Check your username and password.')
    return render(request,'login.html',{'demo_mode':settings.DEMO_MODE,'roles':ROLES})

@require_POST
@login_required
def logout_view(request):
    audit(request.user,'Logout',request.user); logout(request); return redirect('login')

def health(request):
    from django.db import connection
    with connection.cursor() as cursor: cursor.execute('SELECT 1')
    return JsonResponse({'status':'ok','application':'AthenaFlow','external_transactions':'simulated'})

def scope(request,key):
    if key not in R: raise Http404()
    spec=R[key]; require(request.user,spec.read)
    qs=spec.model.objects.all()
    if spec.patient_path=='': qs=patients_for(request.user)
    elif spec.patient_path: qs=qs.filter(**{spec.patient_path+'__in':patients_for(request.user)})
    if key=='tasks' and role(request.user)!='admin': qs=qs.filter(Q(role=role(request.user))|Q(assigned=request.user))
    if key in ['encounters','schedule'] and role(request.user)=='physician': qs=qs.filter(provider__user=request.user)
    return qs

@login_required
def message_notifications(request):
    require(request.user, MESSAGE_ROLES)
    counts = dict(unread_messages(request.user).values('thread_id').annotate(n=Count('pk')).values_list('thread_id', 'n'))
    response = JsonResponse({'count': sum(counts.values()), 'threads': counts})
    response['Cache-Control'] = 'no-store'
    return response

@login_required
@require_POST
def confirm_responsibility(request, pk):
    require(request.user, {'admin','billing'})
    with transaction.atomic():
        claim = get_object_or_404(Claim.objects.select_for_update(), pk=pk)
        check_patient(request.user, claim.patient)
        try:
            amount = Decimal(request.POST.get('amount',''))
            if not claim.can_post_payment or not amount.is_finite() or amount < 0 or amount > claim.balance or amount.as_tuple().exponent < -2:
                raise ValueError()
            claim.patient_responsibility = amount
            claim.save(update_fields=['patient_responsibility'])
            audit(request.user,'Patient responsibility confirmed',claim,amount=str(amount))
            messages.success(request,'Patient responsibility confirmed.')
        except (ValueError, InvalidOperation):
            messages.error(request,'Enter a nonnegative amount with at most two decimals, no greater than an eligible claim balance.')
    return redirect(record_url('claims',claim))

def display(value):
    if isinstance(value,bool): return 'Yes' if value else 'No'
    if value is None or value=='': return '—'
    if isinstance(value,datetime): return timezone.localtime(value).strftime('%b %d, %Y · %I:%M %p')
    if isinstance(value,Decimal): return f'{value:,.2f}'
    return readable(value)

def record_url(key,obj):
    if key=='patients': return f'/patients/{obj.pk}/'
    if key=='encounters': return f'/encounters/{obj.pk}/'
    return f'/records/{key}/{obj.pk}/'

def headers(spec):
    return [name.replace('_',' ').title() for name in spec.columns]

@login_required
def record_list(request,key):
    qs=scope(request,key); spec=R[key]
    q=request.GET.get('q','').strip()
    if q:
        condition=Q()
        for field in spec.model._meta.fields:
            if isinstance(field,(models.CharField,models.TextField)): condition |= Q(**{field.name+'__icontains':q})
        if spec.patient_path: condition |= Q(**{spec.patient_path+'__first_name__icontains':q})|Q(**{spec.patient_path+'__last_name__icontains':q})|Q(**{spec.patient_path+'__mrn__icontains':q})
        qs=qs.filter(condition)
    status=request.GET.get('status','')
    if status and any(f.name=='status' for f in spec.model._meta.fields): qs=qs.filter(status=status)
    patient=request.GET.get('patient','')
    if patient.isdigit() and spec.patient_path: qs=qs.filter(**{spec.patient_path+'_id':int(patient)})
    provider=request.GET.get('provider','')
    department=request.GET.get('department','')
    fields={f.name for f in spec.model._meta.fields}
    if provider.isdigit() and 'provider' in fields: qs=qs.filter(provider_id=provider)
    if department.isdigit() and 'provider' in fields: qs=qs.filter(provider__department_id=department)
    if key=='patients':
        if request.GET.get('dob'):
            try: qs=qs.filter(dob=datetime.strptime(request.GET['dob'],'%Y-%m-%d').date())
            except ValueError: messages.error(request,'Use YYYY-MM-DD for date of birth.')
        if request.GET.get('active') in ['true','false']: qs=qs.filter(active=request.GET['active']=='true')
    sort=request.GET.get('sort','')
    if sort.lstrip('-') in fields: qs=qs.order_by(sort)
    elif not qs.ordered: qs=qs.order_by('-pk')
    paginator=Paginator(qs.distinct(),20); page=paginator.get_page(request.GET.get('page'))
    unread_counts = dict(unread_messages(request.user).values('thread_id').annotate(n=Count('pk')).values_list('thread_id','n')) if key == 'messages' else {}
    rows=[{'obj':obj,'unread':unread_counts.get(obj.pk,0),'url':record_url(key,obj),'cells':[(money(path_value(obj,c)) if c in {'amount','copay','deductible','total','balance'} else display(path_value(obj,c))) for c in spec.columns]} for obj in page]
    statuses=spec.model.objects.values_list('status',flat=True).distinct() if 'status' in fields else []
    query=request.GET.copy(); query.pop('page',None)
    return render(request,'list.html',{'active':key,'key':key,'title':spec.title,'subtitle':'Live workqueue · changes are saved to the practice record','rows':rows,'headers':headers(spec),'columns':spec.columns,'page':page,'query':query.urlencode(),'q':q,'statuses':statuses,'status':status,'can_create':role(request.user) in spec.write and key not in ['claims','denials'],'providers':Provider.objects.all(),'sort':sort})

def validate_record(user,key,obj,creating):
    p=path_value(obj,R[key].patient_path) if R[key].patient_path else None
    if p: check_patient(user,p)
    if key in ['orders','charges','problems'] and getattr(obj,'encounter_id',None):
        if key!='charges' and role(user)!='coder': check_encounter(user,obj.encounter)
        if key=='problems' and obj.patient_id!=obj.encounter.patient_id: raise ValidationError('Diagnosis and encounter must belong to the same patient.')
        if key in ['orders','problems'] and obj.encounter.status in ['Signed','Closed']:
            existing=Problem.objects.filter(pk=obj.pk).first() if key=='problems' and obj.pk else None
            if not existing or any(getattr(existing,k)!=getattr(obj,k) for k in ['patient_id','code_id','encounter_id','primary']): raise ValidationError('Signed encounter diagnoses and orders cannot be changed. Longitudinal problem status and notes may be updated.')
    if key=='charges':
        if obj.encounter.status not in ['Signed','Closed']: raise ValidationError('Charges require a signed encounter.')
        if hasattr(obj.encounter,'claim') and obj.encounter.claim.status not in ['Draft','Ready for Review','Validation Failed','Rejected','Denied']: raise ValidationError('Charges are locked after claim validation.')
        if not obj.encounter.diagnoses.filter(code=obj.diagnosis).exists(): raise ValidationError('Charge diagnosis must be linked to this encounter.')
        if hasattr(obj.encounter,'claim'):
            claim=obj.encounter.claim
            new_total=sum((c.amount*c.units for c in obj.encounter.charges.exclude(pk=obj.pk)),Decimal(0))+obj.amount*obj.units
            if new_total<sum((p.amount for p in claim.payments.all()),Decimal(0)): raise ValidationError('Charges cannot be reduced below posted payments.')
    if key=='authorizations' and obj.policy.patient_id!=obj.patient_id: raise ValidationError('Insurance policy belongs to another patient.')
    if key=='claims' and obj.policy_id and obj.policy.patient_id!=obj.patient.pk: raise ValidationError('Insurance policy belongs to another patient.')
    if key=='results':
        check_encounter(user,obj.order.encounter)
        if obj.order.category!='Laboratory' or obj.order.status not in ['Processing','Completed']: raise ValidationError('Select a processing laboratory order.')
    if key=='tasks':
        if obj.role not in dict(ROLES) or obj.role=='patient': raise ValidationError('Select a staff role.')
        if obj.assigned_id and role(obj.assigned)!=obj.role: raise ValidationError('Assigned staff must have the selected role.')
    if key=='medications' and role(user)=='physician' and obj.provider.user_id!=user.pk: raise PermissionDenied()

def editable(key,obj):
    if key in ['claims'] and obj.status not in ['Draft','Validation Failed','Rejected','Denied','Ready for Review']: return False
    if key in ['orders','medications','authorizations'] and obj.status!='Draft': return False
    if key=='results' and obj.status!='Entered': return False
    if key=='schedule' and obj.status not in ['Scheduled','Confirmed']: return False
    if key=='denials' and obj.status!='Open': return False
    return True

@login_required
def record_edit(request,key,pk=None):
    if key not in R: raise Http404()
    spec=R[key]; require(request.user,spec.write)
    obj=get_object_or_404(scope(request,key),pk=pk) if pk else None
    if not pk and key in ['claims','denials']: raise PermissionDenied('Create this record through the related encounter or claim.')
    if obj and not editable(key,obj): raise PermissionDenied('This record is locked in its current state.')
    initial={}
    for field in ['patient','encounter','order']:
        if request.GET.get(field,'').isdigit(): initial[field]=request.GET[field]
    form=resource_form(key,request.user,request.POST or None,instance=obj,initial=initial)
    if request.method=='POST' and form.is_valid():
        try:
            with transaction.atomic():
                if obj:
                    current=spec.model.objects.select_for_update().get(pk=obj.pk)
                    if not editable(key,current): raise ValidationError('This record is now locked. Reload to view its current state.')
                saved=form.save(commit=False)
                if key == 'claims':
                    saved.status='Draft'; saved.validation_errors=[]; saved.validation_warnings=[]
                validate_record(request.user,key,saved,not pk)
                if key=='schedule':
                    old=Appointment.objects.get(pk=pk) if pk else None
                    save_appointment(request.user,saved)
                    if old and old.start!=saved.start: audit(request.user,'Appointment rescheduled',saved,old_start=old.start.isoformat(),new_start=saved.start.isoformat())
                else:
                    saved.full_clean(); saved.save(); audit(request.user,'Record updated' if pk else 'Record created',saved)
                if key == 'messages' and not pk:
                    msg = Message.objects.create(thread=saved, sender=request.user, body=form.cleaned_data['body'])
                    audit(request.user,'Message sent',msg)
                    if role(request.user) == 'patient': task(saved.patient,'Reply: '+saved.subject,'Message','nurse',record_url('messages',saved))
                if key=='results': order_action(request.user,saved.order,'Completed') if saved.order.status=='Processing' else None
            messages.success(request,'Record saved successfully.')
            return redirect(record_url(key,saved))
        except (ValidationError,IntegrityError) as exc:
            form.add_error(None,error_text(exc) if isinstance(exc,ValidationError) else 'This record conflicts with an existing record. Reload and try again.')
    return render(request,'form.html',{'active':key,'title':('Edit ' if pk else 'New ')+spec.title,'form':form,'back':record_url(key,obj) if obj else f'/records/{key}/','submit_label':'Send message' if key == 'messages' and not pk else 'Save changes','hint':'All changes persist. Use fictional information only.'})

def actions_for(key,obj,user):
    r=role(user); acts=[]
    if key=='schedule':
        for target in APPOINTMENT_TRANSITIONS.get(obj.status,[]):
            if target=='Checked In': continue
            if (target == 'Roomed' and r in CLINICAL) or (target == 'In Progress' and r in {'admin','physician'}) or (target=='Completed' and r in {'admin','physician'}) or (target not in ['Roomed','In Progress','Completed'] and r in OPERATIONS): acts.append(target)
    elif key=='insurance' and r in OPERATIONS|{'billing'}: acts=['Verify eligibility']
    elif key=='orders':
        options={'Draft':['Signed','Cancelled'],'Signed':['Processing','Cancelled'],'Processing':['Completed','Failed','Cancelled']}.get(obj.status,[])
        acts=[a for a in options if r in ({'admin','physician'} if a in ['Signed','Cancelled'] else {'admin','physician','nurse'})]
    elif key=='results':
        if obj.status=='Entered' and r in {'admin','physician','nurse'}: acts=['Published']
        if obj.status=='Published' and r in {'admin','physician'}: acts=['Reviewed']
        if obj.status=='Reviewed' and not obj.released and r in {'admin','physician'}: acts=['Released']
    elif key=='medications' and r in {'admin','physician'}: acts={'Draft':['Sign prescription'],'Active':['Discontinue']}.get(obj.status,[])
    elif key=='charges' and not obj.approved and r in {'admin','coder','billing'}: acts=['Approve charge']
    elif key=='claims':
        options={'Draft':['Review'],'Ready for Review':['Validate'],'Validation Failed':['Validate'],'Validated':['Submit'],'Submitted':['Payer response'],'Accepted':['Adjudicate'],'Denied':['Correct'],'Rejected':['Correct'],'Paid':['Close']}.get(obj.status,[])
        acts=[a for a in options if r in ({'admin','billing','coder'} if a in ['Review','Validate','Correct'] else {'admin','billing'})]
    elif key=='authorizations' and r in {'admin','physician','billing'}: acts={'Draft':['Submit authorization'],'Submitted':['Pending Review'],'Pending Review':['Approve authorization','Deny authorization','Request information'],'Additional Information Requested':['Submit authorization']}.get(obj.status,[])
    elif key=='tasks' and obj.status=='Open': acts=['Complete task']
    elif key=='waitlist' and obj.status=='Waiting': acts=['Find & book slot']
    return acts

@login_required
def record_detail(request,key,pk):
    obj=get_object_or_404(scope(request,key),pk=pk); spec=R[key]
    if key=='patients': return patient_chart(request,pk)
    if key=='encounters': return encounter_view(request,pk)
    if key=='messages': return message_detail(request,obj)
    fields=[(field.verbose_name.title(),(money(getattr(obj,field.name)) if field.name in {'amount','copay','deductible','patient_responsibility'} else display(getattr(obj,field.name)))) for field in obj._meta.fields if field.name!='id']
    if key == 'claims':
        checked = obj.status not in ['Draft','Ready for Review']
        fields = [(label, ('Not yet validated' if not checked else readable(obj.validation_errors) if obj.validation_errors else 'No validation errors') if label == 'Validation Errors' else ('Not yet validated' if not checked else readable(obj.validation_warnings) if obj.validation_warnings else 'No validation warnings') if label == 'Validation Warnings' else value) for label,value in fields]
    extras={}
    if key=='claims': extras.update(total=obj.total,balance=obj.balance,payments=obj.payments.all(),errors=obj.validation_errors,warnings=obj.validation_warnings)
    if key=='medications': extras['warnings']=medication_warnings(obj)
    if key=='waitlist': extras['hint']='Find & book slot checks weekdays and provider conflicts within the requested dates. Notification is recorded as a simulated task.'
    return render(request,'detail.html',{'active':key,'title':str(obj),'subtitle':spec.title,'key':key,'obj':obj,'fields':fields,'actions':actions_for(key,obj,request.user),'can_edit':role(request.user) in spec.write and editable(key,obj),'extras':extras,'events':AuditEvent.objects.filter(entity=obj._meta.label,object_id=str(obj.pk))[:20]})

@login_required
@require_POST
def record_action(request,key,pk):
    obj=get_object_or_404(scope(request,key),pk=pk)
    action=request.POST.get('action','')
    if action not in actions_for(key,obj,request.user): raise PermissionDenied('Action is not available for this role and state.')
    try:
        with transaction.atomic():
            obj=R[key].model.objects.select_for_update().get(pk=pk)
            if action not in actions_for(key,obj,request.user): raise ValidationError('The record has changed. Reload and retry.')
            if key=='schedule': transition_appointment(request.user,pk,action)
            elif key=='insurance': verify_insurance(request.user,obj)
            elif key=='orders': order_action(request.user,obj,action)
            elif key=='results': result_action(request.user,obj,action,request.POST.get('comment') if action=='Reviewed' else None)
            elif key=='claims': claim_action(request.user,obj,action)
            elif key=='medications':
                check_patient(request.user,obj.patient)
                if role(request.user)=='physician' and obj.provider.user_id!=request.user.pk: raise PermissionDenied()
                if action=='Sign prescription':
                    if medication_warnings(obj) and request.POST.get('acknowledge')!='on': raise ValidationError('Acknowledge the medication warnings before signing.')
                    obj.status='Active'; obj.signed_at=timezone.now()
                else: obj.status='Discontinued'; obj.end_date=timezone.localdate()
                obj.save(); audit(request.user,action,obj)
            elif key=='charges':
                validate_record(request.user,key,obj,False)
                obj.approved=True; obj.save(); audit(request.user,action,obj)
            elif key=='authorizations':
                if obj.expiration<timezone.localdate(): raise ValidationError('Authorization expiration is in the past.')
                mapping={'Submit authorization':'Submitted','Pending Review':'Pending Review','Approve authorization':'Approved','Deny authorization':'Denied','Request information':'Additional Information Requested'}
                if action=='Submit authorization':
                    if not obj.supporting_notes.strip(): raise ValidationError('Supporting documentation is required.')
                    obj.submitted_at=timezone.now()
                obj.status=mapping[action]; obj.save(); audit(request.user,action,obj)
            elif key=='tasks':
                obj.status='Completed'; obj.save(); audit(request.user,action,obj)
            elif key=='waitlist':
                require(request.user,OPERATIONS)
                Provider.objects.select_for_update().get(pk=obj.provider_id)
                chosen=None; date=max(obj.earliest,timezone.localdate())
                search_end=min(obj.latest,date+timedelta(days=90))
                while date<=search_end:
                    if date.weekday()<5:
                        for minute in range(obj.provider.start_hour*60,obj.provider.end_hour*60,30):
                            start=timezone.make_aware(datetime.combine(date,datetime.min.time()))+timedelta(minutes=minute)
                            if start<=timezone.now(): continue
                            a=Appointment(patient=obj.patient,provider=obj.provider,department=obj.provider.department,appointment_type=AppointmentType.objects.first(),start=start,duration=30,reason=obj.reason)
                            try: a.full_clean()
                            except ValidationError: continue
                            chosen=a; break
                    if chosen: break
                    date+=timedelta(days=1)
                if not chosen: raise ValidationError('No available slot in the requested range. Change the date range and retry.')
                save_appointment(request.user,chosen)
                obj.appointment=chosen; obj.status='Booked'; obj.save()
                task(obj.patient,'Simulated waitlist booking notification','Notification','frontdesk',f'/records/schedule/{chosen.pk}/')
                audit(request.user,action,obj,appointment=chosen.pk)
        messages.success(request,f'{action} completed. Changes saved.')
    except (ValidationError,InvalidOperation) as exc:
        messages.error(request,error_text(exc)); audit(request.user,'Validation failed',obj,action_requested=action)
    return redirect(record_url(key,obj))

@login_required
def dashboard(request):
    r=role(request.user)
    if r=='patient': return redirect('portal')
    ps=patients_for(request.user)
    apps=Appointment.objects.filter(patient__in=ps,start__date=timezone.localdate()).select_related('patient','provider','appointment_type')
    if r=='physician': apps=apps.filter(provider__user=request.user)
    department=request.GET.get('department','')
    if department.isdigit(): apps=apps.filter(department_id=department)
    encounters=Encounter.objects.filter(patient__in=ps)
    tasks=scope(request,'tasks').filter(status='Open')
    if r in {'billing','coder','manager'}:
        claims=Claim.objects.all(); balance=sum((c.balance for c in claims),Decimal(0))
        metrics=[('Open claims',claims.exclude(status__in=['Paid','Closed']).count(),'Revenue cycle'),('Denied claims',claims.filter(status='Denied').count(),'Requires resolution'),('Outstanding',f'${balance:,.0f}','Simulated account balances'),('Workqueue',tasks.count(),'Open tasks')]
    else:
        metrics=[("Today's visits",apps.count(),'Across your care team'),('Patients waiting',apps.filter(status__in=['Arrived','Checked In']).count(),'Ready for the next step'),('Unsigned notes',encounters.exclude(status__in=['Signed','Closed']).count(),'Documentation in progress'),('Open tasks',tasks.count(),'Your clinical workqueue')]
    distribution=list(apps.values('status').annotate(count=Count('id')))
    for row in distribution: row['width']=round(row['count']/max(apps.count(),1)*100)
    return render(request,'dashboard.html',{'active':'dashboard','title':'Practice overview','subtitle':timezone.localdate().strftime('%A, %B %d, %Y'),'metrics':metrics,'appointments':apps[:12],'tasks':tasks[:6],'distribution':distribution,'total_visits':apps.count(),'patient_count':ps.count(),'recent_events':AuditEvent.objects.filter(actor=request.user)[:5]})

@login_required
def schedule(request):
    require(request.user,OPERATIONS|CLINICAL)
    try: day=datetime.strptime(request.GET.get('date',str(timezone.localdate())),'%Y-%m-%d').date()
    except ValueError: day=timezone.localdate()
    view=request.GET.get('view','day')
    first=day-timedelta(days=day.weekday()) if view=='week' else day
    last=first+timedelta(days=6) if view=='week' else first
    qs=scope(request,'schedule').filter(start__date__range=[first,last]).select_related('patient','provider','department','appointment_type')
    provider=request.GET.get('provider',''); department=request.GET.get('department','')
    if provider.isdigit(): qs=qs.filter(provider_id=provider)
    if department.isdigit(): qs=qs.filter(department_id=department)
    columns=[]
    if view=='week':
        for offset in range(7):
            d=first+timedelta(days=offset); columns.append({'label':d.strftime('%a %b %d'),'appointments':[a for a in qs if timezone.localtime(a.start).date()==d]})
    elif view=='department':
        for d in Department.objects.all(): columns.append({'label':d.name,'appointments':[a for a in qs if a.department_id==d.pk]})
    else:
        providers=Provider.objects.filter(active=True)
        if provider.isdigit(): providers=providers.filter(pk=provider)
        if department.isdigit(): providers=providers.filter(department_id=department)
        for p in providers: columns.append({'label':p.name,'appointments':[a for a in qs if a.provider_id==p.pk]})
    return render(request,'schedule.html',{'active':'schedule','title':'Schedule','subtitle':'Coordinate the day. Keep care moving.','day':day,'prev':day-timedelta(days=7 if view=='week' else 1),'next':day+timedelta(days=7 if view=='week' else 1),'columns':columns,'view':view,'providers':Provider.objects.all(),'can_book':role(request.user) in OPERATIONS,'count':qs.count(),'requests_count':AppointmentRequest.objects.filter(status='Requested').count()})

@login_required
def checkin(request,pk):
    require(request.user,OPERATIONS)
    a=get_object_or_404(scope(request,'schedule'),pk=pk)
    existing=CheckIn.objects.filter(appointment=a).first()
    if existing and existing.completed_at:
        messages.info(request,'Check-in is already complete.'); return redirect(record_url('schedule',a))
    form=CheckInForm(request.POST or None,instance=existing)
    if request.method=='POST' and form.is_valid():
        try:
            rec=form.save(commit=False); rec.appointment=a
            e=complete_checkin(request.user,rec)
            messages.success(request,'Checked in. The patient is now on the clinical intake worklist.')
            return redirect(record_url('schedule',a))
        except ValidationError as exc: form.add_error(None,error_text(exc))
    return render(request,'form.html',{'active':'schedule','title':'Check in · '+str(a.patient),'form':form,'hint':'Verify active coverage and registration consent before completing all checklist steps. Copays are simulated and credited to the visit claim.','back':record_url('schedule',a)})

@login_required
def patient_chart(request,pk):
    p=get_object_or_404(patients_for(request.user),pk=pk)
    require(request.user,CLINICAL|FINANCE|OPERATIONS)
    tabs=['Summary','Encounters','Problems','Medications','Allergies','Medical','Surgical','Family','Social','Vitals','Orders','Results','Documents','Immunizations','Appointments','Billing']
    clinical=role(request.user) in CLINICAL
    if not clinical: tabs=['Summary','Appointments','Billing'] if role(request.user) in FINANCE|OPERATIONS else ['Summary']
    tab=request.GET.get('tab','Summary')
    if tab not in tabs: raise PermissionDenied()
    sections=[]
    mapping={'Encounters':('encounters',p.encounters.all()),'Problems':('problems',p.problems.all()),'Medications':('medications',p.medications.all()),'Allergies':('allergies',p.allergies.all()),'Orders':('orders',MedicalOrder.objects.filter(encounter__patient=p)),'Results':('results',LabResult.objects.filter(order__encounter__patient=p)),'Appointments':('schedule',p.appointments.all()),'Billing':('claims',Claim.objects.filter(encounter__patient=p))}
    if tab=='Summary' and clinical:
        for name in ['Problems','Medications','Allergies']:
            key,qs=mapping[name]; sections.append({'title':name,'items':[{'label':str(x),'url':record_url(key,x)} for x in qs[:6]],'add':f'/records/{key}/new/?patient={p.pk}' if role(request.user) in R[key].write else None})
    elif tab in mapping:
        key,qs=mapping[tab]
        if key=='claims' and role(request.user) not in FINANCE: qs=Claim.objects.none()
        sections=[{'title':tab,'items':[{'label':str(x)+' · '+str(getattr(x,'status','')),'url':record_url(key,x)} for x in qs], 'add':f'/records/{key}/new/?patient={p.pk}' if role(request.user) in R[key].write and key!='claims' else None}]
    elif tab=='Vitals': sections=[{'title':'Vitals','items':[{'label':str(v)+' · '+display(v.created_at),'url':f'/encounters/{v.encounter_id}/'} for v in VitalSign.objects.filter(encounter__patient=p)]}]
    elif tab in ['Medical','Surgical','Family','Social','Documents','Immunizations']:
        cat={'Documents':'Document','Immunizations':'Immunization'}.get(tab,tab)
        sections=[{'title':tab,'items':[{'label':f'{x.title} · {x.detail}','url':record_url('history',x)} for x in p.history.filter(category=cat)],'add':f'/records/history/new/?patient={p.pk}'}]
    return render(request,'patient.html',{'active':'patients','title':str(p),'subtitle':p.mrn,'patient':p,'tabs':tabs,'tab':tab,'sections':sections,'clinical_access':clinical,'latest_vitals':VitalSign.objects.filter(encounter__patient=p).order_by('-created_at').first() if clinical else None,'policies':p.policies.all(),'can_edit':role(request.user) in OPERATIONS,'can_insurance':role(request.user) in R['insurance'].read})

@login_required
def encounter_view(request,pk):
    e=get_object_or_404(scope(request,'encounters'),pk=pk)
    if role(request.user) in FINANCE and role(request.user) not in CLINICAL:
        return render(request,'coding.html',{'active':'charges','title':str(e),'encounter':e,'charges':e.charges.all(),'can_charge':role(request.user) in R['charges'].write})
    check_encounter(request.user,e)
    note=e.note
    form=NoteForm(initial={k:getattr(note,k) for k in ['subjective','objective','assessment','plan','version']})
    if request.method=='POST':
        action=request.POST.get('action')
        try:
            if action=='Save draft':
                form=NoteForm(request.POST)
                if form.is_valid(): save_note(request.user,e,form.cleaned_data,form.cleaned_data['version'])
                else: raise ValidationError('Review the note fields.')
            elif action=='Sign note': sign_note(request.user,e,request.POST.get('acknowledge')=='on')
            elif action=='Add addendum':
                require(request.user,{'admin','physician'})
                if not note.signed_at or not request.POST.get('text','').strip(): raise ValidationError('Signed note and addendum text are required.')
                with transaction.atomic():
                    ad=Addendum.objects.create(note=note,author=request.user,text=request.POST['text'].strip()); audit(request.user,'Addendum signed',ad)
            elif action=='Close encounter':
                require(request.user,{'admin','physician'})
                if e.status!='Signed': raise ValidationError('Sign the encounter first.')
                with transaction.atomic():
                    e.status='Closed'; e.save(); audit(request.user,'Encounter closed',e)
                    if e.appointment_id and e.appointment.status=='In Progress': transition_appointment(request.user,e.appointment_id,'Completed')
            elif action=='Generate draft':
                generate_ai(request.user,e,request.POST.get('transcript',''))
            elif action=='Approve AI draft':
                require(request.user,{'admin','physician'})
                draft=get_object_or_404(AIDraft,pk=request.POST.get('draft'),encounter=e,status='Unreviewed')
                if request.POST.get('acknowledge')!='on': raise ValidationError('Confirm review before applying the draft.')
                with transaction.atomic():
                    save_note(request.user,e,draft.output,request.POST.get('version',0))
                    draft.status='Approved'; draft.save()
                    e.note.refresh_from_db(); e.note.provenance=f'Deterministic AI draft #{draft.pk}; reviewed by {request.user.username}'; e.note.save()
                    audit(request.user,'AI draft approved',draft)
            elif action=='Copy forward':
                require(request.user,{'admin','physician'})
                previous=ClinicalNote.objects.filter(encounter__patient=e.patient,signed_at__isnull=False).exclude(encounter=e).order_by('-signed_at').first()
                if not previous: raise ValidationError('No signed prior note exists.')
                with transaction.atomic():
                    new=save_note(request.user,e,{k:getattr(previous,k) for k in ['subjective','objective','assessment','plan']},request.POST.get('version',0))
                    new.provenance=f'Copied from note #{previous.pk} v{previous.version}; requires review'; new.save(); audit(request.user,'Note copied forward',new,source_note=previous.pk)
            else: raise ValidationError('Unknown action.')
            messages.success(request,action+' completed.')
            return redirect('encounter',pk=pk)
        except (ValidationError,ValueError) as exc: messages.error(request,error_text(exc))
    return render(request,'encounter.html',{'active':'encounters','title':str(e),'encounter':e,'patient':e.patient,'note':note,'form':form,'vitals':e.vitals.order_by('-created_at').first(),'problems':e.diagnoses.select_related('code'),'orders':e.orders.all(),'can_document':role(request.user) in {'admin','physician'},'ai_draft':e.ai_drafts.filter(status='Unreviewed').order_by('-created_at').first(),'versions':note.versions.order_by('-version')})

@login_required
def intake(request,pk):
    require(request.user,CLINICAL)
    e=get_object_or_404(scope(request,'encounters'),pk=pk); check_encounter(request.user,e)
    if e.status in ['Signed','Closed']: raise PermissionDenied('The encounter is signed.')
    form=IntakeForm(request.POST or None,instance=e)
    vitals=VitalForm(request.POST or None)
    if request.method=='POST' and form.is_valid() and vitals.is_valid():
        with transaction.atomic():
            form.save(); v=vitals.save(commit=False); v.encounter=e; v.author=request.user; v.save()
            Task.objects.filter(related_url=f'/encounters/{e.pk}/',category='Intake').update(status='Completed')
            audit(request.user,'Intake and vitals recorded',e)
        messages.success(request,'Intake and vital signs saved to the chart.'); return redirect('encounter',pk=pk)
    return render(request,'form.html',{'active':'encounters','title':'Clinical intake · '+str(e.patient),'form':form,'form2':vitals,'back':f'/encounters/{pk}/','hint':'Height defaults to inches and weight to pounds. Select cm or kg when needed; changing units converts the value. BMI is calculated automatically.'})

@login_required
@require_POST
def bill_encounter(request,pk):
    require(request.user,FINANCE)
    e=get_object_or_404(scope(request,'encounters'),pk=pk)
    try:
        claim=create_claim(request.user,e); messages.success(request,'Claim created from this encounter.'); return redirect(record_url('claims',claim))
    except ValidationError as exc: messages.error(request,error_text(exc)); return redirect('encounter',pk=pk)

@login_required
def payment_view(request,pk):
    require(request.user,{'admin','billing','patient'})
    claim=get_object_or_404(Claim,pk=pk,encounter__patient__in=patients_for(request.user))
    if not claim.can_post_payment or (role(request.user)=='patient' and not claim.can_patient_pay):
        raise PermissionDenied('No payment is available. Billing must confirm patient responsibility, and the claim must have an eligible outstanding balance.')
    token_key=f'payment-token-{pk}'
    if token_key not in request.session: request.session[token_key]=uuid.uuid4().hex
    form=PaymentForm(request.POST or None,initial={'amount':claim.patient_due if role(request.user)=='patient' else claim.balance,'source':'Patient','token':request.session[token_key]})
    if role(request.user)=='patient': form.fields['source'].choices=[('Patient','Patient')]
    if request.method=='POST' and form.is_valid():
        try:
            if form.cleaned_data['token']!=request.session[token_key]: raise ValidationError('Payment form expired. Reload before paying.')
            reference='SIM-'+form.cleaned_data['token'].upper()
            with transaction.atomic():
                if Payment.objects.filter(reference=reference).exists(): raise ValidationError('This payment has already been posted.')
                payment=post_payment(request.user,claim,form.cleaned_data['amount'],form.cleaned_data['source'],reference)
            del request.session[token_key]
            messages.success(request,'Simulated payment posted. No money was transferred.')
            return redirect('receipt',pk=payment.pk)
        except ValidationError as exc: form.add_error(None,error_text(exc))
    return render(request,'form.html',{'active':'claims','title':f'Simulated payment · {claim}','form':form,'hint':f'Outstanding balance: ${claim.balance}. No card details are collected.','back':'/portal/' if role(request.user)=='patient' else record_url('claims',claim)})

@login_required
def receipt(request,pk):
    require(request.user,FINANCE|{'frontdesk','patient'})
    payment=get_object_or_404(Payment,pk=pk,patient__in=patients_for(request.user))
    return render(request,'receipt.html',{'title':'Payment receipt','payment':payment})

@login_required
def message_detail(request,thread):
    check_patient(request.user,thread.patient)
    if request.method=='POST':
        text=request.POST.get('body','').strip()
        if not text: messages.error(request,'Enter a message before sending.')
        elif len(text)>10000: messages.error(request,'Messages must be at most 10,000 characters.')
        else:
            with transaction.atomic():
                msg=Message.objects.create(thread=thread,sender=request.user,body=text)
                audit(request.user,'Message sent',msg)
                if role(request.user)=='patient': task(thread.patient,'Reply: '+thread.subject,'Message','nurse',record_url('messages',thread))
                else: Task.objects.filter(related_url=record_url('messages',thread),category='Message').update(status='Completed')
            messages.success(request,'Message sent.'); return redirect(record_url('messages',thread))
    displayed = list(thread.messages.select_related('sender'))
    mark_read(request.user, displayed)
    return render(request,'messages.html',{'active':'messages','title':thread.subject,'thread':thread,'thread_messages':displayed})

@login_required
def portal(request):
    require(request.user,{'patient'})
    p=get_object_or_404(Patient,user=request.user)
    if request.method=='POST':
        action=request.POST.get('action')
        try:
            with transaction.atomic():
                if action=='Request appointment':
                    preferred=datetime.strptime(request.POST.get('date',''),'%Y-%m-%d').date()
                    if preferred<timezone.localdate(): raise ValidationError('Choose a future date.')
                    reason=request.POST.get('reason','').strip()
                    if not reason or len(reason)>250: raise ValidationError('Enter a reason of at most 250 characters.')
                    obj=AppointmentRequest.objects.create(patient=p,preferred_date=preferred,reason=reason)
                    task(p,'Book patient appointment request','Appointment request','frontdesk',f'/records/requests/{obj.pk}/'); audit(request.user,action,obj)
                elif action=='Cancel appointment': transition_appointment(request.user,get_object_or_404(Appointment,pk=request.POST.get('id'),patient=p).pk,'Cancelled')
                elif action=='Renew medication':
                    med=get_object_or_404(Medication,pk=request.POST.get('id'),patient=p,status='Active')
                    obj=task(p,'Renewal requested: '+med.name,'Medication renewal','physician',record_url('medications',med)); audit(request.user,action,obj)
                elif action=='Update information':
                    p.phone=request.POST.get('phone',''); p.email=request.POST.get('email',''); p.address=request.POST.get('address',''); p.full_clean(); p.save(); audit(request.user,action,p)
                elif action=='Pre-check-in':
                    a=get_object_or_404(Appointment,pk=request.POST.get('id'),patient=p,status__in=['Scheduled','Confirmed'])
                    if request.POST.get('consent')!='on': raise ValidationError('Confirm the consent statement.')
                    p.consent=True; p.save(); c,_=CheckIn.objects.get_or_create(appointment=a); c.demographics=True; c.consent=True; c.save(); audit(request.user,action,c)
                else: raise ValidationError('Unknown portal action.')
            messages.success(request,action+' saved.'); return redirect('portal')
        except (ValidationError,ValueError) as exc: messages.error(request,error_text(exc))
    claims=Claim.objects.filter(encounter__patient=p)
    return render(request,'portal.html',{'active':'portal','title':'Your health, in one place','patient':p,'appointments':p.appointments.filter(start__gte=timezone.now()).exclude(status__in=['Cancelled','No Show'])[:8],'results':LabResult.objects.filter(order__encounter__patient=p,released=True,status='Reviewed'),'medications':p.medications.filter(status='Active'),'notes':ClinicalNote.objects.filter(encounter__patient=p,signed_at__isnull=False),'claims':claims,'balance':sum((c.balance for c in claims),Decimal(0)),'payments':p.payments.all(),'requests':AppointmentRequest.objects.filter(patient=p),'unread':unread_messages(request.user).count()})

@login_required
def request_booking(request,pk):
    require(request.user,OPERATIONS)
    req=get_object_or_404(AppointmentRequest,pk=pk)
    if req.status!='Requested': raise PermissionDenied('Request already booked.')
    initial={'patient':req.patient,'provider':req.patient.provider,'department':req.patient.provider.department,'reason':req.reason,'start':f'{req.preferred_date}T09:00','duration':30,'appointment_type':AppointmentType.objects.first()}
    form=resource_form('schedule',request.user,request.POST or None,initial=initial)
    if request.method=='POST' and form.is_valid():
        try:
            with transaction.atomic():
                req=AppointmentRequest.objects.select_for_update().get(pk=pk)
                if req.status!='Requested': raise ValidationError('This request has already been booked.')
                a=form.save(commit=False)
                if a.patient_id!=req.patient_id: raise ValidationError('Patient must match the request.')
                save_appointment(request.user,a); req.appointment=a; req.status='Booked'; req.save()
                Task.objects.filter(related_url=f'/records/requests/{pk}/').update(status='Completed'); audit(request.user,'Appointment request booked',req)
            messages.success(request,'Appointment booked and request completed.'); return redirect(record_url('schedule',a))
        except ValidationError as exc: form.add_error(None,error_text(exc))
    return render(request,'form.html',{'active':'schedule','title':'Book requested appointment','form':form,'back':f'/records/requests/{pk}/'})

@login_required
def ai_page(request):
    require(request.user,{'admin','physician'})
    ps=patients_for(request.user)
    p=ps.filter(pk=request.GET.get('patient')).first() if request.GET.get('patient','').isdigit() else ps.first()
    facts=[]; suggestions=[]
    if p:
        facts=[
            ('Demographics',f'{p}, age {p.age}, {p.sex}; {p.mrn}'),
            ('Active problems','; '.join(str(x) for x in p.problems.filter(status='Active')) or 'None recorded'),
            ('Current medications','; '.join(str(x) for x in p.medications.filter(status='Active')) or 'None recorded'),
            ('Allergies','; '.join(str(x) for x in p.allergies.all()) or 'No allergies recorded (not an assertion of no known allergies)'),
            ('Recent encounters','; '.join(str(x) for x in p.encounters.all()[:3])),
            ('Recent results','; '.join(str(x) for x in LabResult.objects.filter(order__encounter__patient=p).order_by('-created_at')[:3])),
            ('Pending orders','; '.join(str(x) for x in MedicalOrder.objects.filter(encounter__patient=p).exclude(status__in=['Completed','Cancelled','Failed'])) or 'None'),
        ]
        if p.encounters.exclude(status__in=['Signed','Closed']).exists(): suggestions.append('Review outstanding encounter documentation.')
        if not p.allergies.exists(): suggestions.append('Confirm allergy history with the patient.')
        if LabResult.objects.filter(order__encounter__patient=p,status='Published').exists(): suggestions.append('Review published results in the results workqueue.')
    return render(request,'ai.html',{'active':'ai','title':'Clinical assistant','patients':ps,'patient':p,'facts':facts,'suggestions':suggestions,'encounters':p.encounters.exclude(status__in=['Signed','Closed']) if p else []})

@login_required
def reports(request):
    require(request.user,FINANCE)
    apps=Appointment.objects.all(); encounters=Encounter.objects.all(); claims=Claim.objects.all(); payments=Payment.objects.all()
    try:
        start=datetime.strptime(request.GET.get('start',str(timezone.localdate()-timedelta(days=30))),'%Y-%m-%d').date()
        end=datetime.strptime(request.GET.get('end',str(timezone.localdate())),'%Y-%m-%d').date()
        if end<start: raise ValueError()
    except ValueError:
        messages.error(request,'Invalid reporting date range. Showing the last 30 days.'); start=timezone.localdate()-timedelta(days=30); end=timezone.localdate()
    apps=apps.filter(start__date__range=[start,end]); encounters=encounters.filter(created_at__date__range=[start,end]); claims=claims.filter(encounter__in=encounters); payments=payments.filter(created_at__date__range=[start,end])
    for field in ['provider','department']:
        value=request.GET.get(field,'')
        if value.isdigit():
            lookup='provider_id' if field=='provider' else 'provider__department_id'
            apps=apps.filter(**{lookup:value}); encounters=encounters.filter(**{lookup:value}); claims=claims.filter(encounter__in=encounters); payments=payments.filter(claim__encounter__in=encounters)
    total=sum((c.total for c in claims),Decimal(0)); balance=sum((c.balance for c in claims),Decimal(0)); paid=payments.aggregate(s=Sum('amount'))['s'] or 0
    denial_rate=round(claims.filter(status='Denied').count()/max(claims.count(),1)*100,1)
    submitted=claims.exclude(submitted_at=None)
    accepted=submitted.filter(status__in=['Accepted','Adjudicated','Paid','Closed','Partially Paid','Denied'])
    metrics=[('Appointments',apps.count()),('No-show rate',f'{apps.filter(status="No Show").count()/max(apps.count(),1)*100:.1f}%'),('Encounters',encounters.count()),('Completion rate',f'{encounters.filter(status__in=["Signed","Closed"]).count()/max(encounters.count(),1)*100:.1f}%'),('Total charges',f'${total:,.2f}'),('Simulated payments',f'${paid:,.2f}'),('Outstanding',f'${balance:,.2f}'),('Denial rate',f'{denial_rate}%'),('Unsigned notes',encounters.exclude(status__in=['Signed','Closed']).count()),('Results awaiting review',LabResult.objects.filter(order__encounter__in=encounters,status='Published').count()),('Claims submitted',submitted.count()),('Acceptance rate',f'{accepted.count()/max(submitted.count(),1)*100:.1f}%')]
    aging={x:Decimal(0) for x in ['0–30 days','31–60 days','61–90 days','90+ days']}
    for c in claims:
        days=(timezone.localdate()-c.created_at.date()).days
        bucket='0–30 days' if days<=30 else '31–60 days' if days<=60 else '61–90 days' if days<=90 else '90+ days'
        aging[bucket]+=c.balance
    distribution=list(apps.values('status').annotate(count=Count('pk')))
    for row in distribution: row['width']=round(row['count']/max(apps.count(),1)*100)
    if request.GET.get('export')=='csv':
        response=HttpResponse(content_type='text/csv'); response['Content-Disposition']='attachment; filename="athenaflow-report.csv"'
        writer=csv.writer(response); writer.writerow(['Metric','Value','Start','End'])
        for name,val in metrics+[(label,money(value)) for label,value in aging.items()]: writer.writerow([name,val,start,end])
        audit(request.user,'Report exported',request.user); return response
    query=request.GET.copy(); query['export']='csv'
    weekdays=sum(1 for offset in range((end-start).days+1) if (start+timedelta(days=offset)).weekday()<5)
    utilization=[]
    report_providers=Provider.objects.filter(active=True)
    if request.GET.get('provider','').isdigit(): report_providers=report_providers.filter(pk=request.GET['provider'])
    if request.GET.get('department','').isdigit(): report_providers=report_providers.filter(department_id=request.GET['department'])
    for provider in report_providers:
        minutes=apps.filter(provider=provider).exclude(status__in=['Cancelled','No Show','Rescheduled']).aggregate(total=Sum('duration'))['total'] or 0
        available=weekdays*(provider.end_hour-provider.start_hour)*60
        utilization.append({'provider':provider,'minutes':minutes,'percent':round(minutes/max(available,1)*100,1)})
    from django.db.models.functions import TruncDate
    trend=list(payments.annotate(day=TruncDate('created_at')).values('day').annotate(amount=Sum('amount')).order_by('day'))
    max_amount=max((row['amount'] for row in trend),default=Decimal(1))
    for row in trend: row['width']=round(row['amount']/max(max_amount,1)*100)
    return render(request,'reports.html',{'active':'reports','title':'Practice analytics','subtitle':'Calculated from your practice records','metrics':metrics,'aging':aging.items(),'distribution':distribution,'utilization':utilization,'trend':trend,'start':start,'end':end,'providers':Provider.objects.all(),'export_query':query.urlencode(),'diagnoses':Problem.objects.filter(encounter__in=encounters).values('code__description').annotate(count=Count('pk')).order_by('-count')[:6]})

@login_required
def administration(request):
    require(request.user,{'admin'})
    return render(request,'administration.html',{'active':'administration','title':'Practice administration','staff':Profile.objects.select_related('user','department').exclude(role='patient'),'reset_allowed':settings.ALLOW_DEMO_RESET})

@login_required
def staff_edit(request,pk=None):
    require(request.user,{'admin'})
    user=get_object_or_404(User,pk=pk) if pk else None
    if user and role(user)=='patient': raise PermissionDenied('Patient accounts are managed through registration.')
    initial={'username':user.username,'first_name':user.first_name,'last_name':user.last_name,'role':user.profile.role,'department':user.profile.department,'is_active':user.is_active} if user else None
    form=StaffForm(request.POST or None,initial=initial)
    if request.method=='POST' and form.is_valid():
        d=form.cleaned_data
        if not user and not d['password']: form.add_error('password','Password required for a new account.')
        elif user and user.pk==request.user.pk and (not d['is_active'] or d['role']!='admin'): form.add_error(None,'You cannot remove your own administrator access.')
        elif User.objects.filter(username=d['username']).exclude(pk=pk).exists(): form.add_error('username','Username already exists.')
        else:
            with transaction.atomic():
                user=user or User()
                for k in ['username','first_name','last_name','is_active']: setattr(user,k,d[k])
                if d['password']: user.set_password(d['password'])
                user.save(); Profile.objects.update_or_create(user=user,defaults={'role':d['role'],'department':d['department']}); audit(request.user,'Staff account saved',user)
            messages.success(request,'Staff account saved.'); return redirect('administration')
    return render(request,'form.html',{'active':'administration','title':'Staff account','form':form,'back':'/administration/'})

@login_required
def reset_demo(request):
    require(request.user,{'admin'})
    if not settings.ALLOW_DEMO_RESET or not settings.DEMO_MODE or not settings.DEBUG: raise PermissionDenied('Demo reset is disabled.')
    if request.method=='POST':
        if request.POST.get('confirmation')!='RESET SYNTHETIC DEMO': messages.error(request,'Type the exact confirmation phrase.')
        else:
            from django.core.management import call_command
            call_command('seed_demo',reset=True,confirm='RESET SYNTHETIC DEMO')
            logout(request); messages.success(request,'Synthetic demo reset. Sign in again.'); return redirect('login')
    return render(request,'reset.html',{'title':'Reset synthetic demo','active':'administration'})

@login_required
def help_view(request):
    return render(request,'help.html',{'title':'Workflow guide'})

@login_required
def fhir(request,resource,pk):
    mapping={'Patient':(Patient,''),'Appointment':(Appointment,'patient'),'Encounter':(Encounter,'patient'),'Condition':(Problem,'patient'),'Observation':(VitalSign,'encounter__patient'),'MedicationRequest':(Medication,'patient'),'ServiceRequest':(MedicalOrder,'encounter__patient'),'DiagnosticReport':(LabResult,'order__encounter__patient'),'Coverage':(InsurancePolicy,'patient')}
    if resource not in mapping: raise Http404()
    model,path=mapping[resource]; obj=get_object_or_404(model,pk=pk)
    p=path_value(obj,path) if path else obj; check_patient(request.user,p)
    if resource not in ['Patient','Appointment','Coverage']: require(request.user,CLINICAL|{'patient'})
    if role(request.user)=='patient' and resource=='DiagnosticReport' and not obj.released: raise PermissionDenied()
    if role(request.user)=='patient' and resource=='MedicationRequest' and not obj.signed_at: raise PermissionDenied('Unsigned prescriptions are not released to the portal.')
    if role(request.user)=='patient' and resource=='ServiceRequest': raise PermissionDenied('Orders are not exported to the portal.')
    data={'resourceType':resource,'id':str(pk),'meta':{'tag':[{'code':'synthetic-educational-nonconformant'}]}}
    if resource!='Patient': data['subject']={'reference':f'Patient/{p.pk}'}
    if resource=='Patient': data.update(identifier=[{'system':'urn:athenaflow:mrn','value':p.mrn}],name=[{'family':p.last_name,'given':[p.first_name]}],birthDate=str(p.dob),gender={'Male':'male','Female':'female','Other':'other'}.get(p.sex,'unknown'))
    elif resource=='Appointment': data.update(status={'Cancelled':'cancelled','Completed':'fulfilled','No Show':'noshow'}.get(obj.status,'booked'),start=obj.start.isoformat(),end=obj.end.isoformat())
    elif resource=='Encounter': data.update(status='finished' if obj.status in ['Signed','Closed'] else 'in-progress',period={'start':obj.created_at.isoformat()})
    elif resource=='Condition': data.update(code={'coding':[{'system':'http://hl7.org/fhir/sid/icd-10-cm','code':obj.code.code,'display':obj.code.description}]},clinicalStatus={'text':obj.status})
    elif resource=='Observation': data.update(status='final',code={'text':'Synthetic vital signs'},component=[{'code':{'text':name},'valueString':str(getattr(obj,name))} for name in ['systolic','diastolic','heart_rate','temperature','oxygen','height','weight']],effectiveDateTime=obj.created_at.isoformat())
    elif resource=='MedicationRequest': data.update(status=obj.status.lower(),intent='order',medicationCodeableConcept={'text':obj.name+' '+obj.strength},dosageInstruction=[{'text':obj.dose+' '+obj.frequency}])
    elif resource=='ServiceRequest': data.update(status=obj.status.lower(),intent='order',code={'text':obj.test})
    elif resource=='DiagnosticReport': data.update(status='final',code={'text':obj.order.test},conclusion=f'{obj.value} {obj.unit}; reference {obj.reference}; flag {obj.flag}')
    elif resource=='Coverage': data.update(status='active' if obj.status=='Active' else 'draft',subscriberId=obj.member_id,payor=[{'display':obj.payer}],period={'start':str(obj.effective),'end':str(obj.expiration)})
    audit(request.user,'FHIR-inspired export',obj)
    return JsonResponse(data)
