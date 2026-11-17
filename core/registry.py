from dataclasses import dataclass
from core.models import *
from clinical.models import *
from revenue.models import *
from engagement.models import *
from core.access import CLINICAL,FINANCE,OPERATIONS

@dataclass
class Resource:
    model: object
    title: str
    fields: tuple
    columns: tuple
    read: set
    write: set
    patient_path: str = 'patient'

R = {
 'patients': Resource(Patient,'Patients',('first_name','middle_name','last_name','preferred_name','dob','sex','gender_identity','phone','email','address','emergency_contact','language','provider','consent','active'),('mrn','first_name','last_name','dob','sex','phone','provider','active'),CLINICAL|FINANCE|OPERATIONS,OPERATIONS,''),
 'insurance': Resource(InsurancePolicy,'Insurance',('patient','payer','plan','member_id','group_number','subscriber','relationship','effective','expiration','primary','copay'),('patient','payer','member_id','expiration','status','verified_at'),OPERATIONS|{'billing'},OPERATIONS|{'billing'}),
 'schedule': Resource(Appointment,'Schedule',('patient','provider','department','appointment_type','start','duration','reason'),('start','patient','provider','appointment_type','reason','status'),OPERATIONS|CLINICAL,OPERATIONS),
 'waitlist': Resource(WaitlistEntry,'Waitlist',('patient','provider','earliest','latest','reason'),('patient','provider','earliest','latest','reason','status'),OPERATIONS,OPERATIONS),
 'encounters': Resource(Encounter,'Encounters',(),('patient','provider','complaint','created_at','status'),CLINICAL|FINANCE,set()),
 'problems': Resource(Problem,'Problems & diagnoses',('patient','code','encounter','primary','status','notes'),('patient','code','encounter','primary','status'),CLINICAL|{'coder'},{'admin','physician','coder'}),
 'allergies': Resource(Allergy,'Allergies',('patient','substance','reaction','severity'),('patient','substance','reaction','severity'),CLINICAL,{'admin','physician','nurse'}),
 'history': Resource(History,'History & documents',('patient','category','title','detail','date'),('patient','category','title','date'),CLINICAL,CLINICAL),
 'medications': Resource(Medication,'Medications',('patient','provider','name','strength','dose','route','frequency','start_date','end_date','quantity','pharmacy'),('patient','name','strength','dose','frequency','status'),CLINICAL,{'admin','physician'}),
 'orders': Resource(MedicalOrder,'Orders',('encounter','diagnosis','category','test','priority','authorization_required','authorization'),('encounter','test','category','priority','status'),CLINICAL,{'admin','physician'},'encounter__patient'),
 'results': Resource(LabResult,'Laboratory results',('order','value','unit','reference','flag','comment'),('order','value','unit','reference','flag','status','released'),CLINICAL,{'admin','physician','nurse'},'order__encounter__patient'),
 'charges': Resource(Charge,'Charge capture',('encounter','procedure','diagnosis','units','amount'),('encounter','procedure','diagnosis','units','amount','approved'),FINANCE,{'admin','coder','billing'},'encounter__patient'),
 'claims': Resource(Claim,'Claims',('policy','scenario'),('encounter','policy','total','balance','status'),FINANCE,{'admin','billing','coder'},'encounter__patient'),
 'denials': Resource(Denial,'Denial management',('appeal',),('claim','reason','category','due_date','status'),FINANCE,{'admin','billing'},'claim__encounter__patient'),
 'authorizations': Resource(Authorization,'Prior authorizations',('patient','policy','provider','service','diagnosis','supporting_notes','expiration'),('patient','service','provider','expiration','status'),CLINICAL|FINANCE,{'admin','physician','billing'}),
 'payments': Resource(Payment,'Payment activity',(),('patient','claim','source','amount','reference','created_at'),FINANCE|{'frontdesk'},set()),
 'tasks': Resource(Task,'Clinical inbox',('patient','title','category','role','assigned','priority','due'),('patient','title','category','priority','assigned','due','status'),CLINICAL|FINANCE|OPERATIONS,CLINICAL|FINANCE|OPERATIONS),
 'messages': Resource(MessageThread,'Messages',('patient','subject'),('patient','subject','created_at'),CLINICAL|OPERATIONS|{'patient'},CLINICAL|OPERATIONS|{'patient'}),
 'requests': Resource(AppointmentRequest,'Appointment requests',(),('patient','preferred_date','reason','status'),OPERATIONS,set()),
 'providers': Resource(Provider,'Providers',('name','user','department','start_hour','end_hour','active'),('name','department','start_hour','end_hour','active'),{'admin','manager'},{'admin'},None),
 'departments': Resource(Department,'Departments',('practice','name'),('name','practice'),{'admin','manager'},{'admin'},None),
 'appointment-types': Resource(AppointmentType,'Appointment types',('name','duration'),('name','duration'),OPERATIONS,{'admin'},None),
 'audit': Resource(AuditEvent,'Audit logs',(),('created_at','actor','action','entity','object_id','detail'),{'admin'},set(),None),
}

def path_value(obj,path):
    for part in path.split('__'):
        if obj is None: return None
        obj=getattr(obj,part,None)
    return obj
