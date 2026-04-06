from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bio_details.models import LeaveApplication, Attendance
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Test duplicate leave application prevention'

    def handle(self, *args, **options):
        self.stdout.write("=== Testing Duplicate Leave Prevention ===")
        
        # Get test user
        user = User.objects.get(username='testuser')
        self.stdout.write(f"Using user: {user.username}")
        
        # Try to create duplicate leave application for April 7-10
        from_date = date(2024, 4, 7)
        to_date = date(2024, 4, 10)
        
        # Check existing applications
        existing_count = LeaveApplication.objects.filter(
            user=user,
            from_date=from_date,
            to_date=to_date
        ).count()
        
        self.stdout.write(f"Existing applications for {from_date} to {to_date}: {existing_count}")
        
        # Check for overlapping applications
        overlapping_leaves = LeaveApplication.objects.filter(
            user=user,
            status__in=['pending', 'approved'],
            from_date__lte=to_date,
            to_date__gte=from_date
        )
        
        self.stdout.write(f"Overlapping applications found: {overlapping_leaves.count()}")
        
        for leave in overlapping_leaves:
            self.stdout.write(f"  - {leave.from_date} to {leave.to_date} ({leave.status})")
        
        # Try to create a new overlapping application
        try:
            if overlapping_leaves.exists():
                self.stdout.write("✓ Duplicate prevention working - overlapping application exists")
            else:
                new_leave = LeaveApplication.objects.create(
                    user=user,
                    leave_type='casual',
                    duration='full_day',
                    from_date=from_date,
                    to_date=to_date,
                    reason='Test duplicate',
                    status='pending'
                )
                self.stdout.write(f"Created new application: {new_leave}")
        except Exception as e:
            self.stdout.write(f"Error: {str(e)}")
        
        self.stdout.write("=== Test Complete ===")