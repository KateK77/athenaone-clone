from django.core.exceptions import PermissionDenied
from django.db.models import Q
from core.models import Patient

CLINICAL = {'admin','physician','nurse','assistant'}
FINANCE = {'admin','manager','billing','coder'}
OPERATIONS = {'admin','manager','frontdesk'}
def role(user):
    return user.profile.role if user.is_authenticated and hasattr(user,'profile') else ''

def require(user, roles):
    if role(user) not in roles: raise PermissionDenied('Your role cannot perform this action.')

def patients_for(user):
    r = role(user)
    qs = Patient.objects.select_related('provider','provider__department')
    if r == 'patient': return qs.filter(user=user)
    if r == 'physician': return qs.filter(Q(provider__user=user)|Q(appointments__provider__user=user)).distinct()
    if r in {'nurse','assistant'}: return qs.filter(provider__department=user.profile.department)
    if r: return qs
    return qs.none()

def check_patient(user, patient):
    if not patients_for(user).filter(pk=patient.pk).exists(): raise PermissionDenied('This patient is outside your assigned scope.')

def check_encounter(user, encounter):
    check_patient(user, encounter.patient)
    if role(user)=='physician' and encounter.provider.user_id != user.id:
        raise PermissionDenied('This encounter is assigned to another clinician.')
