from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bio_details.models import LeaveApplication, Attendance
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Test leave application and attendance system'

    def handle(self, *args, **options):
        self.stdout.write("=== Testing Leave Application System ===")
        
        # Get or create a test user
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(f"Created test user: {user.username}")
        else:
            self.stdout.write(f"Using existing user: {user.username}")
        
        # Create a leave application for April 7-10
        from_date = date(2024, 4, 7)
        to_date = date(2024, 4, 10)
        
        # Check if leave application already exists
        existing_leave = LeaveApplication.objects.filter(
            user=user,
            from_date=from_date,
            to_date=to_date
        ).first()
        
        if existing_leave:
            self.stdout.write(f"Leave application already exists: {existing_leave}")
            leave_app = existing_leave
        else:
            leave_app = LeaveApplication.objects.create(
                user=user,
                leave_type='personal',
                duration='full_day',
                from_date=from_date,
                to_date=to_date,
                reason='Personal work',
                status='pending'
            )
            self.stdout.write(f"Created leave application: {leave_app}")
        
        # Simulate approval and create attendance records
        if leave_app.status != 'approved':
            leave_app.status = 'approved'
            leave_app.approved_by = user  # In real scenario, this would be admin
            leave_app.save()
            
            # Create attendance records for leave dates
            current_date = from_date
            while current_date <= to_date:
                attendance_record, created = Attendance.objects.get_or_create(
                    user=user,
                    date=current_date,
                    defaults={
                        'status': 'absent',
                        'check_in': None,
                        'check_out': None,
                        'total_hours': None
                    }
                )
                
                if created:
                    self.stdout.write(f"Created attendance record for {current_date}: {attendance_record.status}")
                else:
                    self.stdout.write(f"Attendance record already exists for {current_date}: {attendance_record.status}")
                
                current_date += timedelta(days=1)
        
        self.stdout.write("\n=== Checking Attendance Records ===")
        attendance_records = Attendance.objects.filter(
            user=user,
            date__range=[from_date, to_date]
        ).order_by('date')
        
        for record in attendance_records:
            self.stdout.write(f"Date: {record.date}, Status: {record.status}, Check-in: {record.check_in}, Check-out: {record.check_out}")
        
        self.stdout.write(f"\nTotal leave days: {leave_app.total_days}")
        self.stdout.write(f"Leave status: {leave_app.status}")
        self.stdout.write("\n=== Test Complete ===")