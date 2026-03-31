from django.core.management.base import BaseCommand
from bio_details.models import Currency, Order

class Command(BaseCommand):
    help = 'Fix orders with null currency'

    def handle(self, *args, **options):
        # Get the default INR currency
        try:
            inr_currency = Currency.objects.get(country_code='IN', is_active=True)
            self.stdout.write(f'Found INR currency: {inr_currency.symbol}')
        except Currency.DoesNotExist:
            # Create INR currency if it doesn't exist
            inr_currency = Currency.objects.create(
                code='INR',
                name='Indian Rupee',
                symbol='₹',
                country_code='IN',
                is_active=True
            )
            self.stdout.write('Created INR currency')
        
        # Fix orders with null currency
        orders_with_null_currency = Order.objects.filter(currency__isnull=True)
        count = orders_with_null_currency.count()
        
        if count > 0:
            orders_with_null_currency.update(currency=inr_currency)
            self.stdout.write(self.style.SUCCESS(f'Fixed {count} orders with null currency'))
        else:
            self.stdout.write('No orders with null currency found')
            
        # Also check for any orders with currency_id = None or invalid currency
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, order_id, currency_id FROM `order` WHERE currency_id IS NULL")
            null_currency_orders = cursor.fetchall()
            
            if null_currency_orders:
                self.stdout.write(f'Found {len(null_currency_orders)} orders with NULL currency_id:')
                for order_data in null_currency_orders:
                    self.stdout.write(f'  Order ID: {order_data[0]}, Order Number: {order_data[1]}')
                    
                # Fix them
                cursor.execute("UPDATE `order` SET currency_id = %s WHERE currency_id IS NULL", [inr_currency.id])
                self.stdout.write(self.style.SUCCESS(f'Updated {len(null_currency_orders)} orders with default currency'))
            else:
                self.stdout.write('No orders with NULL currency_id found in database')