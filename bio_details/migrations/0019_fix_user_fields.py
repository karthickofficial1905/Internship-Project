# Generated manually to fix user field issues

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def create_dummy_users_and_fix_members(apps, schema_editor):
    """Create dummy users for members with null user fields"""
    User = apps.get_model('auth', 'User')
    Member = apps.get_model('bio_details', 'Member')
    
    # Get members with null user fields
    null_user_members = Member.objects.filter(user__isnull=True)
    
    for i, member in enumerate(null_user_members):
        # Create a dummy user for each member
        dummy_user = User.objects.create_user(
            username=f'dummy_user_{member.id}',
            email=f'dummy_{member.id}@example.com',
            password='temporary_password'
        )
        member.user = dummy_user
        member.save()


def reverse_dummy_users(apps, schema_editor):
    """Remove dummy users created in forward migration"""
    User = apps.get_model('auth', 'User')
    # Remove dummy users
    User.objects.filter(username__startswith='dummy_user_').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('bio_details', '0018_auto_20260413_1248'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # First, create dummy users for members with null user fields
        migrations.RunPython(create_dummy_users_and_fix_members, reverse_dummy_users),
        
        # Then alter the fields to be non-nullable
        migrations.AlterField(
            model_name='leaveapplication',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leave_applications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='member',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]