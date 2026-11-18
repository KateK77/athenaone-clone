from django.db import migrations


def normalize_waiting(apps, schema_editor):
    Encounter = apps.get_model('clinical', 'Encounter')
    Note = apps.get_model('clinical', 'ClinicalNote')
    # Only untouched records created by the old check-in default; preserve drafts/signatures.
    untouched = Note.objects.filter(subjective='', objective='', assessment='', plan='', signed_at__isnull=True).values('encounter_id')
    Encounter.objects.filter(status='In Progress', pk__in=untouched,
        appointment__status__in=['Scheduled','Confirmed','Arrived','Checked In','Roomed']).update(status='Scheduled')


class Migration(migrations.Migration):
    dependencies = [('clinical', '0003_vitalsign_height_unit_vitalsign_weight_unit_and_more')]
    operations = [migrations.RunPython(normalize_waiting, migrations.RunPython.noop)]
