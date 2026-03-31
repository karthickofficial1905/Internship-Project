from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Check order table schema'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # PostgreSQL syntax to get table info
            cursor.execute("""
                SELECT column_name, data_type, is_nullable, column_default 
                FROM information_schema.columns 
                WHERE table_name = 'order'
            """)
            columns = cursor.fetchall()
            
            self.stdout.write("Order table columns:")
            for column in columns:
                self.stdout.write(f"  {column[0]} - {column[1]} - Null: {column[2]} - Default: {column[3]}")
                
            # Check if currency_symbol column exists
            column_names = [col[0] for col in columns]
            if 'currency_symbol' in column_names:
                self.stdout.write(self.style.ERROR("Found currency_symbol column - this needs to be removed"))
                
                # Try to drop the column
                try:
                    cursor.execute('ALTER TABLE "order" DROP COLUMN "currency_symbol"')
                    self.stdout.write(self.style.SUCCESS("Dropped currency_symbol column"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Failed to drop currency_symbol column: {e}"))
            else:
                self.stdout.write("No currency_symbol column found")