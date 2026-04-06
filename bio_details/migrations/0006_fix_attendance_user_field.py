# Generated manually to fix attendance user field with data migration

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


def populate_user_fields(apps, schema_editor):
    """Populate user fields with first available user"""
    User = apps.get_model('auth', 'User')
    Attendance = apps.get_model('bio_details', 'Attendance')
    LeaveApplication = apps.get_model('bio_details', 'LeaveApplication')
    
    # Get first user
    first_user = User.objects.first()
    if first_user:
        # Update all attendance records
        Attendance.objects.filter(user__isnull=True).update(user=first_user)
        # Update all leave application records
        LeaveApplication.objects.filter(user__isnull=True).update(user=first_user)


def reverse_populate_user_fields(apps, schema_editor):
    """Reverse operation - set user fields to null"""
    Attendance = apps.get_model('bio_details', 'Attendance')
    LeaveApplication = apps.get_model('bio_details', 'LeaveApplication')
    
    Attendance.objects.all().update(user=None)
    LeaveApplication.objects.all().update(user=None)


class Migration(migrations.Migration):

    dependencies = [
        ('bio_details', '0005_invoice_country'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # First remove the unique constraint
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together=set(),
        ),
        
        # Remove old employee field from attendance
        migrations.RemoveField(
            model_name='attendance',
            name='employee',
        ),
        
        # Remove old employee field from leaveapplication
        migrations.RemoveField(
            model_name='leaveapplication',
            name='employee',
        ),
        
        # Add user field to attendance (nullable first)
        migrations.AddField(
            model_name='attendance',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='attendance_records',
                to=settings.AUTH_USER_MODEL,
                null=True
            ),
        ),
        
        # Add user field to leaveapplication (nullable first)
        migrations.AddField(
            model_name='leaveapplication',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='leave_applications',
                to=settings.AUTH_USER_MODEL,
                null=True
            ),
        ),
        
        # Populate user fields with data
        migrations.RunPython(
            populate_user_fields,
            reverse_populate_user_fields,
        ),
        
        # Make user field non-nullable
        migrations.AlterField(
            model_name='attendance',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='attendance_records',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        
        migrations.AlterField(
            model_name='leaveapplication',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='leave_applications',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        
        # Add back the unique constraint with correct field name
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together={('user', 'date')},
        ),
    ]