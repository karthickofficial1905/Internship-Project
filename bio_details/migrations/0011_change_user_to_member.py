# Generated manually to change user to member field

import django.db.models.deletion
from django.db import migrations, models


def populate_member_fields(apps, schema_editor):
    """Populate member fields with default member data and handle duplicates"""
    Attendance = apps.get_model('bio_details', 'Attendance')
    LeaveApplication = apps.get_model('bio_details', 'LeaveApplication')
    Member = apps.get_model('bio_details', 'Member')
    
    # Get the first member as default
    default_member = Member.objects.first()
    if default_member:
        # Update all attendance records
        Attendance.objects.filter(member__isnull=True).update(member=default_member)
        # Update all leave application records
        LeaveApplication.objects.filter(member__isnull=True).update(member=default_member)
        
        # Remove duplicate attendance records (keep the first one for each member-date combination)
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM attendance a1 USING attendance a2 
                WHERE a1.id > a2.id 
                AND a1.member_id = a2.member_id 
                AND a1.date = a2.date
            """)


class Migration(migrations.Migration):

    dependencies = [
        ('bio_details', '0010_member_email_member_name'),
    ]

    operations = [
        # Step 1: Remove old unique_together constraint
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together=set(),
        ),
        
        # Step 2: Add member field (nullable first)
        migrations.AddField(
            model_name='attendance',
            name='member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendance_records', to='bio_details.member'),
        ),
        
        # Step 3: Add member field to LeaveApplication (nullable first)  
        migrations.AddField(
            model_name='leaveapplication',
            name='member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leave_applications', to='bio_details.member'),
        ),
        
        # Step 4: Populate member fields with data
        migrations.RunPython(populate_member_fields),
        
        # Step 5: Remove old user fields
        migrations.RemoveField(
            model_name='attendance',
            name='user',
        ),
        migrations.RemoveField(
            model_name='leaveapplication',
            name='user',
        ),
        
        # Step 6: Make member field non-nullable
        migrations.AlterField(
            model_name='attendance',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_records', to='bio_details.member'),
        ),
        migrations.AlterField(
            model_name='leaveapplication',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leave_applications', to='bio_details.member'),
        ),
        
        # Step 7: Add new unique_together constraint
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together={('member', 'date')},
        ),
    ]