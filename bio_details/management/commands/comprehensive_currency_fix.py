from django.core.management.base import BaseCommand
from bio_details.models import Currency, Order, Invoice

class Command(BaseCommand):
    help = 'Comprehensive currency fix'

    def handle(self, *args, **options):
        # Ensure INR currency exists
        inr_currency, created = Currency.objects.get_or_create(
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
            self.stdout.write('INR currency already exists')
            
        # Fix any orders with null currency
        orders_fixed = Order.objects.filter(currency__isnull=True).update(currency=inr_currency)
        if orders_fixed > 0:
            self.stdout.write(self.style.SUCCESS(f'Fixed {orders_fixed} orders with null currency'))
        else:
            self.stdout.write('No orders with null currency found')
            
        # Fix any invoices with null currency
        invoices_fixed = Invoice.objects.filter(currency__isnull=True).update(currency=inr_currency)
        if invoices_fixed > 0:
            self.stdout.write(self.style.SUCCESS(f'Fixed {invoices_fixed} invoices with null currency'))
        else:
            self.stdout.write('No invoices with null currency found')
            
        self.stdout.write(self.style.SUCCESS('Currency fix completed successfully!'))