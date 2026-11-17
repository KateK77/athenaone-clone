from django.conf import settings
from django.db import models
from django.utils import timezone
from core.models import Patient

class Task(models.Model):
    patient = models.ForeignKey(Patient, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    role = models.CharField(max_length=20)
    assigned = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    priority = models.CharField(max_length=20, default='Routine', choices=[('Routine','Routine'),('Urgent','Urgent')])
    status = models.CharField(max_length=20, default='Open')
    related_url = models.CharField(max_length=200, blank=True)
    due = models.DateField(default=timezone.localdate)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['status','due','-created_at']
    def __str__(self): return self.title

class MessageThread(models.Model):
    patient = models.ForeignKey(Patient, related_name='threads', on_delete=models.CASCADE)
    subject = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.subject

class Message(models.Model):
    thread = models.ForeignKey(MessageThread, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    body = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['created_at']

class AppointmentRequest(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    preferred_date = models.DateField()
    reason = models.CharField(max_length=250)
    status = models.CharField(max_length=20, default='Requested')
    appointment = models.OneToOneField('core.Appointment', null=True, blank=True, on_delete=models.PROTECT)
    def __str__(self): return f'{self.patient} · {self.preferred_date} · {self.reason}'

class AIDraft(models.Model):
    encounter = models.ForeignKey('clinical.Encounter', related_name='ai_drafts', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    transcript = models.TextField()
    output = models.JSONField()
    model = models.CharField(max_length=80, default='deterministic-demo-v1')
    prompt_version = models.CharField(max_length=30, default='soap-v1')
    status = models.CharField(max_length=20, default='Unreviewed')
    created_at = models.DateTimeField(auto_now_add=True)
