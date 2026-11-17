import uuid
from datetime import timedelta
from decimal import Decimal
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from django.utils import timezone

def mrn():
    return 'AF-' + uuid.uuid4().hex[:10].upper()

class Practice(models.Model):
    name = models.CharField(max_length=120)
    is_demo = models.BooleanField(default=False)
    def __str__(self): return self.name

class Department(models.Model):
    practice = models.ForeignKey(Practice, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    def __str__(self): return self.name

ROLES = [('admin', 'System Administrator'), ('manager', 'Practice Manager'), ('frontdesk', 'Front Desk'), ('physician', 'Physician'), ('nurse', 'Nurse'), ('assistant', 'Medical Assistant'), ('billing', 'Billing Specialist'), ('coder', 'Coding Specialist'), ('patient', 'Patient')]

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLES)
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.PROTECT)
    def __str__(self): return self.user.get_full_name() or self.user.username

class Provider(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    start_hour = models.PositiveSmallIntegerField(default=8, validators=[MaxValueValidator(23)])
    end_hour = models.PositiveSmallIntegerField(default=17, validators=[MaxValueValidator(23)])
    active = models.BooleanField(default=True)
    def clean(self):
        if self.start_hour >= self.end_hour: raise ValidationError('Availability must end after it starts.')
    def __str__(self): return self.name

class Patient(models.Model):
    mrn = models.CharField(max_length=20, default=mrn, unique=True, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=60)
    middle_name = models.CharField(max_length=60, blank=True)
    last_name = models.CharField(max_length=60)
    preferred_name = models.CharField(max_length=60, blank=True)
    dob = models.DateField('Date of birth')
    sex = models.CharField(max_length=20, choices=[('Female','Female'), ('Male','Male'), ('Other','Other'), ('Unknown','Unknown')])
    gender_identity = models.CharField(max_length=60, blank=True)
    phone = models.CharField(max_length=25, validators=[RegexValidator(r'^\+?[0-9() .-]{7,25}$', 'Enter a valid phone number.')])
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=250)
    emergency_contact = models.CharField(max_length=180, blank=True)
    language = models.CharField(max_length=40, default='English')
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT)
    consent = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['last_name', 'first_name']
        constraints = [models.UniqueConstraint(fields=['first_name','last_name','dob'], name='patient_identity_unique')]
    def clean(self):
        if self.dob and self.dob > timezone.localdate(): raise ValidationError({'dob': 'Birth date cannot be in the future.'})
        duplicate = Patient.objects.filter(first_name__iexact=self.first_name.strip(), last_name__iexact=self.last_name.strip(), dob=self.dob).exclude(pk=self.pk)
        if duplicate.exists(): raise ValidationError('Possible duplicate patient. Search the directory before registering.')
    @property
    def age(self):
        today = timezone.localdate()
        return today.year-self.dob.year-((today.month,today.day)<(self.dob.month,self.dob.day))
    @property
    def initials(self): return self.first_name[:1]+self.last_name[:1]
    def __str__(self): return f'{self.first_name} {self.last_name}'

class InsurancePolicy(models.Model):
    patient = models.ForeignKey(Patient, related_name='policies', on_delete=models.CASCADE)
    payer = models.CharField(max_length=100)
    plan = models.CharField(max_length=100)
    member_id = models.CharField(max_length=40)
    group_number = models.CharField(max_length=40, blank=True)
    subscriber = models.CharField(max_length=120)
    relationship = models.CharField(max_length=30, default='Self')
    effective = models.DateField()
    expiration = models.DateField()
    primary = models.BooleanField(default=True)
    status = models.CharField(max_length=30, default='Unverified')
    verified_at = models.DateTimeField(null=True, blank=True)
    copay = models.DecimalField(max_digits=8, decimal_places=2, default=25, validators=[MinValueValidator(0)])
    deductible = models.DecimalField(max_digits=9, decimal_places=2, default=1000)
    def clean(self):
        if self.effective and self.expiration and self.expiration < self.effective: raise ValidationError('Coverage dates are reversed.')
    def __str__(self): return f'{self.patient} · {self.payer}'

class AppointmentType(models.Model):
    name = models.CharField(max_length=80)
    duration = models.PositiveSmallIntegerField(default=30, validators=[MinValueValidator(5), MaxValueValidator(180)])
    def __str__(self): return self.name

APPOINTMENT_STATES = ['Scheduled','Confirmed','Arrived','Checked In','Roomed','In Progress','Completed','Checked Out','Cancelled','No Show','Rescheduled']
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, related_name='appointments', on_delete=models.PROTECT)
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    appointment_type = models.ForeignKey(AppointmentType, on_delete=models.PROTECT)
    start = models.DateTimeField()
    duration = models.PositiveSmallIntegerField(default=30, validators=[MinValueValidator(5), MaxValueValidator(180)])
    reason = models.CharField(max_length=250)
    status = models.CharField(max_length=30, default='Scheduled', choices=[(s,s) for s in APPOINTMENT_STATES])
    class Meta: ordering = ['start']
    @property
    def end(self): return self.start + timedelta(minutes=self.duration)
    def clean(self):
        if not self.start or not self.provider_id: return
        if self.department_id != self.provider.department_id: raise ValidationError('Provider does not belong to this department.')
        local = timezone.localtime(self.start)
        end = timezone.localtime(self.end)
        if local.weekday() > 4 or local.hour < self.provider.start_hour or end.date()!=local.date() or end.hour > self.provider.end_hour or (end.hour==self.provider.end_hour and end.minute):
            raise ValidationError('Outside provider availability (weekdays, configured office hours).')
        if self.status in ['Cancelled','No Show','Rescheduled']: return
        candidates = Appointment.objects.filter(provider=self.provider, start__lt=self.end, start__date=self.start.date()).exclude(pk=self.pk).exclude(status__in=['Cancelled','No Show','Rescheduled'])
        if any(a.end > self.start for a in candidates): raise ValidationError('This provider already has an overlapping appointment.')
    def __str__(self): return f'{self.patient} · {timezone.localtime(self.start):%b %d, %H:%M}'

class CheckIn(models.Model):
    appointment = models.OneToOneField(Appointment, related_name='checkin', on_delete=models.CASCADE)
    identity = models.BooleanField(default=False)
    demographics = models.BooleanField(default=False)
    insurance = models.BooleanField(default=False)
    consent = models.BooleanField(default=False)
    intake_forms = models.BooleanField(default=False)
    copay = models.DecimalField(max_digits=8, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    completed_at = models.DateTimeField(null=True)

class WaitlistEntry(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT)
    earliest = models.DateField()
    latest = models.DateField()
    reason = models.CharField(max_length=200)
    status = models.CharField(max_length=20, default='Waiting')
    appointment = models.OneToOneField(Appointment, null=True, blank=True, on_delete=models.SET_NULL)
    def clean(self):
        if self.earliest and self.latest and self.latest < self.earliest: raise ValidationError('Latest date must follow earliest date.')
    def __str__(self): return f'{self.patient} · {self.reason}'

class AuditEvent(models.Model):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=80)
    entity = models.CharField(max_length=80)
    object_id = models.CharField(max_length=40)
    detail = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['-created_at']
    def __str__(self): return f'{self.action} · {self.entity} #{self.object_id}'
