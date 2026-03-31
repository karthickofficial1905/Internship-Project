from django.db import migrations

def populate_emp_id(apps, schema_editor):
    Member = apps.get_model('bio_details', 'Member')
    
    # Get all members without emp_id
    members_without_id = Member.objects.filter(emp_id__isnull=True)
    
    for index, member in enumerate(members_without_id, start=1):
        member.emp_id = f"EMP{index:03d}"
        member.save()

def reverse_populate_emp_id(apps, schema_editor):
    # This is irreversible, so we'll just pass
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('bio_details', '0003_member_emp_id'),
    ]

    operations = [
        migrations.RunPython(populate_emp_id, reverse_populate_emp_id),
    ]