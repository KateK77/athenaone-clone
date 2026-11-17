from django import forms
from decimal import Decimal
from django.contrib.auth.models import User
from django.utils import timezone
from core.models import *
from clinical.models import *
from revenue.models import *
from core.access import patients_for,role
from core.registry import R

def resource_form(key,user,data=None,instance=None,initial=None):
    spec=R[key]
    widgets={}
    for name in spec.fields:
        field=spec.model._meta.get_field(name)
        if isinstance(field,models.DateTimeField): widgets[name]=forms.DateTimeInput(attrs={'type':'datetime-local'},format='%Y-%m-%dT%H:%M')
        elif isinstance(field,models.DateField): widgets[name]=forms.DateInput(attrs={'type':'date'})
        elif isinstance(field,models.TextField): widgets[name]=forms.Textarea(attrs={'rows':4})
    Form=forms.modelform_factory(spec.model,fields=spec.fields,widgets=widgets)
    form=Form(data,instance=instance,initial=initial)
    patients=patients_for(user)
    for name,field in form.fields.items():
        if not hasattr(field,'queryset'): continue
        model=field.queryset.model
        if model==Patient:
            field.queryset=patients
            if role(user)=='patient':
                field.initial=patients.first().pk if patients.exists() else None
                field.empty_label=None
                field.widget=forms.HiddenInput()
        elif model==Encounter:
            field.queryset=Encounter.objects.filter(patient__in=patients)
            if role(user)=='physician': field.queryset=field.queryset.filter(provider__user=user)
        elif model==Problem: field.queryset=Problem.objects.filter(patient__in=patients)
        elif model==MedicalOrder: field.queryset=MedicalOrder.objects.filter(encounter__patient__in=patients,category='Laboratory',status__in=['Processing','Completed'])
        elif model==InsurancePolicy: field.queryset=InsurancePolicy.objects.filter(patient__in=patients)
        elif model==Authorization: field.queryset=Authorization.objects.filter(patient__in=patients)
        elif model==Provider and role(user)=='physician': field.queryset=Provider.objects.filter(user=user)
        elif model==User: field.queryset=User.objects.exclude(profile__role='patient').filter(is_active=True)
    return form

class NoteForm(forms.Form):
    subjective=forms.CharField(widget=forms.Textarea(attrs={'rows':5}),required=False)
    objective=forms.CharField(widget=forms.Textarea(attrs={'rows':4}),required=False)
    assessment=forms.CharField(widget=forms.Textarea(attrs={'rows':4}),required=False)
    plan=forms.CharField(widget=forms.Textarea(attrs={'rows':5}),required=False)
    version=forms.IntegerField(widget=forms.HiddenInput)

class CheckInForm(forms.ModelForm):
    class Meta:
        model=CheckIn
        fields=['identity','demographics','insurance','consent','intake_forms','copay']

class VitalForm(forms.ModelForm):
    class Meta:
        model=VitalSign
        exclude=['encounter','author','created_at']

class IntakeForm(forms.ModelForm):
    class Meta:
        model=Encounter
        fields=['complaint','intake','medications_reviewed','allergies_reviewed','history_reviewed']
        widgets={'intake':forms.Textarea(attrs={'rows':4})}

class PaymentForm(forms.Form):
    amount=forms.DecimalField(min_value=Decimal('0.01'),max_digits=10,decimal_places=2)
    source=forms.ChoiceField(choices=[('Patient','Patient'),('Insurance','Insurance')])
    token=forms.CharField(widget=forms.HiddenInput)

class StaffForm(forms.Form):
    username=forms.CharField(max_length=150)
    first_name=forms.CharField(max_length=100)
    last_name=forms.CharField(max_length=100)
    role=forms.ChoiceField(choices=[r for r in ROLES if r[0]!='patient'])
    department=forms.ModelChoiceField(queryset=Department.objects.all())
    password=forms.CharField(min_length=12,required=False,widget=forms.PasswordInput,help_text='At least 12 characters. Leave blank to retain password when editing.')
    is_active=forms.BooleanField(required=False,initial=True)
