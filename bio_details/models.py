from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
from datetime import date, datetime, timedelta
from django.core.validators import MinValueValidator, MaxValueValidator


class Country(models.Model):
    """Country model to store country information"""
    code = models.CharField(max_length=2, unique=True, help_text="Country code (e.g., IN, US, GB)")
    name = models.CharField(max_length=100, help_text="Country name (e.g., India, United States, United Kingdom)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ['name']
        db_table = 'country'


class Tax(models.Model):
    """Tax model to store country-wise tax information"""
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='taxes')
    tax_name = models.CharField(max_length=50, help_text="Tax name (e.g., GST, VAT, Sales Tax)")
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Tax rate in percentage")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.country.name} - {self.tax_name} ({self.tax_rate}%)"

    class Meta:
        verbose_name = "Tax"
        verbose_name_plural = "Taxes"
        unique_together = ('country', 'tax_name')
        db_table = 'tax'


class Currency(models.Model):
    """Currency model to store currency information"""
    code = models.CharField(max_length=3, unique=True, help_text="Currency code (e.g., USD, EUR, INR)")
    name = models.CharField(max_length=50, help_text="Currency name (e.g., US Dollar, Euro, Indian Rupee)")
    currency_name = models.CharField(max_length=50, null=True, blank=True)
    symbol = models.CharField(max_length=5, help_text="Currency symbol (e.g., $, €, ₹)")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='currencies', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"
        ordering = ['code']
        db_table = 'currency'


class Member(models.Model):
    """Company Employee Model"""
    ROLE_CHOICES = [
        ('user', 'User'),
        ('employee', 'Employee'),
        ('hr', 'HR'),
        ('admin', 'Admin'),
    ]
    
    emp_id = models.CharField(max_length=10, unique=True, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address1 = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=50)
    designation = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    profile_pic = models.ImageField(upload_to='profile/', null=True, blank=True)
    account_type = models.CharField(max_length=50, null=True, blank=True)
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    ifsc_code = models.CharField(max_length=100, null=True, blank=True)
    account_number = models.CharField(max_length=100, null=True, blank=True)
    branch_loction = models.CharField(max_length=100, null=True, blank=True)
    pan_num = models.CharField(max_length=100, null=True, blank=True)
    account_status = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.emp_id:
            last_member = Member.objects.order_by('-id').first()

            if last_member and last_member.emp_id:
                last_id = int(last_member.emp_id.replace('EMP', ''))
                new_id = last_id + 1
            else:
                new_id = 1

            self.emp_id = f"EMP{new_id:03d}"  # 3 digit length

        super().save(*args, **kwargs)

    def is_hr_or_admin(self):
        """Check if user is HR or Admin"""
        return self.role in ['hr', 'admin'] or self.user.is_superuser
    
    def is_hr(self):
        """Check if user is HR"""
        return self.role == 'hr'
    
    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'member_details'


class Customer(models.Model):
    """Customer Model for Product Purchase"""
    customer_id = models.CharField(max_length=10, unique=True, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='customer_profiles/', null=True, blank=True)
    account_type = models.CharField(max_length=50, null=True, blank=True)
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    ifsc_code = models.CharField(max_length=100, null=True, blank=True)
    account_number = models.CharField(max_length=100, null=True, blank=True)
    branch_location = models.CharField(max_length=100, null=True, blank=True)
    pan_num = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.customer_id:
            last_customer = Customer.objects.order_by('-id').first()
            if last_customer and last_customer.customer_id:
                last_id = int(last_customer.customer_id.replace('CUST', ''))
                new_id = last_id + 1
            else:
                new_id = 1
            self.customer_id = f"CUST{new_id:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer_id} - {self.user.username}"

    class Meta:
        db_table = 'customer_details'



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'



class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ManyToManyField(Category, related_name='brands', blank=True)


    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'brand'

class Product(models.Model):
    product_id = models.CharField(max_length=20, unique=True, blank=True)
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField(blank=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)
    min_stock = models.IntegerField(default=0)
    current_stock = models.IntegerField()
    product_image = models.ImageField(upload_to='products/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.product_id:
            last_product = Product.objects.order_by('-id').first()
            if last_product and last_product.product_id:
                last_id = int(last_product.product_id.replace('PRD', ''))
                new_id = last_id + 1
            else:
                new_id = 1
            self.product_id = f"PRD{new_id:03d}"
        super().save(*args, **kwargs)
    
    def get_tax_rate(self, country_code='IN'):
        """Get tax rate for specific country"""
        try:
            country = Country.objects.get(code=country_code)
            tax = Tax.objects.filter(country=country, is_active=True).first()
            return tax.tax_rate if tax else 0
        except Country.DoesNotExist:
            return 0
    
    def get_converted_price(self, currency='IN'):
        """Get product price in specified currency"""
        from .currency_utils import convert_currency
        return convert_currency(float(self.rate), 'IN', currency)
    
    def __str__(self):
        return f"{self.name} - {self.brand}"
    
    class Meta:
        db_table = 'product'


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def is_customer_cart(self):
        """Check if cart belongs to a customer"""
        return hasattr(self.user, 'customer')

    def __str__(self):
        return f"Cart - {self.user.username}"

    @property
    def total_amount(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def subtotal(self):
        return sum(item.product.rate * item.quantity for item in self.items.all())

    @property
    def total_discount(self):
        return sum(item.discount_amount for item in self.items.all())

    @property
    def total_gst(self):
        return sum(item.gst_amount for item in self.items.all())
    
    def get_total_tax(self, country_code='IN'):
        """Get total tax for specific country"""
        return sum(item.get_tax_amount(country_code) for item in self.items.all())
    
    def get_grand_total(self, country_code='IN'):
        """Get grand total with country-specific tax"""
        return self.subtotal - self.total_discount + self.get_total_tax(country_code)

    @property
    def grand_total(self):
        return self.subtotal - self.total_discount + self.total_gst
    
    def get_converted_subtotal(self, currency='IN'):
        """Get subtotal in specified currency"""
        from .currency_utils import convert_currency
        return convert_currency(float(self.subtotal), 'IN', currency)
    
    def get_converted_total_discount(self, currency='IN'):
        """Get total discount in specified currency"""
        from .currency_utils import convert_currency
        return convert_currency(float(self.total_discount), 'IN', currency)
    
    def get_converted_total_gst(self, currency='IN'):
        """Get total GST in specified currency"""
        from .currency_utils import convert_currency
        return convert_currency(float(self.total_gst), 'IN', currency)
    
    def get_converted_total_tax(self, country_code='IN', currency='IN'):
        """Get total tax in specified currency for specific country"""
        from .currency_utils import convert_currency
        return convert_currency(float(self.get_total_tax(country_code)), 'IN', currency)
    
    def get_converted_grand_total_with_tax(self, country_code='IN', currency='IN'):
        """Get grand total with tax in specified currency"""
        from .currency_utils import convert_currency
        return convert_currency(float(self.get_grand_total(country_code)), 'IN', currency)
    
    def get_converted_grand_total(self, currency='IN'):
        """Get grand total in specified currency (using default country tax)"""
        from .currency_utils import convert_currency
        return convert_currency(float(self.get_grand_total(currency)), 'IN', currency)

    class Meta:
        db_table = 'cart'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    @property
    def total_price(self):
        discounted_price = self.product.rate - (self.product.rate * self.product.discount / 100)
        return discounted_price * self.quantity

    @property
    def discount_amount(self):
        return (self.product.rate * self.product.discount / 100) * self.quantity

    @property
    def gst_amount(self):
        tax_rate = self.product.get_tax_rate('IN')  # Default to India
        return (self.total_price * tax_rate) / 100
    
    def get_tax_amount(self, country_code='IN'):
        """Get tax amount for specific country"""
        tax_rate = self.product.get_tax_rate(country_code)
        return (self.total_price * tax_rate) / 100
    
    def get_converted_total_price(self, currency='IN'):
        """Get total price in specified currency"""
        from .currency_utils import convert_currency
        return convert_currency(float(self.total_price), 'IN', currency)
    
    def get_converted_discount_amount(self, currency='IN'):
        """Get discount amount in specified currency"""
        from .currency_utils import convert_currency
        return convert_currency(float(self.discount_amount), 'IN', currency)
    
    def get_converted_tax_amount(self, country_code='IN', currency='IN'):
        """Get tax amount in specified currency for specific country"""
        from .currency_utils import convert_currency
        return convert_currency(float(self.get_tax_amount(country_code)), 'IN', currency)

    class Meta:
        db_table = 'cart_item'
        unique_together = ('cart', 'product')


class Order(models.Model):
    order_id = models.CharField(max_length=20, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, default=1, help_text="Order currency")
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def currency_symbol(self):
        """Get currency symbol from related currency object"""
        return self.currency.symbol if self.currency else '₹'
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            last_order = Order.objects.order_by('-id').first()
            if last_order and last_order.order_id:
                last_id = int(last_order.order_id.replace('ORD', ''))
                new_id = last_id + 1
            else:
                new_id = 1
            self.order_id = f"ORD{new_id:03d}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Order {self.order_id} - {self.user.username}"
    
    class Meta:
        db_table = 'order'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    
    @property
    def total_price(self):
        return self.price * self.quantity
    
    def __str__(self):
        return f"{self.product_name} - {self.quantity}"
    
    class Meta:
        db_table = 'order_item'


def get_default_terms():
    return [
        "Payment is due within 30 days from the invoice date",
        "Late payment charges may apply as per company policy",
        "Goods once sold cannot be returned or exchanged",
        "All disputes are subject to local jurisdiction",
        "Any damages or issues must be reported within 3 days of delivery",
        "The company is not responsible for delays caused by unforeseen circumstances",
        "Warranty or support will be provided only as per agreed terms",
    ]


class Invoice(models.Model):
    PAYMENT_METHODS = [('cash', 'Cash'),('card', 'Card'),('upi', 'UPI'),('bank_transfer', 'Bank Transfer'),]
    PAYMENT_STATUS = [('paid', 'Paid'),('pending', 'Pending'),('failed', 'Failed'),]
    invoice_number = models.CharField(max_length=20, unique=True, blank=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='invoice')
    customer_name = models.CharField(max_length=100)
    invoice_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, default=1, help_text="Invoice currency")
    country = models.ForeignKey(Country, on_delete=models.PROTECT, default=1, help_text="Invoice country")
    terms_conditions = models.JSONField(default=get_default_terms, blank=True)
    
    @property
    def currency_symbol(self):
        """Get currency symbol from related currency object"""
        return self.currency.symbol if self.currency else '₹'
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            last_invoice = Invoice.objects.order_by('-id').first()
            if last_invoice and last_invoice.invoice_number:
                last_id = int(last_invoice.invoice_number.replace('INV-', ''))
                new_id = last_id + 1
            else:
                new_id = 1
            self.invoice_number = f"INV-{new_id:03d}"
        super().save(*args, **kwargs)
        
    
    def get_converted_total_amount(self, target_currency_code='INR'):
        """Get total amount in specified currency"""
        from .currency_utils import convert_currency
        # Convert from invoice currency to target currency
        source_currency_code = self.currency.country.code if self.currency and self.currency.country else 'IN'
        return convert_currency(float(self.total_amount), source_currency_code, target_currency_code)
    
    def get_converted_total_discount(self, target_currency_code='INR'):
        """Get total discount in specified currency"""
        from .currency_utils import convert_currency
        source_currency_code = self.currency.country.code if self.currency and self.currency.country else 'IN'
        return convert_currency(float(self.total_discount), source_currency_code, target_currency_code)
    
    def get_converted_total_tax(self, target_currency_code='INR'):
        """Get total tax in specified currency"""
        from .currency_utils import convert_currency
        source_currency_code = self.currency.country.code if self.currency and self.currency.country else 'IN'
        return convert_currency(float(self.total_tax), source_currency_code, target_currency_code)
    
    def get_converted_subtotal(self, target_currency_code='INR'):
        """Get subtotal in specified currency"""
        from .currency_utils import convert_currency
        source_currency_code = self.currency.country.code if self.currency and self.currency.country else 'IN'
        return convert_currency(float(self.subtotal), source_currency_code, target_currency_code)
    
    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.customer_name}"
    
    class Meta:
        db_table = 'invoice'


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=100)
    qty = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=18.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    @property
    def tax_amount(self):
        """Calculate the tax amount for this item"""
        from decimal import Decimal
        subtotal = self.unit_price * self.qty
        return (subtotal * self.tax) / Decimal('100')
    
    def save(self, *args, **kwargs):
        from decimal import Decimal
        # Calculate total: (unit_price * qty) - discount + tax
        subtotal = self.unit_price * self.qty
        tax_amount = (subtotal * self.tax) / Decimal('100')
        self.total = subtotal - self.discount + tax_amount
        super().save(*args, **kwargs)

    def get_converted_unit_price(self, target_currency_code='INR'):
        """Get unit price in specified currency"""
        from .currency_utils import convert_currency
        # Convert from invoice currency to target currency
        source_currency_code = self.invoice.currency.country.code if self.invoice.currency and self.invoice.currency.country else 'IN'
        return convert_currency(float(self.unit_price), source_currency_code, target_currency_code)
    
    def get_converted_tax_amount(self, target_currency_code='INR'):
        """Get tax amount in specified currency"""
        from .currency_utils import convert_currency
        source_currency_code = self.invoice.currency.country.code if self.invoice.currency and self.invoice.currency.country else 'IN'
        return convert_currency(float(self.tax_amount), source_currency_code, target_currency_code)
    
    def get_converted_discount(self, target_currency_code='INR'):
        """Get discount in specified currency"""
        from .currency_utils import convert_currency
        source_currency_code = self.invoice.currency.country.code if self.invoice.currency and self.invoice.currency.country else 'IN'
        return convert_currency(float(self.discount), source_currency_code, target_currency_code)
    
    def get_converted_total(self, target_currency_code='INR'):
        """Get total in specified currency"""
        from .currency_utils import convert_currency
        source_currency_code = self.invoice.currency.country.code if self.invoice.currency and self.invoice.currency.country else 'IN'
        return convert_currency(float(self.total), source_currency_code, target_currency_code)
      
    
    def __str__(self):
        return f"{self.product_name} - {self.qty}"
    
    class Meta:
        db_table = 'invoice_item'


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('half_day', 'Half Day'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance_records',null=True, blank=True,)
    date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    total_hours = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Convert string date to date object if needed
        if isinstance(self.date, str):
            self.date = datetime.strptime(self.date, '%Y-%m-%d').date()
        
        # Calculate total hours if both check_in and check_out are provided
        if self.check_in and self.check_out:
            # Convert string times to time objects if needed
            if isinstance(self.check_in, str):
                from datetime import time as time_cls
                time_parts = self.check_in.split(':')
                hour = int(time_parts[0])
                minute = int(time_parts[1])
                second = int(time_parts[2]) if len(time_parts) > 2 else 0
                self.check_in = time_cls(hour, minute, second)
            
            if isinstance(self.check_out, str):
                from datetime import time as time_cls
                time_parts = self.check_out.split(':')
                hour = int(time_parts[0])
                minute = int(time_parts[1])
                second = int(time_parts[2]) if len(time_parts) > 2 else 0
                self.check_out = time_cls(hour, minute, second)
            
            check_in_datetime = datetime.combine(self.date, self.check_in)
            check_out_datetime = datetime.combine(self.date, self.check_out)
            
            # Handle case where check_out is next day
            if self.check_out < self.check_in:
                check_out_datetime += timedelta(days=1)
            
            time_diff = check_out_datetime - check_in_datetime
            self.total_hours = round(time_diff.total_seconds() / 3600, 2)
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user} - {self.date} - {self.status}"
    
    @property
    def formatted_hours(self):
        """Return total hours in 'Xh Ym' format"""
        if not self.total_hours:
            return "—"
        
        hours = int(self.total_hours)
        minutes = int((self.total_hours - hours) * 60)
        return f"{hours}h {minutes}m"
    
    class Meta:
        db_table = 'attendance'
        unique_together = ('user', 'date')
        ordering = ['-date']


class LeaveApplication(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('personal', 'Personal Leave'),
        ('sick', 'Sick Leave'),
        ('casual', 'Casual Leave'),
        ('emergency', 'Emergency Leave'),
    ]
    
    DURATION_CHOICES = [
        ('full_day', 'Full Day'),
        ('half_day', 'Half Day'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_applications')
    leave_type = models.CharField(max_length=10, choices=LEAVE_TYPE_CHOICES)
    duration = models.CharField(max_length=10, choices=DURATION_CHOICES)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves')
    approved_at = models.DateTimeField(null=True, blank=True)
    
    @property
    def total_days(self):
        """Calculate total leave days"""
        days = (self.to_date - self.from_date).days + 1
        return days / 2 if self.duration == 'half_day' else days
    
    def __str__(self):
        return f"{self.user.username} - {self.leave_type} ({self.from_date} to {self.to_date})"
    
    class Meta:
        db_table = 'leave_application'
        ordering = ['-applied_at']


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    technical_comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}/5)"
    
    class Meta:
        db_table = 'product_review'
        unique_together = ('product', 'user')
        ordering = ['-created_at']