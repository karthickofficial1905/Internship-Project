from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bio_details.models import Member

class Command(BaseCommand):
    help = 'Create a test user for login'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            user = User.objects.create_user(
                username='admin',
                email='admin@gmail.com',
                password='admin'
            )
            member = Member.objects.create(
                user=user,
                phone='1234567890',
                city='Test City',
                state='Test State',
                gender='Male',
                designation='Admin'
            )
            self.stdout.write(self.style.SUCCESS('Test user created: admin/admin'))
        else:
            self.stdout.write(self.style.WARNING('Test user already exists'))