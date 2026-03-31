from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Create member_details table manually'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS member_details (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL UNIQUE REFERENCES auth_user(id) ON DELETE CASCADE,
                    phone VARCHAR(15) NOT NULL,
                    address1 VARCHAR(200),
                    city VARCHAR(50) NOT NULL,
                    state VARCHAR(50) NOT NULL,
                    date_of_birth DATE,
                    gender VARCHAR(50) NOT NULL,
                    designation VARCHAR(100) NOT NULL,
                    profile_pic VARCHAR(100),
                    account_type VARCHAR(50),
                    bank_name VARCHAR(100),
                    ifsc_code VARCHAR(100),
                    account_number VARCHAR(100),
                    branch_loction VARCHAR(100),
                    pan_num VARCHAR(100)
                );
            """)
        self.stdout.write(self.style.SUCCESS('Successfully created member_details table'))