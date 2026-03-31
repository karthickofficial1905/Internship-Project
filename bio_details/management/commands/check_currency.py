from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Check currency table structure'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Check if currency table exists and its structure
            cursor.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'currency'
                ORDER BY ordinal_position;
            """)
            
            columns = cursor.fetchall()
            if columns:
                self.stdout.write("Currency table columns:")
                for column in columns:
                    self.stdout.write(f"  {column[0]}: {column[1]}")
            else:
                self.stdout.write("Currency table not found")
                
            # Try to create the table manually if needed
            try:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS currency (
                        id SERIAL PRIMARY KEY,
                        code VARCHAR(3) UNIQUE NOT NULL,
                        name VARCHAR(50) NOT NULL,
                        symbol VARCHAR(5) NOT NULL,
                        country_code VARCHAR(2) NOT NULL,
                        is_active BOOLEAN DEFAULT TRUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                self.stdout.write("Currency table created/verified")
            except Exception as e:
                self.stdout.write(f"Error: {e}")