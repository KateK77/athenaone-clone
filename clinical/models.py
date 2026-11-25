from decimal import Decimal
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from core.models import Patient, Provider, Appointment

class DiagnosisCode(models.Model):
    code = models.CharField(max_length=12, unique=True)
    description = models.CharField(max_length=150)
    def __str__(self): return f'{self.code} · {self.description}'

class Encounter(models.Model):
    patient = models.ForeignKey(Patient, related_name='encounters', on_delete=models.PROTECT)
    appointment = models.OneToOneField(Appointment, null=True, blank=True, on_delete=models.PROTECT)
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT)
    status = models.CharField(max_length=30, default='Scheduled')
    complaint = models.CharField(max_length=250)
    intake = models.TextField(blank=True)
    medications_reviewed = models.BooleanField(default=False)
    allergies_reviewed = models.BooleanField(default=False)
    history_reviewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    class Meta: ordering = ['-created_at']
    def __str__(self): return f'ENC-{self.pk:04d} · {self.patient}' if self.pk else 'New encounter'

class ClinicalNote(models.Model):
    encounter = models.OneToOneField(Encounter, related_name='note', on_delete=models.CASCADE)
    subjective = models.TextField(blank=True)
    objective = models.TextField(blank=True)
    assessment = models.TextField(blank=True)
    plan = models.TextField(blank=True)
    version = models.PositiveIntegerField(default=1)
    signed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT)
    signed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    provenance = models.CharField(max_length=250, default='Clinician entered')
    def save(self, *args, **kwargs):
        if self.pk:
            old = ClinicalNote.objects.get(pk=self.pk)
            if old.signed_at and any(getattr(old,k) != getattr(self,k) for k in ['subjective','objective','assessment','plan','signed_by_id','signed_at','version','provenance']):
                raise ValidationError('Signed notes are immutable. Add an addendum.')
        super().save(*args, **kwargs)
    def __str__(self): return f'Note · {self.encounter}'

class NoteVersion(models.Model):
    note = models.ForeignKey(ClinicalNote, related_name='versions', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    version = models.PositiveIntegerField()
    content = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: constraints = [models.UniqueConstraint(fields=['note','version'], name='unique_note_version')]

class Addendum(models.Model):
    note = models.ForeignKey(ClinicalNote, related_name='addenda', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Problem(models.Model):
    patient = models.ForeignKey(Patient, related_name='problems', on_delete=models.CASCADE)
    code = models.ForeignKey(DiagnosisCode, on_delete=models.PROTECT)
    encounter = models.ForeignKey(Encounter, related_name='diagnoses', null=True, blank=True, on_delete=models.PROTECT)
    primary = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=[('Active','Active'),('Resolved','Resolved')], default='Active')
    notes = models.TextField(blank=True)
    def __str__(self): return str(self.code)

class Allergy(models.Model):
    patient = models.ForeignKey(Patient, related_name='allergies', on_delete=models.CASCADE)
    substance = models.CharField(max_length=100)
    reaction = models.CharField(max_length=150)
    severity = models.CharField(max_length=20, choices=[('Mild','Mild'),('Moderate','Moderate'),('Severe','Severe')])
    def __str__(self): return f'{self.substance} — {self.reaction}'

class History(models.Model):
    patient = models.ForeignKey(Patient, related_name='history', on_delete=models.CASCADE)
    category = models.CharField(max_length=30, choices=[(x,x) for x in ['Medical','Surgical','Family','Social','Immunization','Document']])
    title = models.CharField(max_length=150)
    detail = models.TextField()
    date = models.DateField(default=timezone.localdate)
    def __str__(self): return self.title

class VitalSign(models.Model):
    encounter = models.ForeignKey(Encounter, related_name='vitals', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    systolic = models.PositiveSmallIntegerField(validators=[MinValueValidator(50),MaxValueValidator(300)])
    diastolic = models.PositiveSmallIntegerField(validators=[MinValueValidator(20),MaxValueValidator(200)])
    heart_rate = models.PositiveSmallIntegerField(validators=[MinValueValidator(20),MaxValueValidator(250)])
    respiratory_rate = models.PositiveSmallIntegerField(default=16, validators=[MinValueValidator(4),MaxValueValidator(80)])
    temperature = models.DecimalField(max_digits=4,decimal_places=1, validators=[MinValueValidator(30),MaxValueValidator(45)], help_text='°C')
    oxygen = models.PositiveSmallIntegerField(validators=[MinValueValidator(50),MaxValueValidator(100)], help_text='%')
    height = models.DecimalField(max_digits=12,decimal_places=8, validators=[MinValueValidator(30),MaxValueValidator(250)], help_text='cm')
    weight = models.DecimalField(max_digits=12,decimal_places=8, validators=[MinValueValidator(1),MaxValueValidator(500)], help_text='kg')
    pain = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)
    @property
    def bmi(self): return round(self.weight / (self.height/100)**2, 1)
    height_unit = models.CharField(max_length=2, choices=[('in', 'in'), ('cm', 'cm')], default='cm')
    weight_unit = models.CharField(max_length=2, choices=[('lb', 'lb'), ('kg', 'kg')], default='kg')
    @staticmethod
    def measurement_text(value):
        return format(value, '.2f').rstrip('0').rstrip('.')
    @property
    def display_height(self):
        from decimal import Decimal
        return self.measurement_text(self.height / Decimal('2.54') if self.height_unit == 'in' else self.height)
    @property
    def display_weight(self):
        from decimal import Decimal
        return self.measurement_text(self.weight / Decimal('0.45359237') if self.weight_unit == 'lb' else self.weight)
    def __str__(self):
        return (f'Blood pressure {self.systolic}/{self.diastolic} mmHg · Heart rate {self.heart_rate} bpm · '
                f'Respiratory rate {self.respiratory_rate} breaths/min · Temperature {self.temperature} °C · '
                f'SpO₂ {self.oxygen}% · Height {self.display_height} {self.height_unit} · '
                f'Weight {self.display_weight} {self.weight_unit} · BMI {self.bmi} · Pain {self.pain}/10')

class Medication(models.Model):
    patient = models.ForeignKey(Patient, related_name='medications', on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    strength = models.CharField(max_length=50)
    dose = models.CharField(max_length=50)
    route = models.CharField(max_length=40, default='Oral')
    frequency = models.CharField(max_length=60)
    start_date = models.DateField(default=timezone.localdate)
    end_date = models.DateField(null=True, blank=True)
    quantity = models.PositiveIntegerField(default=30, validators=[MinValueValidator(1)])
    pharmacy = models.CharField(max_length=120, default='Demo Community Pharmacy')
    status = models.CharField(max_length=20, default='Draft')
    signed_at = models.DateTimeField(null=True, blank=True)
    def clean(self):
        if self.end_date and self.end_date < self.start_date: raise ValidationError('End date must follow start date.')
    def __str__(self): return f'{self.name} {self.strength} · {self.frequency}'

class MedicalOrder(models.Model):
    encounter = models.ForeignKey(Encounter, related_name='orders', on_delete=models.PROTECT)
    diagnosis = models.ForeignKey(Problem, on_delete=models.PROTECT)
    category = models.CharField(max_length=30, choices=[(x,x) for x in ['Laboratory','Imaging','Referral','Procedure','Medication']])
    test = models.CharField(max_length=120)
    priority = models.CharField(max_length=20, choices=[('Routine','Routine'),('Urgent','Urgent')], default='Routine')
    status = models.CharField(max_length=20, default='Draft')
    authorization_required = models.BooleanField(default=False)
    authorization = models.ForeignKey('revenue.Authorization', null=True, blank=True, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    @property
    def patient(self): return self.encounter.patient
    def clean(self):
        if self.diagnosis_id and self.encounter_id and self.diagnosis.patient_id != self.encounter.patient_id: raise ValidationError('Diagnosis belongs to another patient.')
        if self.authorization_id and self.authorization.patient_id != self.encounter.patient_id: raise ValidationError('Authorization belongs to another patient.')
    def __str__(self): return f'ORD-{self.pk:04d} · {self.test}' if self.pk else self.test

class LabResult(models.Model):
    order = models.OneToOneField(MedicalOrder, related_name='result', on_delete=models.PROTECT)
    value = models.CharField(max_length=100)
    unit = models.CharField(max_length=30)
    reference = models.CharField(max_length=80)
    flag = models.CharField(max_length=20, choices=[('Normal','Normal'),('High','High'),('Low','Low'),('Critical','Critical')])
    status = models.CharField(max_length=30, default='Entered')
    comment = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT)
    released = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    @property
    def patient(self): return self.order.patient
    def __str__(self): return f'{self.order.test}: {self.value} {self.unit}'
