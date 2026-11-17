from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from core.models import Patient, InsurancePolicy, Provider
from clinical.models import Encounter, DiagnosisCode

class ProcedureCode(models.Model):
    code = models.CharField(max_length=12, unique=True)
    description = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(0)])
    def __str__(self): return f'{self.code} · {self.description}'

class Charge(models.Model):
    encounter = models.ForeignKey(Encounter, related_name='charges', on_delete=models.PROTECT)
    procedure = models.ForeignKey(ProcedureCode, on_delete=models.PROTECT)
    diagnosis = models.ForeignKey(DiagnosisCode, on_delete=models.PROTECT)
    units = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    approved = models.BooleanField(default=False)
    class Meta: constraints = [models.UniqueConstraint(fields=['encounter','procedure'], name='unique_encounter_procedure')]
    @property
    def patient(self): return self.encounter.patient
    def __str__(self): return f'{self.procedure.code} · ${self.amount}'

class Claim(models.Model):
    encounter = models.OneToOneField(Encounter, related_name='claim', on_delete=models.PROTECT)
    policy = models.ForeignKey(InsurancePolicy, null=True, blank=True, on_delete=models.PROTECT)
    status = models.CharField(max_length=30, default='Draft')
    scenario = models.CharField(max_length=30, default='Pay', choices=[(s,s) for s in ['Pay','Partial','Deny','Reject']])
    validation_errors = models.JSONField(default=list, blank=True)
    validation_warnings = models.JSONField(default=list, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    @property
    def patient(self): return self.encounter.patient
    @property
    def total(self): return sum((c.amount*c.units for c in self.encounter.charges.all()), Decimal('0.00'))
    @property
    def balance(self): return self.total - sum((p.amount for p in self.payments.all()), Decimal('0.00'))
    def __str__(self): return f'CLM-{self.pk:05d}' if self.pk else 'New claim'

class Denial(models.Model):
    claim = models.OneToOneField(Claim, related_name='denial', on_delete=models.PROTECT)
    reason = models.CharField(max_length=200)
    category = models.CharField(max_length=50, default='Authorization')
    status = models.CharField(max_length=30, default='Open')
    appeal = models.TextField(blank=True)
    due_date = models.DateField()
    @property
    def patient(self): return self.claim.patient
    def __str__(self): return f'{self.claim} · {self.reason}'

class Authorization(models.Model):
    patient = models.ForeignKey(Patient, related_name='authorizations', on_delete=models.PROTECT)
    policy = models.ForeignKey(InsurancePolicy, on_delete=models.PROTECT)
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT)
    service = models.CharField(max_length=150)
    diagnosis = models.ForeignKey(DiagnosisCode, on_delete=models.PROTECT)
    supporting_notes = models.TextField(blank=True)
    status = models.CharField(max_length=40, default='Draft')
    expiration = models.DateField()
    submitted_at = models.DateTimeField(null=True, blank=True)
    def __str__(self): return f'AUTH-{self.pk:04d} · {self.service}' if self.pk else self.service

class Payment(models.Model):
    patient = models.ForeignKey(Patient, related_name='payments', on_delete=models.PROTECT)
    claim = models.ForeignKey(Claim, related_name='payments', null=True, blank=True, on_delete=models.PROTECT)
    checkin = models.OneToOneField('core.CheckIn', null=True, blank=True, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10,decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    source = models.CharField(max_length=25, choices=[('Patient','Patient'),('Insurance','Insurance'),('Copay','Copay')])
    reference = models.CharField(max_length=80, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: constraints = [models.CheckConstraint(condition=models.Q(amount__gt=0), name='payment_positive')]
    def __str__(self): return f'{self.reference} · ${self.amount}'
