from django.core.management.base import BaseCommand
from bio_details.models import Currency

class Command(BaseCommand):
    help = 'Ensure default currency exists'

    def handle(self, *args, **options):
        # Ensure INR currency exists
        currency, created = Currency.objects.get_or_create(
            country_code='IN',
            defaults={
                'code': 'INR',
                'name': 'Indian Rupee',
                'symbol': '₹',
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Created INR currency'))
        else:
            self.stdout.write(self.style.SUCCESS('INR currency already exists'))
            
        # Update any orders with null currency to use INR
        from bio_details.models import Order
        orders_updated = Order.objects.filter(currency__isnull=True).update(currency=currency)
        
        if orders_updated > 0:
            self.stdout.write(self.style.SUCCESS(f'Updated {orders_updated} orders with default currency'))
        else:
            self.stdout.write(self.style.SUCCESS('No orders needed currency update'))