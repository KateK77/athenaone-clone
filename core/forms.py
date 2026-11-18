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
    if key == 'messages' and instance is None:
        form.fields['body'] = forms.CharField(label='Message', max_length=10000, widget=forms.Textarea(attrs={'rows': 5}))
    if key == 'problems':
        form.fields['primary'].help_text = 'Select to make this the primary diagnosis for this encounter.'
    if key == 'orders':
        form.fields['authorization_required'].help_text = 'Select only when this service needs prior insurance authorization.'
    patients=patients_for(user)
    for name,field in form.fields.items():
        if not hasattr(field,'queryset'): continue
        model=field.queryset.model
        if model==Patient:
            field.queryset=patients
            field.label_from_instance = lambda p: f'{p} · {p.mrn} · DOB {p.dob:%b %d, %Y}'
            field.widget.attrs['data-search-select'] = 'patient'
            if role(user)=='patient':
                field.initial=patients.first().pk if patients.exists() else None
                field.empty_label=None
                field.widget=forms.HiddenInput()
        elif model==Encounter:
            field.queryset=Encounter.objects.filter(patient__in=patients)
            if role(user)=='physician': field.queryset=field.queryset.filter(provider__user=user)
        elif model==Problem:
            field.queryset=Problem.objects.filter(patient__in=patients).select_related('patient','encounter','code')
            field.label_from_instance = lambda p: f'{p.code} · {p.patient} · {p.patient.mrn} · {p.encounter or "Longitudinal"}'
            encounter_id = (data or {}).get('encounter') or (initial or {}).get('encounter') or getattr(instance, 'encounter_id', None)
            if str(encounter_id).isdigit():
                field.queryset = field.queryset.filter(encounter_id=encounter_id)
            field.widget.attrs['data-search-select'] = 'diagnosis'
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
    height = forms.DecimalField(max_digits=12, decimal_places=6, label='Height', widget=forms.NumberInput(attrs={'step':'any'}))
    weight = forms.DecimalField(max_digits=12, decimal_places=6, label='Weight', widget=forms.NumberInput(attrs={'step':'any'}))
    height_unit = forms.ChoiceField(choices=[('in','Inches (in)'),('cm','Centimeters (cm)')], initial='in', label='Height unit')
    weight_unit = forms.ChoiceField(choices=[('lb','Pounds (lb)'),('kg','Kilograms (kg)')], initial='lb', label='Weight unit')

    def __init__(self, *args, **kwargs):
        # Legacy metric POST clients remain compatible; rendered V2 forms always send units.
        if args and args[0] is not None:
            data = args[0].copy()
            data.setdefault('height_unit', 'cm'); data.setdefault('weight_unit', 'kg')
            args = (data,) + args[1:]
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.initial.update(height_unit='in', weight_unit='lb')
        self.order_fields(['systolic','diastolic','heart_rate','respiratory_rate','temperature','oxygen','height','height_unit','weight','weight_unit','pain'])
        for name, unit in {'systolic':'mmHg','diastolic':'mmHg','heart_rate':'bpm','respiratory_rate':'breaths/min','pain':'0–10 (0 = no pain; 10 = worst pain)'}.items():
            self.fields[name].help_text = unit
        self.fields['height'].help_text = 'Uses the selected height unit.'
        self.fields['weight'].help_text = 'Uses the selected weight unit.'

    def clean_height(self):
        value = self.cleaned_data['height']
        if self.data.get('height_unit') == 'in': value *= Decimal('2.54')
        if not Decimal('30') <= value <= Decimal('250'):
            raise forms.ValidationError('Height must be between 30 and 250 cm (11.82–98.42 in).')
        return value.quantize(Decimal('0.1'))

    def clean_weight(self):
        value = self.cleaned_data['weight']
        if self.data.get('weight_unit') == 'lb': value *= Decimal('0.45359237')
        if not Decimal('1') <= value <= Decimal('500'):
            raise forms.ValidationError('Weight must be between 1 and 500 kg (2.21–1102.31 lb).')
        return value.quantize(Decimal('0.1'))

    class Meta:
        model=VitalSign
        exclude=['encounter','author','created_at']

class IntakeForm(forms.ModelForm):
    class Meta:
        model=Encounter
        fields=['complaint','intake','medications_reviewed','allergies_reviewed','history_reviewed']
        widgets={'intake':forms.Textarea(attrs={'rows':4})}
        help_texts={'complaint':'Main reason for this visit.', 'intake':'Record patient-reported concerns, relevant observations, and preparation for the clinician.'}

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
