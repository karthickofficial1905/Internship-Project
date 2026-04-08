from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bio_details.models import Member

class Command(BaseCommand):
    help = 'Set user role (employee, hr, admin)'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username of the user')
        parser.add_argument('role', type=str, choices=['employee', 'hr', 'admin'], help='Role to assign')

    def handle(self, *args, **options):
        username = options['username']
        role = options['role']
        
        try:
            user = User.objects.get(username=username)
            member = user.member
            
            old_role = member.role
            member.role = role
            member.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully updated {username} role from "{old_role}" to "{role}"'
                )
            )
            
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User "{username}" does not exist')
            )
        except Member.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User "{username}" does not have a member profile')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error updating user role: {str(e)}')
            )