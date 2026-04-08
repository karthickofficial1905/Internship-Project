from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bio_details.models import Member

class Command(BaseCommand):
    help = 'List all users and their roles'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('User Roles:'))
        self.stdout.write('-' * 50)
        
        users = User.objects.all().order_by('username')
        
        for user in users:
            try:
                member = user.member
                role = member.role
                status = "Active" if member.account_status else "Inactive"
                
                # Color code based on role
                if role == 'admin':
                    role_display = self.style.ERROR(role.upper())
                elif role == 'hr':
                    role_display = self.style.WARNING(role.upper())
                else:
                    role_display = self.style.SUCCESS(role.upper())
                
                self.stdout.write(
                    f'{user.username:<20} | {role_display:<15} | {status:<10} | {user.email}'
                )
                
            except Member.DoesNotExist:
                self.stdout.write(
                    f'{user.username:<20} | {"NO PROFILE":<15} | {"N/A":<10} | {user.email}'
                )
        
        self.stdout.write('-' * 50)
        
        # Summary
        total_users = User.objects.count()
        hr_count = Member.objects.filter(role='hr').count()
        admin_count = Member.objects.filter(role='admin').count()
        employee_count = Member.objects.filter(role='employee').count()
        
        self.stdout.write(f'Total Users: {total_users}')
        self.stdout.write(f'Admins: {admin_count}')
        self.stdout.write(f'HR: {hr_count}')
        self.stdout.write(f'Employees: {employee_count}')