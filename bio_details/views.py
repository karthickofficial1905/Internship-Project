from django.shortcuts import render, redirect
from .models import Member, Customer, Product, Cart, CartItem, Order, OrderItem, Invoice, InvoiceItem, Attendance, LeaveApplication, ProductReview
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from .models import Invoice, InvoiceItem
from decimal import Decimal
from django.http import JsonResponse
from django.db import models
import json
from .currency_utils import convert_currency, get_currency_info, COUNTRY_CURRENCY_MAP, get_live_exchange_rates
from django.utils import timezone


def customer_register(request):
    """Customer registration for product purchase"""
    if request.method == 'POST':
        # Get all form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        address1 = request.POST.get('address1')
        account_type = request.POST.get('account_type')
        bank_name = request.POST.get('bank_name')
        ifsc_code = request.POST.get('ifsc_code')
        branch_location = request.POST.get('branch_location')
        pan_num = request.POST.get('pan_num')
        account_number = request.POST.get('account_number')
        
        # Validation
        if not all([name, email, password, cpassword, phone]):
            messages.error(request, "Please fill all required fields!")
            return render(request, "customer_register.html")
            
        if password != cpassword:
            messages.error(request, "Passwords do not match!")
            return render(request, "customer_register.html")
        
        if User.objects.filter(username=name).exists():
            messages.error(request, 'Username already exists!')
            return render(request, "customer_register.html")
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return render(request, "customer_register.html")
        else:
            try:
                user = User.objects.create_user(username=name, email=email, password=password)
                Customer.objects.create(
                    user=user,
                    phone=phone,
                    address=address1 or '',
                    city=city or '',
                    state=state or '',
                    pincode=pincode or '',
                    date_of_birth=date_of_birth or None,
                    gender=gender or '',
                    account_type=account_type or '',
                    bank_name=bank_name or '',
                    ifsc_code=ifsc_code or '',
                    branch_location=branch_location or '',
                    pan_num=pan_num or '',
                    account_number=account_number or '',
                    profile_pic=request.FILES.get('profile_pic')
                )
                messages.success(request, 'Customer account created successfully!')
                return redirect('bio_details:login')
            except Exception as e:
                messages.error(request, f"Registration failed: {str(e)}")
                return render(request, "customer_register.html")
    
    return render(request, 'customer_register.html')


def rewrite_customer(request, customer_id):
    if not request.user.is_authenticated:
        return redirect('bio_details:login')
    
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('bio_details:dashboard')
    
    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        messages.error(request, "Customer not found!")
        return redirect('bio_details:usertable')
    
    if request.method == "POST":
        try:
            # Update user fields
            customer.user.username = request.POST.get('name')
            customer.user.email = request.POST.get('email')
            customer.user.save()
            
            # Update customer fields
            customer.phone = request.POST.get('phone')
            customer.address = request.POST.get('address')
            customer.city = request.POST.get('city')
            customer.state = request.POST.get('state')
            customer.pincode = request.POST.get('pincode')
            customer.date_of_birth = request.POST.get('date_of_birth') or None
            customer.gender = request.POST.get('gender')
            customer.account_type = request.POST.get('account_type')
            customer.bank_name = request.POST.get('bank_name')
            customer.ifsc_code = request.POST.get('ifsc_code')
            customer.account_number = request.POST.get('account_number')
            customer.branch_location = request.POST.get('branch_location')
            customer.pan_num = request.POST.get('pan_num')
            customer.is_active = bool(int(request.POST.get('is_active', '1')))
            
            if request.FILES.get('profile_pic'):
                customer.profile_pic = request.FILES.get('profile_pic')
            
            customer.save()
            messages.success(request, "Customer updated successfully")
            return redirect('bio_details:usertable')
            
        except Exception as e:
            messages.error(request, f"Error updating customer: {str(e)}")
    
    return render(request, "customer_rewrite.html", {"customer": customer})

# Member Authentication and Registration
def members(request):
    if request.method == "POST":
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        phone = request.POST.get('phone')
        
        # Validation
        if not all([name, email, password, cpassword, phone]):
            messages.error(request, "Please fill all required fields!")
            return render(request, "main_content.html")
            
        if password != cpassword:
            messages.error(request, "Passwords do not match!")
            return render(request, "main_content.html")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return render(request, "main_content.html")
        
        if User.objects.filter(username=name).exists():
            messages.error(request, "Username already exists!")
            return render(request, "main_content.html")
        
        try:
            # Create user
            user = User.objects.create_user(
                username=name,
                email=email,
                password=password
            )
            
            # Create member profile
            member = Member.objects.create(
                user=user,
                phone=phone,
                designation=request.POST.get('designation'),
                role=request.POST.get('role', 'user'),  # Default to employee if not provided
                address1=request.POST.get('address1'),
                city=request.POST.get('city'),
                state=request.POST.get('state'),
                pincode=request.POST.get('pincode'),
                date_of_birth=request.POST.get('date_of_birth') or None,
                gender=request.POST.get('gender'),
                account_type=request.POST.get('account_type'),
                bank_name=request.POST.get('bank_name'),
                ifsc_code=request.POST.get('ifsc_code'),
                account_number=request.POST.get('account_number'),
                branch_loction=request.POST.get('branch_location'),
                pan_num=request.POST.get('pan_num')
            )
            
            # Handle profile picture
            if request.FILES.get('profile_pic'):
                member.profile_pic = request.FILES.get('profile_pic')
                member.save()
            
            messages.success(request, f"Employee {name} registered successfully with ID: {member.emp_id}")
            if request.user.is_superuser:
                return redirect("bio_details:table")
            else:
                return redirect("bio_details:login")
            
        except Exception as e:
            messages.error(request, f"Registration failed: {str(e)}")
            return render(request, "main_content.html")
    
    return render(request, "main_content.html")



def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('bio_details:login')
    
    if not (request.user.is_superuser or (hasattr(request.user, 'member') and request.user.member.role == 'hr')):
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('bio_details:product_view')
    
    from datetime import datetime, date, timedelta
    from django.db.models import Count, Q
    from calendar import monthrange
    
    # Get selected month from request (default to current month)
    selected_month = int(request.GET.get('month', datetime.now().month))
    selected_year = int(request.GET.get('year', datetime.now().year))
    
    # Customer statistics
    total_customers = Customer.objects.count()
    active_customers = Customer.objects.filter(is_active=True).count()
    inactive_customers = Customer.objects.filter(is_active=False).count()
    
    # Employee statistics
    total_employees = Member.objects.filter(user__is_superuser=False,role="employee").count()
    active_employees = Member.objects.filter(account_status=True,role="employee",user__is_superuser=False).count()
    inactive_employees = Member.objects.filter(account_status=False,role="employee",user__is_superuser=False).count()
    
    # Product statistics
    total_products = Product.objects.count()
    available_products = Product.objects.filter(current_stock__gt=0).count()
    out_of_stock_products = Product.objects.filter(current_stock=0).count()
    
    # Order statistics
    if request.user.is_superuser or (hasattr(request.user, 'member') and request.user.member.role == 'hr'):
        total_orders = Order.objects.count()
        paid_orders = Invoice.objects.filter(payment_status='paid').count()
        pending_orders = Invoice.objects.filter(payment_status='pending').count()
    else:
        total_orders = Order.objects.filter(user=request.user).count()
        paid_orders = Invoice.objects.filter(order__user=request.user, payment_status='paid').count()
        pending_orders = Invoice.objects.filter(order__user=request.user, payment_status='pending').count()
    
    # Attendance statistics for selected month
    # Get all employees with employee role
    employees = Member.objects.filter(role='employee', account_status=True, user__is_superuser=False)
    
    # Calculate attendance stats for selected month
    present_days = Attendance.objects.filter(
        date__month=selected_month,
        date__year=selected_year,
        status='present'
    ).count()
    
    leave_days = Attendance.objects.filter(
        date__month=selected_month,
        date__year=selected_year,
        status='absent'
    ).count()
    
    # Add approved leaves to leave count
    approved_leaves = LeaveApplication.objects.filter(
        status='approved',
        from_date__month__lte=selected_month,
        to_date__month__gte=selected_month,
        from_date__year=selected_year
    )
    
    # Calculate total leave days for the month
    for leave in approved_leaves:
        # Calculate overlap with selected month
        month_start = date(selected_year, selected_month, 1)
        month_end = date(selected_year, selected_month, monthrange(selected_year, selected_month)[1])
        
        overlap_start = max(leave.from_date, month_start)
        overlap_end = min(leave.to_date, month_end)
        
        if overlap_start <= overlap_end:
            days_in_month = (overlap_end - overlap_start).days + 1
            if leave.duration == 'half_day':
                leave_days += days_in_month * 0.5
            else:
                leave_days += days_in_month
    
    half_days = Attendance.objects.filter(
        date__month=selected_month,
        date__year=selected_year,
        status='half_day'
    ).count()
    
    # Weekly attendance data for charts (last 4 weeks of selected month)
    weekly_data = []
    month_start = date(selected_year, selected_month, 1)
    month_end = date(selected_year, selected_month, monthrange(selected_year, selected_month)[1])
    
    # Calculate weekly data
    current_date = month_start
    week_num = 1
    while current_date <= month_end and week_num <= 4:
        week_end = min(current_date + timedelta(days=6), month_end)
        
        week_present = Attendance.objects.filter(
            date__range=[current_date, week_end],
            status='present'
        ).count()
        
        week_leave = Attendance.objects.filter(
            date__range=[current_date, week_end],
            status='absent'
        ).count()
        
        # Add approved leaves for this week
        week_approved_leaves = LeaveApplication.objects.filter(
            status='approved',
            from_date__lte=week_end,
            to_date__gte=current_date
        )
        
        for leave in week_approved_leaves:
            overlap_start = max(leave.from_date, current_date)
            overlap_end = min(leave.to_date, week_end)
            
            if overlap_start <= overlap_end:
                days_in_week = (overlap_end - overlap_start).days + 1
                if leave.duration == 'half_day':
                    week_leave += days_in_week * 0.5
                else:
                    week_leave += days_in_week
        
        week_halfday = Attendance.objects.filter(
            date__range=[current_date, week_end],
            status='half_day'
        ).count()
        
        weekly_data.append({
            'week': f'Week {week_num}',
            'present': week_present,
            'leave': week_leave,
            'halfday': week_halfday
        })
        
        current_date = week_end + timedelta(days=1)
        week_num += 1
    
    # Month names for dropdown
    month_names = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    # Generate years for analytics (from 2020 to current year + 1)
    from datetime import datetime
    current_year = datetime.now().year
    analytics_years = list(range(2020, current_year + 2))  # 2020 to next year
    analytics_years.reverse()  # Show newest years first
    
    # Generate available years for attendance year selector (same as analytics)
    available_years = analytics_years
    
    context = {
        'total_employees': total_employees,
        'active_employees': active_employees,
        'inactive_employees': inactive_employees,
        'total_customers': total_customers,
        'active_customers': active_customers,
        'inactive_customers': inactive_customers,
        'total_products': total_products,
        'available_products': available_products,
        'out_of_stock_products': out_of_stock_products,
        'total_orders': total_orders,
        'completed_orders': paid_orders,
        'pending_orders': pending_orders,
        # Attendance data
        'present_days': int(present_days),
        'leave_days': int(leave_days),
        'half_days': int(half_days),
        'selected_month': selected_month,
        'selected_year': selected_year,
        'selected_month_name': month_names[selected_month - 1],
        'weekly_data': weekly_data,
        'month_names': month_names,
        'analytics_years': analytics_years,
        'current_year': current_year,
        'available_years': available_years,
    }
    
    return render(request, "dashboard.html", context)





def login_page(request):

    if request.user.is_authenticated:
        return redirect('bio_details:dashboard')

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # check email exists
            user_obj = User.objects.get(email=email)

            # check password
            user = authenticate(request, username=user_obj.username, password=password)

            if not User.objects.filter(email=email).exists():
                messages.error(request,"Email not registered")

            if user is not None:
                login(request, user)
                messages.success(request, "Login successful")
                if user.is_superuser:
                    return redirect('bio_details:dashboard')
                else:
                    # Check if user is a customer
                    try:
                        Customer.objects.get(user=user)
                        return redirect('bio_details:my_profile_user')  # Customer user
                    except Customer.DoesNotExist:
                        return redirect('bio_details:my_profile')  # Regular member/employee
            else:
                messages.error(request, "Incorrect password")
                return render(request, "login.html", {"email": email})

        except User.DoesNotExist:
            messages.error(request, "Email not found")
            return render(request, "login.html", {"email": email})

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect('bio_details:login')

def table(request):
    if not request.user.is_authenticated:
        return redirect('bio_details:login')
    
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('bio_details:dashboard')
    
    search = request.GET.get('search')
    per_page = request.GET.get('per_page', 5) 
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 5
    
    members = Member.objects.filter(user__is_superuser=False,role='employee').order_by('id')  # Ensure consistent ordering

    if search:
        members = members.filter(user__username__icontains=search)

    paginator = Paginator(members, per_page) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "tables.html", {"page_obj": page_obj, "members": page_obj})


def usertable(request):
    if not request.user.is_authenticated:
        return redirect('bio_details:login')
    
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('bio_details:dashboard')
    
    search = request.GET.get('search')
    per_page = request.GET.get('per_page', 5) 
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 5
    
    customers = Customer.objects.all().order_by('id')

    if search:
        customers = customers.filter(
            models.Q(user__username__icontains=search) |
            models.Q(customer_id__icontains=search) |
            models.Q(user__email__icontains=search) |
            models.Q(phone__icontains=search)
        )

    paginator = Paginator(customers, per_page) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "user.html", {"page_obj": page_obj, "customers": page_obj})


def delete_customer(request, id):
    if not request.user.is_authenticated:
        return redirect('bio_details:login')
    
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('bio_details:dashboard')
    
    try:
        customer = Customer.objects.get(id=id)
        customer.is_active = False
        customer.save()
        messages.success(request, f"Customer {customer.user.username} deactivated successfully", extra_tags="delete-toast")
    except Customer.DoesNotExist:
        messages.error(request, "Customer not found!", extra_tags="delete-toast")
    
    return redirect("bio_details:usertable")


def delete_member(request, id):
    if not request.user.is_authenticated:
        return redirect('bio_details:login')
    
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('bio_details:dashboard')
    
    member = Member.objects.get(id=id)
    username = member.user.username
    member.account_status = False
    member.save()
    return redirect("bio_details:table")

def rewrite_member(request, emp_id):
    if not request.user.is_authenticated:
        return redirect('bio_details:login')
    
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('bio_details:dashboard')
    
    member = Member.objects.get(emp_id=emp_id)
    if request.method == "POST":
        member.user.username = request.POST.get('name')
        member.user.email = request.POST.get('email')
        member.user.save()
        member.phone = request.POST.get('phone')
        member.designation = request.POST.get('designation')
        member.role = request.POST.get('role', member.role)  # Keep existing role if not provided
        member.address1 = request.POST.get('address1')
        member.city = request.POST.get('city')
        member.state = request.POST.get('state')
        member.pincode = request.POST.get('pincode')
        member.date_of_birth = request.POST.get('date_of_birth')
        member.gender = request.POST.get('gender')
        member.account_type = request.POST.get('account_type')
        member.bank_name = request.POST.get('bank_name')
        member.ifsc_code = request.POST.get('ifsc_code')
        member.account_number = request.POST.get('account_number')
        member.branch_loction = request.POST.get('branch_loction')
        member.pan_num = request.POST.get('pan_num')
        member.account_status = bool(int(request.POST.get('account_status', '1')))
        if request.FILES.get('profile_pic'):
            member.profile_pic = request.FILES.get('profile_pic')
        member.save()
        messages.success(request, "Member updated successfully")
        return redirect('/table/?updated=success')
    return render(request, "rewrite.html", {"member": member})




def product_management(request):
    if not request.user.is_authenticated:
        return redirect('bio_details:login')
    
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('bio_details:dashboard')
    
    search = request.GET.get('search')
    per_page = request.GET.get('per_page', 5)  
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 5
    
    products = Product.objects.all().order_by('created_at')

    if search:
        products = products.filter(name__icontains=search)

    paginator = Paginator(products, per_page) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "product_table.html", {"page_obj": page_obj, "products": page_obj})

def product_form(request):
    if not request.user.is_authenticated:
        return redirect('bio_details:login')
    
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('bio_details:dashboard')
    
    from .models import Brand, Category
    brands = Brand.objects.all()
    categories = Category.objects.all()
    
    if request.method == "POST":
        try:
            # Get or create brand
            brand_name = request.POST.get('brand')
            brand, created = Brand.objects.get_or_create(name=brand_name)
            
            # Get or create category
            category_name = request.POST.get('category')
            category, created = Category.objects.get_or_create(name=category_name)
            
            product = Product.objects.create(
                name=request.POST.get('name'),
                brand=brand,
                category=category,
                description=request.POST.get('description', ''),
                rate=request.POST.get('price'),
                discount=request.POST.get('discount', 5.00),
                min_stock=request.POST.get('min_stock', 0),
                current_stock=request.POST.get('current_stock'),
            )
            
            if request.FILES.get('product_image'):
                product.product_image = request.FILES.get('product_image')
                product.save()
            
            messages.success(request, f"Product {product.name} created successfully with ID: {product.product_id}")
            return redirect('bio_details:product_management')
            
        except Exception as e:
            messages.error(request, f"Error creating product: {str(e)}")
    
    return render(request, "product_form.html", {'brands': brands, 'categories': categories})



def product_rewrite(request, product_id):
    if not request.user.is_authenticated:
        return redirect('bio_details:login')
    
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('bio_details:dashboard')
    
    product = Product.objects.get(product_id=product_id)
    from .models import Brand, Category
    brands = Brand.objects.all()
    categories = Category.objects.all()
    
    if request.method == "POST":
        try:
            # Get or create brand
            brand_name = request.POST.get('brand')
            brand, created = Brand.objects.get_or_create(name=brand_name)
            
            # Get or create category
            category_name = request.POST.get('category')
            category, created = Category.objects.get_or_create(name=category_name)
            
            # Update product
            product.name = request.POST.get('name')
            product.brand = brand
            product.category = category
            product.description = request.POST.get('description', '')
            product.rate = request.POST.get('price')
            product.discount = request.POST.get('discount', 5.00)
            product.min_stock = request.POST.get('min_stock', 0)
            product.current_stock = request.POST.get('current_stock')
            
            if request.FILES.get('product_image'):
                product.product_image = request.FILES.get('product_image')
            
            product.save()
            
            messages.success(request, f"Product {product.name} updated successfully!")
            return redirect('/product/?updated=success')
            
        except Exception as e:
            messages.error(request, f"Error updating product: {str(e)}")
    
    return render(request, "product_rewrite.html", {"product": product, 'brands': brands, 'categories': categories})



def product_view(request):
    if not request.user.is_authenticated:
        return redirect('bio_details:login')
    
    products = Product.objects.all().order_by('created_at')
    
    # Get selected currency from session, default to India
    selected_currency = request.session.get('selected_currency', 'IN')
    
    # Get currency object
    from .models import Currency, Country
    try:
        country_obj = Country.objects.get(code=selected_currency, is_active=True)
        currency_obj = Currency.objects.get(country=country_obj, is_active=True)
        currency_symbol = currency_obj.symbol
    except (Currency.DoesNotExist, Country.DoesNotExist):
        # Fallback to India if selected currency doesn't exist
        country_obj = Country.objects.get(code='IN', is_active=True)
        currency_obj = Currency.objects.get(country=country_obj, is_active=True)
        currency_symbol = currency_obj.symbol
        selected_currency = 'IN'
        # Update session with fallback
        request.session['selected_currency'] = 'IN'
    
    # Get all active currencies for dropdown
    currencies = Currency.objects.filter(is_active=True).select_related('country').order_by('name')
    
    paginator = Paginator(products, 8)  
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        'products': products,
        'selected_currency': selected_currency,
        'currency_symbol': currency_symbol,
        'currencies': currencies
    }
    
    return render(request, 'product.html', context)

def search_products(request):
    query = request.GET.get('search', '')
    products = Product.objects.filter(name__icontains=query)
    
    paginator = Paginator(products, 8)  
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    return render(request, "partials/product_results.html", {"products": products})


def delete_product(request, product_id):
    if not request.user.is_authenticated:
        return redirect('bio_details:login')
    
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('bio_details:dashboard')
    
    try:
        product = Product.objects.get(product_id=product_id)
        product_name = product.name
        product.delete()
        messages.success(request, f"Product {product_name} deleted successfully!")
    except Product.DoesNotExist:
        messages.error(request, "Product not found!")
    except Exception as e:
        messages.error(request, f"Error deleting product: {str(e)}")
    
    return redirect('bio_details:product_management')


def shop_detail(request, product_id):

    if not request.user.is_authenticated:
        return redirect('bio_details:login')

    try:
        product = Product.objects.get(product_id=product_id)
        
        # Get selected currency from session
        selected_currency = request.session.get('selected_currency', 'IN')
        
        # Get currency object
        from .models import Currency, Country
        try:
            country_obj = Country.objects.get(code=selected_currency, is_active=True)
            currency_obj = Currency.objects.get(country=country_obj, is_active=True)
            currency_symbol = currency_obj.symbol
        except (Currency.DoesNotExist, Country.DoesNotExist):
            country_obj = Country.objects.get(code='IN', is_active=True)
            currency_obj = Currency.objects.get(country=country_obj, is_active=True)
            currency_symbol = currency_obj.symbol
            selected_currency = 'IN'
        
        # Convert price to selected currency
        converted_price = product.get_converted_price(selected_currency)

        # stock check
        if product.current_stock == 0:
            messages.error(request, "Out of stock!")

        elif product.current_stock <= 5:
            messages.warning(request, "Limited stock available!")
        
        # Get product reviews
        reviews = ProductReview.objects.filter(product=product).select_related('user').order_by('-created_at')
        
        # Calculate average rating
        from django.db.models import Avg
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        avg_rating = round(avg_rating, 1)
        
        # Check if current user has already reviewed this product
        user_review = None
        if hasattr(request.user, 'customer'):
            user_review = reviews.filter(user=request.user).first()

        context = {
            'product': product,
            'converted_price': converted_price,
            'currency_symbol': currency_symbol,
            'selected_currency': selected_currency,
            'reviews': reviews,
            'avg_rating': avg_rating,
            'user_review': user_review,
            'review_count': reviews.count()
        }
        
        return render(request, 'shop.html', context)

    except Product.DoesNotExist:
        messages.error(request, "Product not found!")
        return redirect('bio_details:product_view')


def add_review(request, product_id):
    if not request.user.is_authenticated:
        return redirect('bio_details:login')
    
    # Check if user is a customer
    try:
        Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        messages.error(request, 'Only customers can add reviews.')
        return redirect('bio_details:shop_detail', product_id=product_id)
    
    if request.method == 'POST':
        try:
            product = Product.objects.get(product_id=product_id)
            rating = int(request.POST.get('rating'))
            comment = request.POST.get('comment')
            
            # Check if user already reviewed this product
            existing_review = ProductReview.objects.filter(product=product, user=request.user).first()
            
            if existing_review:
                # Update existing review
                existing_review.rating = rating
                existing_review.comment = comment
                existing_review.save()
                messages.success(request, 'Your review has been updated!')
            else:
                # Create new review
                ProductReview.objects.create(
                    product=product,
                    user=request.user,
                    rating=rating,
                    comment=comment
                )
                messages.success(request, 'Thank you for your review!')
            
        except Product.DoesNotExist:
            messages.error(request, 'Product not found!')
        except ValueError:
            messages.error(request, 'Invalid rating value!')
        except Exception as e:
            messages.error(request, f'Error adding review: {str(e)}')
    
    return redirect('bio_details:shop_detail', product_id=product_id)



def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('bio_details:customer_login')
    
    # Check if user is a customer
    try:
        Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        messages.error(request, 'Access denied. Customer account required.')
        return redirect('bio_details:customer_login')
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    
    # Get selected currency from session
    selected_currency = request.session.get('selected_currency', 'IN')
    currency_symbol = request.session.get('currency_symbol', '₹')
    
    # Get country-specific tax rate
    country_code = selected_currency
    
    # Import models inside function to avoid circular import issues
    from .models import Country, Tax
    
    # Get active taxes for the selected country
    try:
        country = Country.objects.get(code=country_code, is_active=True)
        taxes = Tax.objects.filter(country=country, is_active=True)
        print(f"Found country: {country.name}, Taxes count: {taxes.count()}")
        for tax in taxes:
            print(f"Tax: {tax.tax_name} - {tax.tax_rate}%")
    except Country.DoesNotExist:
        print(f"Country with code {country_code} not found, falling back to India")
        # Fallback to India if country not found
        country = Country.objects.get(code='IN', is_active=True)
        taxes = Tax.objects.filter(country=country, is_active=True)
        print(f"Fallback - Found country: {country.name}, Taxes count: {taxes.count()}")
        for tax in taxes:
            print(f"Fallback Tax: {tax.tax_name} - {tax.tax_rate}%")
    
    # Convert cart totals to selected currency
    from .currency_utils import convert_currency
    converted_subtotal = convert_currency(float(cart.subtotal), 'IN', selected_currency)
    
    # Calculate tax on subtotal first
    tax_amount = 0
    for tax in taxes:
        tax_amount += (converted_subtotal * float(tax.tax_rate)) / 100
    
    # Calculate discount amount
    converted_discount = convert_currency(float(cart.total_discount), 'IN', selected_currency)
    
    # Calculate grand total: subtotal + tax - discount
    converted_grand_total = converted_subtotal + tax_amount - converted_discount
    
    context = {
        'cart_items': cart_items,
        'cart': cart,
        'subtotal': converted_subtotal,
        'total_tax': tax_amount,
        'grand_total': converted_grand_total,
        'selected_currency': selected_currency,
        'currency_symbol': currency_symbol,
        'country_code': country_code,
        'taxes': taxes
    }
    
    return render(request, 'add_cart.html', context)



def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('bio_details:customer_login')
    
    # Check if user is a customer
    try:
        Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        messages.error(request, 'Access denied. Customer account required.')
        return redirect('bio_details:customer_login')
    
    try:
        product = Product.objects.get(product_id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        
        # Stock check
        if product.current_stock < quantity:
            messages.error(
                request,
                f"Only {product.current_stock} items available!",
                extra_tags="cart-toast"
            )
            return redirect('bio_details:shop_detail', product_id=product_id)
        
        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            new_total_quantity = cart_item.quantity + quantity

            if new_total_quantity > product.current_stock:
                messages.error(
                    request,
                    f"Only {product.current_stock} items available!",
                    extra_tags="cart-toast"
                )
                return redirect('bio_details:shop_detail', product_id=product_id)

            cart_item.quantity = new_total_quantity
            cart_item.save()

        messages.success(
            request,
            f"{product.name} added to cart!",
            extra_tags="cart-toast"
        )

        return redirect('bio_details:cart_view')

    except Product.DoesNotExist:
        messages.error(request, "Product not found!", extra_tags="cart-toast")
        return redirect('bio_details:product_view')
    
def update_cart_item(request, item_id):
    if not request.user.is_authenticated:
        return redirect('bio_details:login')
    
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        change = int(request.POST.get('change', 0))
        new_quantity = cart_item.quantity + change
        
        if new_quantity >= 1 and new_quantity <= cart_item.product.current_stock:
            cart_item.quantity = new_quantity
            cart_item.save()
            messages.success(request, "Quantity updated!")
        
        return redirect('bio_details:cart_view')
    except CartItem.DoesNotExist:
        messages.error(request, "Item not found!")
        return redirect('bio_details:cart_view')

def remove_cart_item(request, item_id):
    if not request.user.is_authenticated:
        return redirect('bio_details:login')
    
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        cart_item.delete()
        messages.success(request, "Item removed from cart!")
    except CartItem.DoesNotExist:
        messages.error(request, "Item not found!")
    
    return redirect('bio_details:cart_view')


def apply_discount(request):
    if not request.user.is_authenticated:
        return redirect('bio_details:login')
    
    if request.method == 'POST':
        discount_code = request.POST.get('discount_code', '')
        
        # Simple discount codes
        discount_rates = {
            'SAVE10': 10,
            'SAVE20': 20,
            'WELCOME': 15,
            'STUDENT': 25
        }
        
        discount = discount_rates.get(discount_code.upper(), 0)
        
        if discount > 0:
            request.session['discount'] = discount
            messages.success(request, f"Discount of {discount}% applied!")
        else:
            messages.error(request, "Invalid discount code!")
    
    return redirect('bio_details:cart_view')


def checkout(request):
    if not request.user.is_authenticated:
        return redirect('bio_details:customer_login')
    
    # Check if user is a customer
    try:
        Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        messages.error(request, 'Access denied. Customer account required.')
        return redirect('bio_details:customer_login')
    
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
        
        if not cart_items:
            messages.error(request, "Your cart is empty!")
            return redirect('bio_details:cart_view')
        
        # Check stock for all items first
        for item in cart_items:
            if item.product.current_stock < item.quantity:
                messages.error(request, f"Insufficient stock for {item.product.name}. Available: {item.product.current_stock}")
                return redirect('bio_details:cart_view')
        
        # Get cart discount
        cart_discount_percent = request.session.get('discount', 0)
        
        # Get selected currency and country from session
        selected_currency = request.session.get('selected_currency', 'IN')
        selected_country = request.session.get('selected_country', 'IN')  # Get country selection
        currency_symbol = request.session.get('currency_symbol', '₹')
        
        # Calculate totals in selected currency
        from .currency_utils import convert_currency
        
        # Convert cart totals to selected currency
        converted_subtotal = convert_currency(float(cart.subtotal), 'IN', selected_currency)
        converted_total_tax = convert_currency(float(cart.get_total_tax(selected_currency)), 'IN', selected_currency)
        converted_grand_total = convert_currency(float(cart.get_grand_total(selected_currency)), 'IN', selected_currency)
        
        subtotal = converted_grand_total
        discount_amount = (subtotal * cart_discount_percent) / 100
        final_total = subtotal - discount_amount
        
        # Create single order for all items with selected country and currency
        from .models import Currency, Country
        try:
            # Use the selected country from product view
            country_obj = Country.objects.get(code=selected_country, is_active=True)
            # Get currency for the selected currency (not necessarily same country)
            currency_obj = Currency.objects.get(country__code=selected_currency, is_active=True)
        except (Currency.DoesNotExist, Country.DoesNotExist):
            # Fallback to India if selected country/currency doesn't exist
            country_obj = Country.objects.get(code='IN', is_active=True)
            currency_obj = Currency.objects.get(country=country_obj, is_active=True)
            
        order = Order.objects.create(
            user=request.user,
            total_amount=final_total,
            currency=currency_obj
        )
        
        # Store cart discount in session for invoice
        if cart_discount_percent > 0:
            request.session['cart_discount_percent'] = cart_discount_percent
        
        # Create order items with converted prices
        for item in cart_items:
            # Convert product price to selected currency
            from .currency_utils import convert_currency
            converted_price = convert_currency(float(item.product.rate), 'IN', selected_currency)
            
            OrderItem.objects.create(
                order=order,
                product_name=item.product.name,
                price=converted_price,  # Use converted price
                quantity=item.quantity
            )
            
            # Reduce current stock immediately during checkout
            item.product.current_stock -= item.quantity
            item.product.save()
        
        # Clear cart and discount after checkout
        cart_items.delete()
        if 'discount' in request.session:
            del request.session['discount']
        
        # Redirect to invoice without placing order
        return redirect('bio_details:invoice_detail', order_id=order.id)
        
    except Cart.DoesNotExist:
        messages.error(request, "Cart not found!")
        return redirect('bio_details:cart_view')


def order_view(request):
    if not request.user.is_authenticated:
        return redirect('bio_details:login')
    
    if not request.user.is_superuser:
        return redirect('bio_details:dashboard')
    
    search = request.GET.get('search')
    per_page = request.GET.get('per_page', 5)  
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 5
    
    # Get all orders with their related data
    orders = Order.objects.select_related('user', 'invoice').prefetch_related('user__member').order_by('created_at')

    if search:
        orders = orders.filter(
            models.Q(order_id__icontains=search) |
            models.Q(user__username__icontains=search)
        )
    
    paginator = Paginator(orders, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all invoices
    invoices = Invoice.objects.all()

    # Add terms data - make empty to show default terms in template
    term = [ "Payment is due within 30 days from the invoice date",
            "Late payment charges may apply as per company policy   ",
            "Goods once sold cannot be returned or exchanged",
            "All disputes are subject to local jurisdiction",
            "Any damages or issues must be reported within 3 days of delivery",
            "The company is not responsible for delays caused by unforeseen circumstances",
            "Warranty or support will be provided only as per agreed terms",]

    return render(request, 'order.html', {
        'page_obj': page_obj,
        'invoices': invoices,
        'terms': term,
    })




def update_invoice_item(request, item_id):
    if not request.user.is_authenticated:
        return redirect('bio_details:login')
    
    if request.method == 'POST':
        try:
            item = InvoiceItem.objects.get(id=item_id)
            change = int(request.POST.get('change', 0))
            old_qty = item.qty
            new_qty = item.qty + change
            
            if new_qty >= 1:
                item.qty = new_qty
                
                # Recalculate discount based on new quantity
                from decimal import Decimal
                discount_per_unit = item.discount / old_qty if old_qty > 0 else Decimal('0')
                item.discount = discount_per_unit * new_qty
                
                item.save()  # This will recalculate the total
                
                # Recalculate invoice totals
                invoice = item.invoice
                invoice_items = invoice.items.all()
                invoice.subtotal = sum(item.unit_price * item.qty for item in invoice_items)
                invoice.total_tax = sum((item.unit_price * item.qty * item.tax) / Decimal('100') for item in invoice_items)
                invoice.total_discount = sum(item.discount for item in invoice_items)
                invoice.total_amount = invoice.subtotal + invoice.total_tax - invoice.total_discount
                invoice.save()
                
                messages.success(request, "Quantity updated successfully!")
            else:
                messages.error(request, "Quantity cannot be less than 1!")
                
            return redirect('bio_details:invoice_detail', order_id=item.invoice.order.id)
            
        except InvoiceItem.DoesNotExist:
            messages.error(request, "Item not found!")
            return redirect('bio_details:order')
    
    return redirect('bio_details:order')



def invoice_view(request, order_id=None):
    if not request.user.is_authenticated:
        return redirect('bio_details:login')
    
    # Handle POST request for payment method update
    if request.method == 'POST' and order_id:
        try:
            order = Order.objects.get(id=order_id)
            invoice = Invoice.objects.get(order=order)
            payment_method = request.POST.get('payment_method', 'cash')
            
            invoice.payment_method = payment_method
            invoice.save()
            return redirect('bio_details:dashboard')
            
        except (Order.DoesNotExist, Invoice.DoesNotExist):
            messages.error(request, "Order or Invoice not found!")
            return redirect('bio_details:order')
    
    if order_id:
        try:
            order = Order.objects.get(id=order_id)
            
            # Get selected currency and country from session (independent selections)
            selected_currency = request.session.get('selected_currency', 'IN')
            selected_country = request.session.get('selected_country', 'IN')
            
            # Get currency object for selected currency
            from .models import Currency, Country
            try:
                # Get the country object for selected country
                country_obj = Country.objects.get(code=selected_country, is_active=True)
                # Get the currency object for selected currency (independent of country)
                currency_obj = Currency.objects.get(country__code=selected_currency, is_active=True)
                display_currency = currency_obj
            except (Currency.DoesNotExist, Country.DoesNotExist):
                country_obj = Country.objects.get(code='IN', is_active=True)
                display_currency = Currency.objects.get(country=country_obj, is_active=True)
                selected_currency = 'IN'
                selected_country = 'IN'
            
            # Get or create invoice for this order
            invoice, created = Invoice.objects.get_or_create(
                order=order,
                defaults={
                    'customer_name': order.user.get_full_name() or order.user.username,
                    'invoice_date': order.created_at,
                    'payment_method': 'cash',
                    'payment_status': 'pending',
                    'subtotal': Decimal('0'),
                    'total_tax': Decimal('0'),
                    'total_discount': Decimal('0'),
                    'total_amount': Decimal('0'),
                    'currency': display_currency,
                    'country': country_obj
                }
            )
            
            if created:
                # Get cart discount from session
                cart_discount_percent = request.session.get('cart_discount_percent', 0)
                
                subtotal = Decimal('0')
                total_tax = Decimal('0')
                total_discount = Decimal('0')
                
                for order_item in order.items.all():
                    # Get product to access its discount and tax rate
                    try:
                        product = Product.objects.get(name=order_item.product_name)
                        product_discount_percent = product.discount
                        # Get tax rate for the invoice currency country
                        tax_rate = product.get_tax_rate(selected_currency)
                    except Product.DoesNotExist:
                        product_discount_percent = Decimal('0')
                        tax_rate = Decimal('18')  # Default tax rate
                    
                    item_subtotal = order_item.price * order_item.quantity
                    item_tax = (item_subtotal * Decimal(str(tax_rate))) / Decimal('100')
                    
                    # Apply product discount first
                    product_discount_amount = (item_subtotal * product_discount_percent) / Decimal('100')
                    
                    # Apply cart discount on top of product discount
                    if cart_discount_percent > 0:
                        cart_discount_amount = (item_subtotal * Decimal(str(cart_discount_percent))) / Decimal('100')
                    else:
                        cart_discount_amount = Decimal('0')
                    
                    # Total discount is product discount + cart discount
                    item_discount = product_discount_amount + cart_discount_amount
                    item_total = item_subtotal + item_tax - item_discount
                    
                    InvoiceItem(
                        invoice=invoice,
                        product_name=order_item.product_name,
                        qty=order_item.quantity,
                        unit_price=order_item.price,
                        tax=Decimal(str(tax_rate)),
                        discount=item_discount,
                        total=item_total
                    ).save()
                    
                    subtotal += item_subtotal
                    total_tax += item_tax
                    total_discount += item_discount
                
                # Update invoice totals
                invoice.subtotal = subtotal
                invoice.total_tax = total_tax
                invoice.total_discount = total_discount
                invoice.total_amount = subtotal + total_tax - total_discount
                invoice.save()
                
                # Clear cart discount from session after using it
                if 'cart_discount_percent' in request.session:
                    del request.session['cart_discount_percent']
            
            # Get list of product IDs already in the invoice
            added_product_ids = []
            if invoice.items.exists():
                for item in invoice.items.all():
                    try:
                        product = Product.objects.get(name=item.product_name)
                        added_product_ids.append(product.product_id)
                    except Product.DoesNotExist:
                        pass
            
            # Terms and conditions
            terms_conditions = [
                "Payment is due within 30 days from the invoice date",
                "Late payment charges may apply as per company policy",
                "Goods once sold cannot be returned or exchanged",
                "All disputes are subject to local jurisdiction",
                "Any damages or issues must be reported within 3 days of delivery",
                "The company is not responsible for delays caused by unforeseen circumstances",
                "Warranty or support will be provided only as per agreed terms"
            ]
            
            # Get all active currencies for dropdown
            currencies = Currency.objects.filter(is_active=True).select_related('country').order_by('name')
            
            context = {
                'invoice_date': invoice.invoice_date,
                'customer_name': invoice.customer_name,
                'customer_email': order.user.email,
                'customer_phone': getattr(order.user.member, 'phone', '+91 9876543210') if hasattr(order.user, 'member') else '+91 9876543210',
                'payment_method': invoice.payment_method,  # Raw value instead of display
                'payment_status': invoice.get_payment_status_display(),
                'transaction_id': invoice.transaction_id,
                'items': invoice.items.all(),
                'subtotal': invoice.subtotal,
                'total_tax': invoice.total_tax,
                'total_discount': invoice.total_discount,
                'total_amount': invoice.total_amount,
                'invoice_number': invoice.invoice_number,
                'invoice': invoice,
                'products': Product.objects.filter(current_stock__gt=0),
                'added_product_ids': added_product_ids,
                'terms_conditions': terms_conditions,
                'currency_symbol': display_currency.symbol,
                'selected_currency': selected_currency,
                'selected_country': selected_country,
                'selected_country_name': country_obj.name,
                'currencies': currencies,
                'display_currency': display_currency,
            }
            
        except Order.DoesNotExist:
            messages.error(request, "Order not found!")
            return redirect('bio_details:cart')
    else:
        messages.error(request, "Invoice not found!")
        return redirect('bio_details:cart')
    
    return render(request, 'invoice.html', context)




def invoice2_view(request, order_id):
    if not request.user.is_authenticated:
        return redirect('bio_details:login')
    
    try:
        order = Order.objects.get(id=order_id)
        
        # Allow access if user owns the order OR is superuser
        if order.user != request.user and not request.user.is_superuser:
            messages.error(request, "Access denied. You can only view your own orders.")
            return redirect('bio_details:my_orders')
        
        invoice = Invoice.objects.get(order=order)
        
        # Get selected currency from URL parameter or use order currency
        selected_currency = request.GET.get('currency', order.currency.country.code if order.currency else 'IN')
        
        # Get currency symbol from database based on selected currency
        from .models import Currency, Country,Tax
        try:
            if selected_currency == 'IN':
                selected_currency = 'INR'
            
            # Get currency object to get the symbol
            currency_obj = Currency.objects.filter(code=selected_currency, is_active=True).first()
            if not currency_obj:
                # Try by country code
                country_obj = Country.objects.filter(code=selected_currency[:2], is_active=True).first()
                if country_obj:
                    currency_obj = Currency.objects.filter(country=country_obj, is_active=True).first()
            
            currency_symbol = currency_obj.symbol if currency_obj else '₹'
        except Exception:
            currency_symbol = '₹'
        
        # Get currency object for selected currency
        from .models import Currency, Country
        try:
            if selected_currency == 'IN':
                selected_currency = 'INR'  # Convert IN to INR for consistency
            
            # Try to find currency by code first
            display_currency = Currency.objects.filter(code=selected_currency, is_active=True).first()
            if not display_currency:
                # Fallback to country code lookup
                country_obj = Country.objects.get(code=selected_currency[:2], is_active=True)
                display_currency = Currency.objects.get(country=country_obj, is_active=True)
        except (Currency.DoesNotExist, Country.DoesNotExist):
            # Final fallback to INR
            display_currency = Currency.objects.get(code='INR', is_active=True)
            selected_currency = 'INR'
            currency_symbol = '₹'
        
        # Get all active currencies for dropdown
        currencies = Currency.objects.filter(is_active=True).order_by('name')
        
        context = {
            'invoice_date': invoice.invoice_date,
            'customer_name': invoice.customer_name,
            'customer_email': order.user.email,
            'customer_phone': getattr(order.user.member, 'phone', '+91 9876543210') if hasattr(order.user, 'member') else '+91 9876543210',
            'payment_method': invoice.payment_method,
            'payment_status': invoice.get_payment_status_display(),
            'transaction_id': invoice.transaction_id,
            'items': invoice.items.all(),
            'subtotal': invoice.subtotal,
            'total_tax': invoice.total_tax,
            'total_discount': invoice.total_discount,
            'total_amount': invoice.subtotal + invoice.total_tax - invoice.total_discount,
            'invoice_number': invoice.invoice_number,
            'invoice': invoice,
            'currency_symbol': currency_symbol,
            'selected_currency': selected_currency,
            'currencies': currencies,
            'display_currency': display_currency,
        }
        
        return render(request, 'invoice2.html', context)
        
    except (Order.DoesNotExist, Invoice.DoesNotExist):
        messages.error(request, "Invoice not found!")
        if request.user.is_superuser:
            return redirect('bio_details:order')
        else:
            return redirect('bio_details:my_orders')




def add_product_to_invoice(request, order_id):
    if not request.user.is_authenticated:
        return redirect('bio_details:login')
    
    if request.method == 'POST':
        from decimal import Decimal
        
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        # Clean and validate tax_rate input
        tax_rate_str = request.POST.get('tax_rate', '18')
        # Remove common problematic characters
        tax_rate_str = tax_rate_str.replace('%', '').replace('&#39;', '').replace("'", '').strip()
        # Extract only numeric characters and decimal point
        import re
        tax_rate_str = re.sub(r'[^0-9.]', '', tax_rate_str)
        if not tax_rate_str:
            tax_rate_str = '18'
        tax_rate = Decimal(tax_rate_str)
        # Clean and validate discount_rate input
        discount_rate_str = request.POST.get('discount_rate', '5')
        # Remove common problematic characters
        discount_rate_str = discount_rate_str.replace('%', '').replace('&#39;', '').replace("'", '').strip()
        # Extract only numeric characters and decimal point
        discount_rate_str = re.sub(r'[^0-9.]', '', discount_rate_str)
        if not discount_rate_str:
            discount_rate_str = '5'
        discount_rate = Decimal(discount_rate_str)
        
        try:
            order = Order.objects.get(id=order_id)
            product = Product.objects.get(product_id=product_id)
            invoice = Invoice.objects.get(order=order)
            
            # Check if product already exists in invoice
            if invoice.items.filter(product_name=product.name).exists():
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': 'Product already added to invoice'})
                messages.error(request, 'Product already added to invoice')
                return redirect('bio_details:invoice_detail', order_id=order_id)
            
            # Check stock
            if product.current_stock < quantity:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': f'Insufficient stock! Only {product.current_stock} units available.'})
                messages.error(request, f"Insufficient stock! Only {product.current_stock} units available.")
                return redirect('bio_details:invoice_detail', order_id=order_id)
            
            # IMPORTANT: Convert product price to invoice currency
            from .currency_utils import convert_currency
            invoice_currency_code = invoice.currency.country.code if invoice.currency else 'IN'
            converted_price = Decimal(str(convert_currency(float(product.rate), 'IN', invoice_currency_code)))
            
            # Create order item with converted price
            order_item = OrderItem.objects.create(
                order=order,
                product_name=product.name,
                price=converted_price,  # Use converted price
                quantity=quantity
            )
            
            # Create invoice item with custom tax and discount using converted price
            item_subtotal = converted_price * quantity
            item_tax_amount = (item_subtotal * tax_rate) / Decimal('100')
            item_discount_amount = (item_subtotal * discount_rate) / Decimal('100')
            item_total = item_subtotal + item_tax_amount - item_discount_amount
            
            invoice_item = InvoiceItem.objects.create(
                invoice=invoice,
                product_name=product.name,
                qty=quantity,
                unit_price=converted_price,  # Use converted price
                tax=tax_rate,
                discount=item_discount_amount,
                total=item_total
            )
            
            # Update product stock
            product.current_stock -= quantity
            product.save()
            
            # Recalculate invoice totals
            invoice_items = invoice.items.all()
            invoice.subtotal = sum(item.unit_price * item.qty for item in invoice_items)
            invoice.total_tax = sum((item.unit_price * item.qty * item.tax) / Decimal('100') for item in invoice_items)
            invoice.total_discount = sum(item.discount for item in invoice_items)
            invoice.total_amount = invoice.subtotal + invoice.total_tax - invoice.total_discount
            
            # Update order total
            order.total_amount = invoice.total_amount
            order.save()
            invoice.save()
            
            # Return JSON response for AJAX
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # IMPORTANT: Convert all totals to the invoice currency before sending
                from .currency_utils import convert_currency
                
                # Convert totals to invoice currency (they should already be in invoice currency, but ensure consistency)
                converted_subtotal = invoice.subtotal
                converted_total_tax = invoice.total_tax
                converted_total_discount = invoice.total_discount
                converted_total_amount = invoice.total_amount
                
                return JsonResponse({
                    'success': True,
                    'item': {
                        'id': invoice_item.id,
                        'product_name': invoice_item.product_name,
                        'unit_price': str(invoice_item.unit_price),
                        'qty': invoice_item.qty,
                        'tax': str(item_tax_amount),
                        'discount': str(invoice_item.discount),
                        'total': str(invoice_item.total),
                        'currency_symbol': invoice.currency_symbol
                    },
                    'subtotal': str(converted_subtotal),
                    'total_tax': str(converted_total_tax),
                    'total_discount': str(converted_total_discount),
                    'total_amount': str(converted_total_amount),
                    'currency_symbol': invoice.currency_symbol
                })
            
            messages.success(request, f"{product.name} added to invoice successfully!")
            
        except (Order.DoesNotExist, Product.DoesNotExist, Invoice.DoesNotExist):
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Order, Product or Invoice not found!'})
            messages.error(request, "Order, Product or Invoice not found!")
    
    return redirect('bio_details:invoice_detail', order_id=order_id)


def add_product_to_invoice_ajax(request, order_id):
    if not request.user.is_authenticated:
        return redirect('bio_details:login')
    
    if request.method == 'POST':
        
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = int(data.get('quantity', 1))
            
            order = Order.objects.get(id=order_id)
            product = Product.objects.get(product_id=product_id)
            invoice = Invoice.objects.get(order=order)
            
            # Check if product already exists in invoice
            if invoice.items.filter(product_name=product.name).exists():
                return JsonResponse({'success': False, 'message': 'Product already added to invoice'})
            
            # Check stock
            if product.current_stock < quantity:
                return JsonResponse({'success': False, 'message': f'Insufficient stock! Only {product.current_stock} units available.'})
            
            # Create order item
            order_item = OrderItem.objects.create(
                order=order,
                product_name=product.name,
                price=product.rate,
                quantity=quantity
            )
            
            # Create invoice item
            from decimal import Decimal
            item_subtotal = product.rate * quantity
            item_tax = (item_subtotal * Decimal('18')) / Decimal('100')
            product_discount_amount = (item_subtotal * product.discount) / Decimal('100')
            item_total = item_subtotal + item_tax - product_discount_amount
            
            InvoiceItem.objects.create(
                invoice=invoice,
                product_name=product.name,
                qty=quantity,
                unit_price=product.rate,
                tax=Decimal('18.00'),
                discount=product_discount_amount,
                total=item_total
            )
            
            # Update product stock
            product.current_stock -= quantity
            product.save()
            
            # Recalculate invoice totals
            invoice_items = invoice.items.all()
            invoice.subtotal = sum(item.unit_price * item.qty for item in invoice_items)
            invoice.total_tax = sum((item.unit_price * item.qty * item.tax) / Decimal('100') for item in invoice_items)
            invoice.total_discount = sum(item.discount for item in invoice_items)
            invoice.total_amount = invoice.subtotal + invoice.total_tax - invoice.total_discount
            
            # Update order total
            order.total_amount = invoice.total_amount
            order.save()
            invoice.save()
            
            return JsonResponse({
                'success': True, 
                'message': f'{product.name} added successfully!',
                'subtotal': str(invoice.subtotal),
                'total_tax': str(invoice.total_tax),
                'total_discount': str(invoice.total_discount),
                'total_amount': str(invoice.total_amount)
            })
            
        except (Order.DoesNotExist, Product.DoesNotExist, Invoice.DoesNotExist):
            return JsonResponse({'success': False, 'message': 'Order, Product or Invoice not found!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def place_order(request):
    if not request.user.is_authenticated:
        return redirect('bio_details:login')
    
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        
        try:
            order = Order.objects.get(id=order_id)
            invoice = Invoice.objects.get(order=order)
            
            # Check if invoice has items
            if not invoice.items.exists():
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': 'Cannot place order without items'})
                messages.error(request, "Cannot place order without items")
                return redirect('bio_details:invoice_detail', order_id=order_id)
            
            # Update invoice payment status
            invoice.payment_status = 'pending'
            invoice.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True, 
                    'message': f'Order {order.order_id} placed successfully!',
                    'redirect_url': '/my-orders/'
                })
            
            messages.success(request, f"Order {order.order_id} placed successfully!")
            return redirect('bio_details:my_orders')
            
        except (Order.DoesNotExist, Invoice.DoesNotExist):
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Order or Invoice not found!'})
            messages.error(request, "Order or Invoice not found!")
            return redirect('bio_details:my_orders')
    
    return redirect('bio_details:my_orders')


def cancel_order(request):
    if not request.user.is_authenticated:
        return redirect('bio_details:login')
    
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        
        try:
            order = Order.objects.get(id=order_id)
            invoice = Invoice.objects.get(order=order)
            
            # Restore stock for all items
            for invoice_item in invoice.items.all():
                try:
                    product = Product.objects.get(name=invoice_item.product_name)
                    product.current_stock += invoice_item.qty
                    product.save()
                except Product.DoesNotExist:
                    pass
            
            # Delete invoice and order
            invoice.delete()
            order.delete()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Order cancelled successfully!',
                    'redirect_url': '/cart/'
                })
            
            messages.success(request, "Order cancelled successfully!")
            return redirect('bio_details:cart_view')
            
        except (Order.DoesNotExist, Invoice.DoesNotExist):
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Order or Invoice not found!'})
            messages.error(request, "Order or Invoice not found!")
            return redirect('bio_details:cart_view')
    
    return redirect('bio_details:cart_view')


def update_payment_method(request, invoice_id):
    if not request.user.is_authenticated:
        return redirect('bio_details:login')
    
    if request.method == 'POST':
        from django.http import JsonResponse
        import json
        
        try:
            data = json.loads(request.body)
            payment_method = data.get('payment_method', 'cash')
            
            invoice = Invoice.objects.get(id=invoice_id)
            invoice.payment_method = payment_method
            invoice.save()
            
            return JsonResponse({'success': True, 'message': 'Payment method updated successfully'})
            
        except Invoice.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invoice not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def remove_invoice_item(request, item_id):
    if not request.user.is_authenticated:
        return redirect('bio_details:login')
    

    print(f"Remove item request - Method: {request.method}, Item ID: {item_id}")
    
    if request.method == 'POST':
        try:
            from decimal import Decimal
            item = InvoiceItem.objects.get(id=item_id)
            invoice = item.invoice
            
            print(f"Found item: {item.product_name}, Quantity: {item.qty}")
            
            # Restore stock
            try:
                product = Product.objects.get(name=item.product_name)
                product.current_stock += item.qty
                product.save()
                print(f"Stock restored for {product.name}: {product.current_stock}")
            except Product.DoesNotExist:
                print(f"Product not found: {item.product_name}")
                pass
            
            # Remove item
            item.delete()
            print("Item deleted successfully")
            
            # Recalculate invoice totals
            invoice_items = invoice.items.all()
            if invoice_items.exists():
                invoice.subtotal = sum(item.unit_price * item.qty for item in invoice_items)
                invoice.total_tax = sum((item.unit_price * item.qty * item.tax) / Decimal('100') for item in invoice_items)
                invoice.total_discount = sum(item.discount for item in invoice_items)
                invoice.total_amount = invoice.subtotal + invoice.total_tax - invoice.total_discount
                
                # Update order total
                order = invoice.order
                order.total_amount = invoice.total_amount
                order.save()
                invoice.save()
                
                print(f"Invoice updated - Total: {invoice.total_amount}")
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'message': 'Item removed successfully!',
                        'subtotal': str(invoice.subtotal),
                        'total_tax': str(invoice.total_tax),
                        'total_discount': str(invoice.total_discount),
                        'total_amount': str(invoice.total_amount),
                        'currency_symbol': invoice.currency_symbol
                    })
                
                messages.success(request, 'Item removed successfully!')
                return redirect('bio_details:invoice_detail', order_id=invoice.order.id)
            else:
                # If no items left, delete the entire order
                order = invoice.order
                invoice.delete()
                order.delete()
                
                print("Last item removed, order cancelled")
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'message': 'Item removed successfully! Order cancelled as no items remain.',
                        'redirect': True,
                        'redirect_url': '/cart/'
                    })
                
                messages.success(request, 'Item removed successfully! Order cancelled as no items remain.')
                return redirect('bio_details:cart_view')
                
        except InvoiceItem.DoesNotExist:
            print(f"InvoiceItem not found: {item_id}")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Item not found!'})
            messages.error(request, 'Item not found!')
            return redirect('bio_details:order')
        except Exception as e:
            print(f"Error removing item: {str(e)}")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': f'Error removing item: {str(e)}'})
            messages.error(request, f'Error removing item: {str(e)}')
            return redirect('bio_details:order')
    
    print("Invalid request method")
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    return redirect('bio_details:order')



def my_orders(request):
    if not request.user.is_authenticated:
        return redirect('bio_details:login')
    
    # Get orders for the current user
    search = request.GET.get('search')
    per_page = request.GET.get('per_page', 5)
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 5
    
    user_orders = Order.objects.filter(user=request.user).select_related('invoice').prefetch_related('items', 'invoice__items').order_by('created_at')
    
    if search:
        user_orders = user_orders.filter(
            models.Q(order_id__icontains=search) |
            models.Q(invoice__invoice_number__icontains=search)
        )
    
    paginator = Paginator(user_orders, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'my_orders.html', {
        'page_obj': page_obj,
    })

def get_product_stock(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Not authenticated'})
    
    product_name = request.GET.get('product_name')
    if not product_name:
        return JsonResponse({'success': False, 'error': 'Product name required'})
    
    try:
        product = Product.objects.get(name=product_name)
        return JsonResponse({
            'success': True,
            'current_stock': product.current_stock,
            'product_name': product.name
        })
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Product not found'})


def update_invoice_item_qty(request, item_id):
    if not request.user.is_authenticated:
        return redirect('bio_details:login')
    
    if request.method == 'POST':
        try:
            print(f"=== UPDATE REQUEST FOR ITEM {item_id} ===")
            
            # Get the invoice item
            item = InvoiceItem.objects.get(id=item_id)
            print(f"Original product: {item.product_name}")
            
            # Get form data
            quantity = int(request.POST.get('quantity', 1))
            product_changed = request.POST.get('product_changed', 'false')
            
            print(f"Quantity: {quantity}")
            print(f"Product changed: {product_changed}")
            
            # Store original product for comparison
            original_product_name = item.product_name
            
            # Check if product was changed
            if product_changed == 'true':
                new_product_id = request.POST.get('product_id')
                print(f"New product ID: {new_product_id}")
                
                if new_product_id:
                    try:
                        # Get the new product
                        new_product = Product.objects.get(product_id=new_product_id)
                        print(f"Found new product: {new_product.name}")
                        
                        # CRITICAL: Convert price to invoice currency
                        from .currency_utils import convert_currency
                        from decimal import Decimal
                        invoice_currency_code = item.invoice.currency.country.code if item.invoice.currency else 'IN'
                        converted_price = Decimal(str(convert_currency(float(new_product.rate), 'IN', invoice_currency_code)))
                        
                        # CRITICAL: Update the invoice item with new product
                        from decimal import Decimal
                        item.product_name = new_product.name
                        item.unit_price = converted_price  # Use converted price
                        
                        print(f"Updated product from '{original_product_name}' to '{new_product.name}'")
                        print(f"Converted price from {new_product.rate} to {converted_price} for currency {item.invoice.currency}")
                        
                        # Get tax and discount from form or product defaults
                        from decimal import Decimal
                        tax_rate = Decimal(str(request.POST.get('tax_rate', new_product.get_tax_rate('IN') or 18)))
                        discount_rate = Decimal(str(request.POST.get('discount_rate', new_product.discount or 0)))
                        
                    except Product.DoesNotExist:
                        print(f"Product with ID {new_product_id} not found")
                        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                            return JsonResponse({
                                'success': False,
                                'error': f'Product with ID {new_product_id} not found'
                            })
                        messages.error(request, f'Product with ID {new_product_id} not found')
                        return redirect('bio_details:invoice_detail', order_id=item.invoice.order.id)
                else:
                    print("No product ID provided for product change")
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({
                            'success': False,
                            'error': 'No product ID provided'
                        })
                    messages.error(request, 'No product ID provided')
                    return redirect('bio_details:invoice_detail', order_id=item.invoice.order.id)
            else:
                # Just update quantity, keep same product
                from decimal import Decimal
                tax_rate = Decimal(str(request.POST.get('tax_rate', 18)))
                discount_rate = Decimal(str(request.POST.get('discount_rate', 0)))
                print("Only updating quantity, keeping same product")
            
            # Update quantity
            item.qty = quantity
            
            # Recalculate amounts
            from decimal import Decimal
            subtotal = Decimal(str(item.unit_price)) * quantity
            tax_amount = (subtotal * Decimal(str(tax_rate))) / Decimal('100')
            discount_amount = (subtotal * Decimal(str(discount_rate))) / Decimal('100')
            total = subtotal + tax_amount - discount_amount
            
            # Update calculated fields
            item.tax = Decimal(str(tax_rate))
            item.discount = discount_amount
            item.total = total
            
            print(f"Calculated values:")
            print(f"  Unit Price: {item.unit_price}")
            print(f"  Quantity: {item.qty}")
            print(f"  Tax Amount: {tax_amount}")
            print(f"  Discount: {discount_amount}")
            print(f"  Total: {total}")
            
            # CRITICAL: Save the changes to database
            item.save()
            print(f"SAVED TO DATABASE: {item.product_name}, Qty: {item.qty}")
            
            # Verify the save worked
            saved_item = InvoiceItem.objects.get(id=item_id)
            print(f"VERIFICATION - Saved product name: {saved_item.product_name}")
            print(f"VERIFICATION - Saved quantity: {saved_item.qty}")
            
            # Recalculate invoice totals
            invoice = item.invoice
            invoice_items = invoice.items.all()
            
            invoice_subtotal = sum(Decimal(str(item.unit_price)) * item.qty for item in invoice_items)
            invoice_total_tax = sum((Decimal(str(item.unit_price)) * item.qty * item.tax) / Decimal('100') for item in invoice_items)
            invoice_total_discount = sum(item.discount for item in invoice_items)
            invoice_total_amount = invoice_subtotal + invoice_total_tax - invoice_total_discount
            
            # Update invoice totals
            invoice.subtotal = invoice_subtotal
            invoice.total_tax = invoice_total_tax
            invoice.total_discount = invoice_total_discount
            invoice.total_amount = invoice_total_amount
            
            # CRITICAL: Save invoice totals
            invoice.save()
            print(f"SAVED INVOICE TOTALS")
            
            # Prepare response data
            response_data = {
                'success': True,
                'item_unit_price': f"{item.unit_price:.2f}",
                'item_tax_amount': f"{tax_amount:.2f}",
                'item_discount': f"{item.discount:.2f}",
                'item_total': f"{item.total:.2f}",
                'subtotal': f"{invoice_subtotal:.2f}",
                'total_tax': f"{invoice_total_tax:.2f}",
                'total_discount': f"{invoice_total_discount:.2f}",
                'total_amount': f"{invoice_total_amount:.2f}",
                'currency_symbol': invoice.currency_symbol or '₹',
                'message': f'Product updated successfully. Changed from "{original_product_name}" to "{item.product_name}"' if product_changed == 'true' else 'Quantity updated successfully'
            }
            
            print(f"=== RESPONSE DATA ===")
            print(json.dumps(response_data, indent=2))
            print(f"=== END UPDATE ===")
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(response_data)
            
            messages.success(request, response_data['message'])
            return redirect('bio_details:invoice_detail', order_id=item.invoice.order.id)
            
        except InvoiceItem.DoesNotExist:
            print(f"InvoiceItem not found: {item_id}")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Item not found'})
            messages.error(request, 'Item not found')
            return redirect('bio_details:order')
        except ValueError as e:
            print(f"ValueError in update_invoice_item_qty: {str(e)}")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Invalid quantity or data'})
            messages.error(request, 'Invalid quantity or data')
            return redirect('bio_details:order')
        except Exception as e:
            print(f"ERROR in update_invoice_item_qty: {str(e)}")
            import traceback
            traceback.print_exc()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': f'Server error: {str(e)}'
                })
            messages.error(request, f'Server error: {str(e)}')
            return redirect('bio_details:order')
    
    return redirect('bio_details:order')


def delete_order(request, order_id):
    if not request.user.is_authenticated:
        return redirect('bio_details:login')
    
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('bio_details:dashboard')
    
    try:
        order = Order.objects.get(id=order_id)
        
        # Restore stock for all items if invoice exists
        try:
            invoice = Invoice.objects.get(order=order)
            for invoice_item in invoice.items.all():
                try:
                    product = Product.objects.get(name=invoice_item.product_name)
                    product.current_stock += invoice_item.qty
                    product.save()
                except Product.DoesNotExist:
                    pass
            invoice.delete()
        except Invoice.DoesNotExist:
            pass
        
        # Delete the order
        order.delete()
        messages.success(request, "Order deleted successfully!", extra_tags="delete-toast")
        
    except Order.DoesNotExist:
        messages.error(request, "Order not found!", extra_tags="delete-toast")
    
    # Preserve current page parameters when redirecting
    if request.GET:
        query_params = request.GET.urlencode()
        return redirect(f"/order/?{query_params}")
    
    return redirect('bio_details:order')


def save_terms_conditions(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Not authenticated'})
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            invoice_id = data.get('invoice_id')
            terms_conditions = data.get('terms_conditions', [])
            
            invoice = Invoice.objects.get(id=invoice_id)
            invoice.terms_conditions = terms_conditions
            invoice.save()
            
            return JsonResponse({'success': True, 'message': 'Terms & Conditions saved successfully'})
            
        except Invoice.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Invoice not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def get_order_items(request, order_id):
    """AJAX endpoint to fetch order items for the invoice modal"""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Not authenticated'})
    
    try:
        order = Order.objects.get(id=order_id)
        invoice = Invoice.objects.get(order=order)
        
        items_data = []
        for i, item in enumerate(invoice.items.all(), 1):
            items_data.append({
                'sno': i,
                'product_name': item.product_name,
                'unit_price': f"{item.unit_price:.2f}",
                'qty': item.qty,
                'tax': str(item.tax),
                'tax_amount': f"{item.tax_amount:.2f}",
                'discount': f"{item.discount:.2f}",
                'total': f"{item.total:.2f}"
            })
        
        return JsonResponse({
            'success': True,
            'items': items_data,
            'subtotal': f"{invoice.subtotal:.2f}",
            'total_tax': f"{invoice.total_tax:.2f}",
            'total_discount': f"{invoice.total_discount:.2f}",
            'total_amount': f"{invoice.total_amount:.2f}"
        })
        
    except (Order.DoesNotExist, Invoice.DoesNotExist):
        return JsonResponse({'success': False, 'error': 'Order or Invoice not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def convert_product_currency(request):
    """AJAX endpoint to convert product prices using live rates and store currency in session"""
    if request.method == 'GET':
        country = request.GET.get('country', 'IN')
        
        try:
            # Store selected currency in session
            currency_info = get_currency_info(country)
            request.session['selected_currency'] = country
            request.session['currency_symbol'] = currency_info['symbol']
            request.session['currency_code'] = currency_info['code']
            
            # Get live exchange rates
            from .currency_utils import get_live_exchange_rates
            live_rates = get_live_exchange_rates()
            
            products = Product.objects.all()
            converted_products = []
            
            for product in products:
                converted_rate = convert_currency(float(product.rate), 'IN', country)
                converted_products.append({
                    'product_id': product.product_id,
                    'name': product.name,
                    'original_rate': float(product.rate),
                    'converted_rate': converted_rate,
                    'currency_symbol': currency_info['symbol'],
                    'currency_code': currency_info['code']
                })
            
            return JsonResponse({
                'success': True,
                'products': converted_products,
                'currency': currency_info,
                'live_rates_used': True,
                'rates_source': 'ExchangeRate API',
                'rates': live_rates  # Include live rates for client-side fallback
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def print_invoice(request, order_id):
    if not request.user.is_authenticated:
        return redirect('bio_details:login')
    
    try:
        order = Order.objects.get(id=order_id)
        invoice = Invoice.objects.get(order=order)
        
        # Check access permissions
        if order.user != request.user and not request.user.is_superuser:
            messages.error(request, "Access denied.")
            return redirect('bio_details:my_orders')
        
        # Get terms conditions from invoice or use defaults
        terms_conditions = invoice.terms_conditions if hasattr(invoice, 'terms_conditions') and invoice.terms_conditions else [
            "Payment is due within 30 days from the invoice date",
            "Late payment charges may apply as per company policy   ",
            "Goods once sold cannot be returned or exchanged",
            "All disputes are subject to local jurisdiction",
            "Any damages or issues must be reported within 3 days of delivery",
            "The company is not responsible for delays caused by unforeseen circumstances",
            "Warranty or support will be provided only as per agreed terms",
        ]
        
        # Import and use number to words converter
        from .utils import number_to_words
        total_amount_words = number_to_words(invoice.total_amount, invoice.currency.code  )
        
        context = {
            'invoice_number': invoice.invoice_number,
            'invoice_date': invoice.invoice_date,
            'customer_name': invoice.customer_name,
            'customer_email': order.user.email,
            'customer_phone': getattr(order.user.member, 'phone', '+91 9876543210') if hasattr(order.user, 'member') else '+91 9876543210',
            'items': invoice.items.all(),
            'subtotal': invoice.subtotal,
            'total_tax': invoice.total_tax,
            'total_discount': invoice.total_discount,
            'total_amount': invoice.total_amount,
            'total_amount_words': total_amount_words,
            'total_qty': sum(item.qty for item in invoice.items.all()),
            'terms_conditions': terms_conditions,
            'currency_symbol': invoice.currency.symbol,
            'currency_name': invoice.currency.name,
            'selected_currency': invoice.currency.code,
            'customer': {
                'country': {
                    'name': invoice.country.name if invoice.country else 'India'
                }
            },
            'customer_country_name': invoice.country.name if invoice.country else 'India'
        }
        
        return render(request, 'print_invoice.html', context)
        
    except (Order.DoesNotExist, Invoice.DoesNotExist):
        messages.error(request, "Invoice not found!")
        return redirect('bio_details:my_orders')


def my_profile_user(request):
    if not request.user.is_authenticated:
        return redirect('bio_details:login')
    
    if request.method == 'POST':
        try:
            # Update user fields
            if request.POST.get('full_name'):
                names = request.POST.get('full_name').split(' ', 1)
                request.user.first_name = names[0]
                request.user.last_name = names[1] if len(names) > 1 else ''
                # Also update username to the full name
                request.user.username = request.POST.get('full_name')
            
            if request.POST.get('email'):
                request.user.email = request.POST.get('email')
            
            request.user.save()
            
            # Update member fields
            try:
                customer = request.user.customer
            except Customer.DoesNotExist:
                # Create member if doesn't exist
                customer = Customer.objects.create(
                    user=request.user,
                    phone='',
                    city='',
                    state='',
                    gender='',
                    designation=''
                )
            
            if request.POST.get('phone'):
                customer.phone = request.POST.get('phone')
            if request.POST.get('gender'):
                customer.gender = request.POST.get('gender')
            if request.POST.get('date_of_birth'):
                customer.date_of_birth = request.POST.get('date_of_birth')
            if request.POST.get('city'):
                customer.city = request.POST.get('city')
            if request.POST.get('state'):
                customer.state = request.POST.get('state')
            if request.POST.get('pincode'):
                customer.pincode = request.POST.get('pincode')
            if request.POST.get('address1'):
                customer.address = request.POST.get('address1')
            if request.POST.get('bank_name'):
                customer.bank_name = request.POST.get('bank_name')
            if request.POST.get('account_number'):
                customer.account_number = request.POST.get('account_number')
            if request.POST.get('ifsc_code'):
                customer.ifsc_code = request.POST.get('ifsc_code')
            if request.POST.get('pan_num'):
                customer.pan_num = request.POST.get('pan_num')
            
            # Handle profile picture upload
            if request.FILES.get('profile_pic'):
                customer.profile_pic = request.FILES.get('profile_pic')
            
            customer.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Profile updated successfully'})
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('bio_details:my_profile_user')
            
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': str(e)})
            
            messages.error(request, f'Error updating profile: {str(e)}')
    
    return render(request, 'myprofile_user.html')



def my_profile(request):
    if not request.user.is_authenticated:
        return redirect('bio_details:login')
    
    if request.method == 'POST':
        try:
            # Update user fields
            if request.POST.get('full_name'):
                names = request.POST.get('full_name').split(' ', 1)
                request.user.first_name = names[0]
                request.user.last_name = names[1] if len(names) > 1 else ''
                # Also update username to the full name
                request.user.username = request.POST.get('full_name')
            
            if request.POST.get('email'):
                request.user.email = request.POST.get('email')
            
            request.user.save()
            
            # Update member fields
            try:
                member = request.user.member
            except Member.DoesNotExist:
                # Create member if doesn't exist
                member = Member.objects.create(
                    user=request.user,
                    phone='',
                    city='',
                    state='',
                    gender='',
                    designation=''
                )
            
            if request.POST.get('phone'):
                member.phone = request.POST.get('phone')
            if request.POST.get('designation'):
                member.designation = request.POST.get('designation')
            if request.POST.get('gender'):
                member.gender = request.POST.get('gender')
            if request.POST.get('date_of_birth'):
                member.date_of_birth = request.POST.get('date_of_birth')
            if request.POST.get('city'):
                member.city = request.POST.get('city')
            if request.POST.get('state'):
                member.state = request.POST.get('state')
            if request.POST.get('pincode'):
                member.pincode = request.POST.get('pincode')
            if request.POST.get('address1'):
                member.address1 = request.POST.get('address1')
            if request.POST.get('bank_name'):
                member.bank_name = request.POST.get('bank_name')
            if request.POST.get('account_number'):
                member.account_number = request.POST.get('account_number')
            if request.POST.get('ifsc_code'):
                member.ifsc_code = request.POST.get('ifsc_code')
            if request.POST.get('pan_num'):
                member.pan_num = request.POST.get('pan_num')
            
            # Handle profile picture upload
            if request.FILES.get('profile_pic'):
                member.profile_pic = request.FILES.get('profile_pic')
            
            member.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Profile updated successfully'})
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('bio_details:my_profile')
            
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': str(e)})
            
            messages.error(request, f'Error updating profile: {str(e)}')
    
    return render(request, 'my_profile.html')


def save_country_selection(request):
    """Save selected country to session"""
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            country = data.get('country', 'IN')
            request.session['selected_country'] = country
            return JsonResponse({'success': True, 'message': 'Country saved'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def save_currency_selection(request):
    """Save selected currency to session"""
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            currency = data.get('currency', 'IN')
            request.session['selected_currency'] = currency
            
            # Also get currency symbol and save it
            from .models import Currency, Country
            try:
                country_obj = Country.objects.get(code=currency, is_active=True)
                currency_obj = Currency.objects.get(country=country_obj, is_active=True)
                request.session['currency_symbol'] = currency_obj.symbol
            except (Currency.DoesNotExist, Country.DoesNotExist):
                request.session['currency_symbol'] = '₹'
            
            return JsonResponse({'success': True, 'message': 'Currency saved'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})



def attendance(request):
    if not request.user.is_authenticated:
        return redirect('bio_details:login')
    
    if hasattr(request.user, 'member') and request.user.member.role == 'user':
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('bio_details:product_view')
        
    # Import required modules at the top
    from django.contrib.auth.models import User
    from datetime import datetime, timedelta, date as date_obj
    from django.db.models import Count, Avg
    
    # Handle form submissions
    if request.method == 'POST':
        print(f"DEBUG: POST request received")
        print(f"DEBUG: POST data: {request.POST}")
        
        form_type = request.POST.get('form_type')
        print(f"DEBUG: Form type: {form_type}")
        
        if form_type == 'attendance':
            # Handle attendance marking
            employee_id = request.POST.get('employee_id')
            date = request.POST.get('date')
            status = request.POST.get('status')
            check_in = request.POST.get('check_in') or None
            check_out = request.POST.get('check_out') or None
            notes = request.POST.get('notes', '')
            
            print(f"DEBUG: Attendance data - Employee: {employee_id}, Date: {date}, Status: {status}, Check-in: {check_in}, Check-out: {check_out}")
            
            # Get the employee user - for regular users, only allow marking their own attendance
            if request.user.is_superuser or (hasattr(request.user, 'member') and request.user.member.is_hr_or_admin()):
                # Admin and HR can mark attendance for any employee
                if employee_id:
                    try:
                        employee_user = User.objects.get(id=employee_id)
                    except User.DoesNotExist:
                        messages.error(request, 'Employee not found!')
                        return redirect('bio_details:attendance')
                else:
                    messages.error(request, 'Please select an employee!')
                    return redirect('bio_details:attendance')
            else:
                # Regular users can only mark their own attendance
                employee_user = request.user
            
            # Validate that only today's date can be marked
            from datetime import date as date_obj, datetime
            today = date_obj.today()
            selected_date = datetime.strptime(date, '%Y-%m-%d').date()
            
            if selected_date != today:
                messages.error(request, 'You can only mark attendance for today!')
                return redirect('bio_details:attendance')
            
            # Check if this date has approved leave
            approved_leave = LeaveApplication.objects.filter(
                user=employee_user,
                status='approved',
                from_date__lte=selected_date,
                to_date__gte=selected_date
            ).first()
            
            if approved_leave:
                messages.error(request, f'{employee_user.get_full_name() or employee_user.username} has approved leave on {selected_date.strftime("%d %B %Y")} ({approved_leave.leave_type.title()} Leave from {approved_leave.from_date.strftime("%d %B")} to {approved_leave.to_date.strftime("%d %B %Y")}). Cannot mark attendance on leave day.')
                return redirect('bio_details:attendance')
            
            # Check if this date has pending leave application
            pending_leave = LeaveApplication.objects.filter(
                user=employee_user,
                status='pending',
                from_date__lte=selected_date,
                to_date__gte=selected_date
            ).first()
            
            if pending_leave:
                messages.error(request, f'{employee_user.get_full_name() or employee_user.username} has a pending leave application for {selected_date.strftime("%d %B %Y")} ({pending_leave.leave_type.title()} Leave from {pending_leave.from_date.strftime("%d %B")} to {pending_leave.to_date.strftime("%d %B %Y")}). Cannot mark attendance while leave application is pending.')
                return redirect('bio_details:attendance')
            
            try:
                # Check if attendance already exists for this date
                existing_attendance = Attendance.objects.filter(
                    user=employee_user,
                    date=date
                ).first()
                
                if existing_attendance:
                    # Check if user has permission to update existing attendance
                    can_update = False
                    
                    # Only HR, Admin, or Superuser can update existing attendance
                    if request.user.is_superuser:
                        can_update = True
                    elif hasattr(request.user, 'member') and request.user.member.is_hr_or_admin():
                        can_update = True
                    
                    if not can_update:
                        messages.error(request, f'Attendance for {employee_user.get_full_name() or employee_user.username} on {selected_date.strftime("%d %B %Y")} already exists. Only HR can update existing attendance records.')
                        return redirect('bio_details:attendance')
                    
                    # Update existing record (HR/Admin only)
                    existing_attendance.status = status
                    existing_attendance.check_in = check_in
                    existing_attendance.check_out = check_out
                    existing_attendance.save()
                    print(f"DEBUG: Updated existing attendance record by HR/Admin")
                    messages.success(request, f'Attendance updated successfully for {employee_user.get_full_name() or employee_user.username}!')
                else:
                    # Create new attendance record
                    attendance_record = Attendance.objects.create(
                        user=employee_user,
                        date=date,
                        status=status,
                        check_in=check_in,
                        check_out=check_out
                    )
                    print(f"DEBUG: Created new attendance record")
                    messages.success(request, f'Attendance marked successfully for {employee_user.get_full_name() or employee_user.username}!')
                
                return redirect('bio_details:attendance')  # Redirect to prevent resubmission
                    
            except Exception as e:
                print(f"DEBUG: Error marking attendance: {str(e)}")
                import traceback
                traceback.print_exc()
                messages.error(request, f'Error marking attendance: {str(e)}')
                return redirect('bio_details:attendance')  # Redirect even on error
        
        elif form_type == 'leave':
            # Handle leave application
            employee_id = request.POST.get('employee_id')
            leave_type = request.POST.get('leave_type')
            duration = request.POST.get('duration')
            from_date = request.POST.get('from_date')
            to_date = request.POST.get('to_date')
            reason = request.POST.get('reason')
            
            print(f"DEBUG: Leave data - Employee: {employee_id}, Type: {leave_type}, Duration: {duration}, From: {from_date}, To: {to_date}")
            
            # Get the employee user (for superusers and HR) or use current user
            if (request.user.is_superuser or (hasattr(request.user, 'member') and request.user.member.is_hr_or_admin())) and employee_id:
                try:
                    employee_user = User.objects.get(id=employee_id)
                except User.DoesNotExist:
                    messages.error(request, 'Employee not found!')
                    return redirect('bio_details:attendance')
            else:
                employee_user = request.user
            
            try:
                # Check for overlapping leave applications
                from datetime import datetime
                from_date_obj = datetime.strptime(from_date, '%Y-%m-%d').date()
                to_date_obj = datetime.strptime(to_date, '%Y-%m-%d').date()
                
                overlapping_leaves = LeaveApplication.objects.filter(
                    user=employee_user,
                    status__in=['pending', 'approved'],
                    from_date__lte=to_date_obj,
                    to_date__gte=from_date_obj
                )
                
                if overlapping_leaves.exists():
                    messages.error(request, f'{employee_user.get_full_name() or employee_user.username} already has a leave application for overlapping dates!')
                    return redirect('bio_details:attendance')
                
                # Check if there are existing attendance records for the leave dates and delete them
                existing_attendance = Attendance.objects.filter(
                    user=employee_user,
                    date__gte=from_date_obj,
                    date__lte=to_date_obj
                )
                
                deleted_count = existing_attendance.count()
                if deleted_count > 0:
                    existing_attendance.delete()
                    print(f"DEBUG: Deleted {deleted_count} attendance records for leave dates")
                
                leave_application = LeaveApplication.objects.create(
                    user=employee_user,
                    leave_type=leave_type,
                    duration=duration,
                    from_date=from_date_obj,
                    to_date=to_date_obj,
                    reason=reason
                )
                print(f"DEBUG: Created leave application")
                
                success_message = f'Leave application submitted successfully for {employee_user.get_full_name() or employee_user.username}!'
                if deleted_count > 0:
                    success_message += f' Existing attendance records ({deleted_count} days) have been removed.'
                
                messages.success(request, success_message)
                return redirect('bio_details:attendance')  # Redirect to prevent resubmission
                
            except Exception as e:
                print(f"DEBUG: Error submitting leave application: {str(e)}")
                import traceback
                traceback.print_exc()
                messages.error(request, f'Error submitting leave application: {str(e)}')
                return redirect('bio_details:attendance')  # Redirect even on error
    
    # Get current user as the only employee (unless admin wants to see all)
    # For regular users, show only themselves. For admins and HR, show all employees with 'employee' role only
    if request.user.is_superuser:
        # Admin can see all employees with 'employee' role only
        employees = User.objects.filter(
            member__isnull=False,
            member__account_status=True,
            member__role='employee'  # Only show employees
        ).select_related('member').order_by('first_name', 'last_name', 'username')
    elif hasattr(request.user, 'member') and request.user.member.is_hr_or_admin():
        # HR can see all employees with 'employee' role only
        employees = User.objects.filter(
            member__isnull=False,
            member__account_status=True,
            member__role='employee'  # Only show employees
        ).select_related('member').order_by('first_name', 'last_name', 'username')
    else:
        # Regular users see only themselves if they have employee role
        if hasattr(request.user, 'member') and request.user.member.role == 'employee':
            employees = User.objects.filter(id=request.user.id).select_related('member')
        else:
            employees = User.objects.none()  # Empty QuerySet if user doesn't have employee role
    
    # Add today's attendance status and leave information to each employee
    today = date_obj.today()
    current_month = today.month
    current_year = today.year
    
    for employee in employees:
        # Check today's attendance
        today_attendance = Attendance.objects.filter(
            user=employee,
            date=today
        ).first()
        
        # Check if employee has approved leave today
        today_leave = LeaveApplication.objects.filter(
            user=employee,
            status='approved',
            from_date__lte=today,
            to_date__gte=today
        ).first()
        
        if today_leave:
            employee.today_status = 'leave'
            employee.leave_info = {
                'type': today_leave.leave_type,
                'from_date': today_leave.from_date,
                'to_date': today_leave.to_date,
                'reason': today_leave.reason
            }
        elif today_attendance:
            employee.today_status = today_attendance.status
            employee.leave_info = None
        else:
            employee.today_status = 'none'
            employee.leave_info = None
        
        # Calculate individual user statistics for current month
        employee.present_count = Attendance.objects.filter(
            user=employee,
            date__month=current_month,
            date__year=current_year,
            status='present'
        ).count()
        
        employee.halfday_count = Attendance.objects.filter(
            user=employee,
            date__month=current_month,
            date__year=current_year,
            status='half_day'
        ).count()
        
        employee.absent_count = Attendance.objects.filter(
            user=employee,
            date__month=current_month,
            date__year=current_year,
            status='absent'
        ).count()
        
        # Count approved leaves for current year
        approved_leaves = LeaveApplication.objects.filter(
            user=employee,
            from_date__year=current_year,
            status='approved'
        )
        employee.leaves_used = sum(leave.total_days for leave in approved_leaves)
        
        # Add department from member designation
        employee.department = employee.member.designation if hasattr(employee, 'member') else 'Staff'
        
        # Add avatar color (you can customize this logic)
        colors = ['#1e3a8a', '#059669', '#dc2626', '#d97706', '#7c3aed', '#0284c7']
        employee.avatar_color = colors[employee.id % len(colors)]
    
    # Calculate today's statistics based on user permissions
    if request.user.is_superuser or (hasattr(request.user, 'member') and request.user.member.is_hr_or_admin()):
        # Admin and HR see all users' statistics
        present_today = Attendance.objects.filter(
            date=today,
            status='present'
        ).count()
        
        halfday_count = Attendance.objects.filter(
            date=today,
            status='half_day'
        ).count()
        
        absent_today = Attendance.objects.filter(
            date=today,
            status='absent'
        ).count()
        
        on_leave_today = LeaveApplication.objects.filter(
            status='approved',
            from_date__lte=today,
            to_date__gte=today
        ).count()
    else:
        # Regular users see only their own statistics
        present_today = Attendance.objects.filter(
            user=request.user,
            date=today,
            status='present'
        ).count()
        
        halfday_count = Attendance.objects.filter(
            user=request.user,
            date=today,
            status='half_day'
        ).count()
        
        absent_today = Attendance.objects.filter(
            user=request.user,
            date=today,
            status='absent'
        ).count()
        
        on_leave_today = LeaveApplication.objects.filter(
            user=request.user,
            status='approved',
            from_date__lte=today,
            to_date__gte=today
        ).count()
    
    # Get recent attendance records for the records tab (limit to recent records)
    # Check if a specific employee is selected via GET parameter
    selected_employee_id = request.GET.get('employee_id')
    
    if request.user.is_superuser or (hasattr(request.user, 'member') and request.user.member.is_hr_or_admin()):
        # Admin and HR can see all records or filter by selected employee
        if selected_employee_id:
            try:
                selected_employee = User.objects.get(id=selected_employee_id)
                attendance_records = Attendance.objects.filter(user=selected_employee).select_related('user').order_by('-date', '-created_at')[:50]
                leave_records = LeaveApplication.objects.filter(user=selected_employee).select_related('user').order_by('-applied_at')[:50]
            except User.DoesNotExist:
                attendance_records = Attendance.objects.select_related('user').order_by('-date', '-created_at')[:50]
                leave_records = LeaveApplication.objects.select_related('user').order_by('-applied_at')[:50]
        else:
            attendance_records = Attendance.objects.select_related('user').order_by('-date', '-created_at')[:50]
            leave_records = LeaveApplication.objects.select_related('user').order_by('-applied_at')[:50]
    else:
        # Regular users see only their own records
        attendance_records = Attendance.objects.filter(user=request.user).select_related('user').order_by('-date', '-created_at')[:50]
        leave_records = LeaveApplication.objects.filter(user=request.user).select_related('user').order_by('-applied_at')[:50]
    
    print(f"DEBUG: Found {len(employees)} employees")
    print(f"DEBUG: Today's stats - Present: {present_today}, Absent: {absent_today}, On Leave: {on_leave_today}")
    
    context = {
        'employees': employees,
        'present_today': present_today,
        'halfday_today': halfday_count,
        'on_leave_today': on_leave_today,
        'attendance_records': attendance_records,
        'leave_records': leave_records,
        'today': today,
        'is_admin': request.user.is_superuser or (hasattr(request.user, 'member') and request.user.member.is_hr_or_admin()),
        'selected_employee_id': selected_employee_id
    }
    
    return render(request, 'attendance.html', context)


def manage_leave_applications(request):
    if not request.user.is_authenticated:
        return redirect('bio_details:login')
    
    # Check if user is HR or Admin
    is_hr_or_admin = False
    if request.user.is_superuser:
        is_hr_or_admin = True
    elif hasattr(request.user, 'member'):
        is_hr_or_admin = request.user.member.is_hr_or_admin()
    
    if not is_hr_or_admin:
        messages.error(request, "Access denied. HR or Admin privileges required.")
        return redirect('bio_details:dashboard')
    
    # Handle leave action (approve/reject)
    if request.method == 'POST':
        leave_id = request.POST.get('leave_id')
        action = request.POST.get('action')
        
        try:
            leave_app = LeaveApplication.objects.get(id=leave_id)
            
            if action == 'approve':
                leave_app.status = 'approved'
                leave_app.approved_by = request.user
                leave_app.approved_at = timezone.now()
                messages.success(request, f'Leave approved for {leave_app.user.get_full_name() or leave_app.user.username}')
                
            elif action == 'reject':
                leave_app.status = 'rejected'
                leave_app.approved_by = request.user
                leave_app.approved_at = timezone.now()
                messages.success(request, f'Leave rejected for {leave_app.user.get_full_name() or leave_app.user.username}')
            
            leave_app.save()
            
        except LeaveApplication.DoesNotExist:
            messages.error(request, 'Leave application not found!')
    
    # Get today's date for statistics
    from datetime import date as date_obj
    today = date_obj.today()
    
    # Get all employees with today's attendance status (exclude superusers)
    employees = User.objects.filter(
        member__isnull=False,
        member__account_status=True,
        member__role='employee'
    ).select_related('member').order_by('first_name', 'last_name', 'username')
    
    # Add today's attendance status to each employee
    for employee in employees:
        # Check today's attendance
        today_attendance = Attendance.objects.filter(
            user=employee,
            date=today
        ).first()
        
        # Check if employee has approved leave today
        today_leave = LeaveApplication.objects.filter(
            user=employee,
            status='approved',
            from_date__lte=today,
            to_date__gte=today
        ).first()
        
        if today_leave:
            employee.today_status = 'leave'
            employee.leave_type = today_leave.leave_type
            employee.leave_duration = today_leave.duration
            employee.today_check_in = None
            employee.today_check_out = None
            employee.today_hours = None
        elif today_attendance:
            employee.today_status = today_attendance.status
            employee.today_check_in = today_attendance.check_in.strftime('%H:%M') if today_attendance.check_in else None
            employee.today_check_out = today_attendance.check_out.strftime('%H:%M') if today_attendance.check_out else None
            employee.today_hours = today_attendance.total_hours
            employee.leave_type = None
            employee.leave_duration = None
        else:
            employee.today_status = None
            employee.today_check_in = None
            employee.today_check_out = None
            employee.today_hours = None
            employee.leave_type = None
            employee.leave_duration = None
        
        # Calculate attendance statistics for current month/year
        current_month = today.month
        current_year = today.year
        
        employee.present_days = Attendance.objects.filter(
            user=employee,
            date__month=current_month,
            date__year=current_year,
            status='present'
        ).count()
        
        employee.halfday_days = Attendance.objects.filter(
            user=employee,
            date__month=current_month,
            date__year=current_year,
            status='half_day'
        ).count()
        
        
        # Count approved leaves for current year
        approved_leaves = LeaveApplication.objects.filter(
            user=employee,
            from_date__year=current_year,
            status='approved'
        )
        employee.leave_days = sum(leave.total_days for leave in approved_leaves)
        
        # Add department and avatar color
        employee.department = employee.member.designation if hasattr(employee, 'member') else 'Staff'
        
        # Generate initials for avatar
        if employee.first_name and employee.last_name:
            employee.initials = f"{employee.first_name[0].upper()}{employee.last_name[0].upper()}"
        elif employee.first_name:
            employee.initials = f"{employee.first_name[0].upper()}{employee.first_name[1].upper() if len(employee.first_name) > 1 else 'X'}"
        elif employee.username:
            name_parts = employee.username.split()
            if len(name_parts) >= 2:
                employee.initials = f"{name_parts[0][0].upper()}{name_parts[1][0].upper()}"
            else:
                employee.initials = f"{employee.username[0].upper()}{employee.username[1].upper() if len(employee.username) > 1 else 'X'}"
        else:
            employee.initials = "XX"
        
        colors = ['#1e3a8a', '#059669', '#dc2626', '#d97706', '#7c3aed', '#0284c7']
        employee.avatar_color = colors[employee.id % len(colors)]
    
    # Calculate today's statistics
    present_today = Attendance.objects.filter(date=today, status='present').count()
    halfday_today = Attendance.objects.filter(date=today, status='half_day').count()
    absent_today = Attendance.objects.filter(date=today, status='absent').count()
    on_leave_today = LeaveApplication.objects.filter(
        status='approved',
        from_date__lte=today,
        to_date__gte=today
    ).count()
    
    # Count employees without attendance record
    total_employees = employees.count()
    marked_attendance = present_today + halfday_today + absent_today + on_leave_today
    not_marked_today = total_employees - marked_attendance
    
    # Get leave requests
    leave_requests = LeaveApplication.objects.select_related('user', 'approved_by').order_by('-applied_at')
    pending_count = leave_requests.filter(status='pending').count()
    
    # Add initials and avatar colors to leave request users
    for leave in leave_requests:
        user = leave.user
        # Generate initials for avatar
        if user.first_name and user.last_name:
            user.initials = f"{user.first_name[0].upper()}{user.last_name[0].upper()}"
        elif user.first_name:
            user.initials = f"{user.first_name[0].upper()}{user.first_name[1].upper() if len(user.first_name) > 1 else 'X'}"
        elif user.username:
            name_parts = user.username.split()
            if len(name_parts) >= 2:
                user.initials = f"{name_parts[0][0].upper()}{name_parts[1][0].upper()}"
            else:
                user.initials = f"{user.username[0].upper()}{user.username[1].upper() if len(user.username) > 1 else 'X'}"
        else:
            user.initials = "XX"
        
        # Add avatar color
        colors = ['#1e3a8a', '#059669', '#dc2626', '#d97706', '#7c3aed', '#0284c7']
        user.avatar_color = colors[user.id % len(colors)]
    
    context = {
        'employees': employees,
        'present_today': present_today,
        'halfday_today': halfday_today,
        'absent_today': absent_today,
        'on_leave_today': on_leave_today,
        'not_marked_today': not_marked_today,
        'leave_requests': leave_requests,
        'pending_count': pending_count,
        'today': today,
    }
    
    return render(request, 'manage_leave_applications.html', context)


def leave_action(request):
    """Handle leave approval/rejection actions"""
    if not request.user.is_authenticated:
        return redirect('bio_details:login')
    
    # Check if user is HR or Admin
    is_hr_or_admin = False
    if request.user.is_superuser:
        is_hr_or_admin = True
    elif hasattr(request.user, 'member'):
        is_hr_or_admin = request.user.member.is_hr_or_admin()
    
    if not is_hr_or_admin:
        messages.error(request, "Access denied. HR or Admin privileges required.")
        return redirect('bio_details:dashboard')
    
    if request.method == 'POST':
        leave_id = request.POST.get('leave_id')
        action = request.POST.get('action')
        
        try:
            leave_app = LeaveApplication.objects.get(id=leave_id)
            
            if action == 'approve':
                leave_app.status = 'approved'
                leave_app.approved_by = request.user
                leave_app.approved_at = timezone.now()
                messages.success(request, f'Leave approved for {leave_app.user.get_full_name() or leave_app.user.username}')
                
            elif action == 'reject':
                leave_app.status = 'rejected'
                leave_app.approved_by = request.user
                leave_app.approved_at = timezone.now()
                messages.success(request, f'Leave rejected for {leave_app.user.get_full_name() or leave_app.user.username}')
            
            leave_app.save()
            
        except LeaveApplication.DoesNotExist:
            messages.error(request, 'Leave application not found!')
    
    return redirect('bio_details:manage_leave_applications')


def attendance_stats(request):
    """AJAX endpoint to get attendance statistics for an employee"""
    print(f"DEBUG: attendance_stats called by user: {request.user}")
    print(f"DEBUG: user authenticated: {request.user.is_authenticated}")
    print(f"DEBUG: GET params: {request.GET}")
    print(f"DEBUG: Request method: {request.method}")
    
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    if not request.user.is_authenticated:
        print("DEBUG: User not authenticated")
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    emp_id = request.GET.get('emp')
    if not emp_id:
        return JsonResponse({'error': 'Employee ID required'}, status=400)
    
    try:
        from django.contrib.auth.models import User
        from datetime import datetime
        
        # Get the employee user
        employee = User.objects.get(id=emp_id)
        
        # Check if user has permission to view this employee's stats
        if not request.user.is_superuser and not (hasattr(request.user, 'member') and request.user.member.is_hr_or_admin()) and employee != request.user:
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        # Calculate statistics for current month
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        # Count present days
        present_count = Attendance.objects.filter(
            user=employee,
            date__month=current_month,
            date__year=current_year,
            status='present'
        ).count()
        
        # Count half-day attendance
        halfday_count = Attendance.objects.filter(
            user=employee,
            date__month=current_month,
            date__year=current_year,
            status='half_day'
        ).count()
        
        # Count absent days
        absent_count = Attendance.objects.filter(
            user=employee,
            date__month=current_month,
            date__year=current_year,
            status='absent'
        ).count()
        
        # Count approved leaves for current year
        approved_leaves = LeaveApplication.objects.filter(
            user=employee,
            from_date__year=current_year,
            status='approved'
        )
        
        # Calculate total leave days used
        leaves_used = sum(leave.total_days for leave in approved_leaves)
        
        return JsonResponse({
            'present': present_count,
            'halfday': halfday_count,
            'absent': absent_count,
            'leaves': leaves_used
        })
        
    except User.DoesNotExist:
        return JsonResponse({'error': 'Employee not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_attendance_data(request):
    """AJAX endpoint to get attendance data for selected month"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    if not (request.user.is_superuser or (hasattr(request.user, 'member') and request.user.member.role == 'hr')):
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('bio_details:product_view')
    
    try:
        from datetime import datetime, date, timedelta
        from calendar import monthrange
        
        # Get selected month and year
        selected_month = int(request.GET.get('month', datetime.now().month))
        selected_year = int(request.GET.get('year', datetime.now().year))
        
        # Calculate attendance stats for selected month
        present_days = Attendance.objects.filter(
            date__month=selected_month,
            date__year=selected_year,
            status='present'
        ).count()
        
        leave_days = Attendance.objects.filter(
            date__month=selected_month,
            date__year=selected_year,
            status='absent'
        ).count()
        
        # Add approved leaves to leave count
        approved_leaves = LeaveApplication.objects.filter(
            status='approved',
            from_date__month__lte=selected_month,
            to_date__month__gte=selected_month,
            from_date__year=selected_year
        )
        
        # Calculate total leave days for the month
        for leave in approved_leaves:
            # Calculate overlap with selected month
            month_start = date(selected_year, selected_month, 1)
            month_end = date(selected_year, selected_month, monthrange(selected_year, selected_month)[1])
            
            overlap_start = max(leave.from_date, month_start)
            overlap_end = min(leave.to_date, month_end)
            
            if overlap_start <= overlap_end:
                days_in_month = (overlap_end - overlap_start).days + 1
                if leave.duration == 'half_day':
                    leave_days += days_in_month * 0.5
                else:
                    leave_days += days_in_month
        
        half_days = Attendance.objects.filter(
            date__month=selected_month,
            date__year=selected_year,
            status='half_day'
        ).count()
        
        # Weekly attendance data for charts (last 4 weeks of selected month)
        weekly_data = []
        month_start = date(selected_year, selected_month, 1)
        month_end = date(selected_year, selected_month, monthrange(selected_year, selected_month)[1])
        
        # Calculate weekly data
        current_date = month_start
        week_num = 1
        while current_date <= month_end and week_num <= 4:
            week_end = min(current_date + timedelta(days=6), month_end)
            
            week_present = Attendance.objects.filter(
                date__range=[current_date, week_end],
                status='present'
            ).count()
            
            week_leave = Attendance.objects.filter(
                date__range=[current_date, week_end],
                status='absent'
            ).count()
            
            week_halfday = Attendance.objects.filter(
                date__range=[current_date, week_end],
                status='half_day'
            ).count()
            
            weekly_data.append({
                'present': week_present,
                'leave': week_leave,
                'halfday': week_halfday
            })
            
            current_date = week_end + timedelta(days=1)
            week_num += 1
        
        return JsonResponse({
            'success': True,
            'present_days': int(present_days),
            'leave_days': int(leave_days),
            'half_days': int(half_days),
            'weekly_data': weekly_data
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_employee_joins_data(request):
    """AJAX endpoint to get monthly employee joins data"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    if not (request.user.is_superuser or (hasattr(request.user, 'member') and request.user.member.role == 'hr')):
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('bio_details:product_view')
    
    try:
        from datetime import datetime, timedelta
        from django.db.models import Count
        from django.contrib.auth.models import User
        
        # Get data for last 12 months
        current_date = datetime.now()
        months = []
        joins = []
        
        for i in range(11, -1, -1):
            # Calculate month and year
            month_date = current_date - timedelta(days=30*i)
            month_name = month_date.strftime('%b')
            
            # Count employee joins for this month (users with member role='employee')
            joins_count = User.objects.filter(
                date_joined__year=month_date.year,
                date_joined__month=month_date.month,
                member__role='employee'
            ).count()
            
            months.append(month_name)
            joins.append(joins_count)
        
        return JsonResponse({
            'success': True,
            'months': months,
            'joins': joins
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_orders_data(request):
    """AJAX endpoint to get monthly orders data"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    if not (request.user.is_superuser or (hasattr(request.user, 'member') and request.user.member.role == 'hr')):
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('bio_details:product_view')
    
    try:
        from datetime import datetime, timedelta
        from django.db.models import Count
        
        # Get data for last 12 months
        current_date = datetime.now()
        months = []
        orders = []
        
        for i in range(11, -1, -1):
            # Calculate month and year
            month_date = current_date - timedelta(days=30*i)
            month_name = month_date.strftime('%b')
            
            # Count orders for this month
            orders_count = Order.objects.filter(
                created_at__year=month_date.year,
                created_at__month=month_date.month
            ).count()
            
            months.append(month_name)
            orders.append(orders_count)
        
        return JsonResponse({
            'success': True,
            'months': months,
            'orders': orders
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_employee_monthly_data(request):
    """AJAX endpoint to get monthly employee data for analytics charts"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    if not (request.user.is_superuser or (hasattr(request.user, 'member') and request.user.member.role == 'hr')):
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        from datetime import datetime, timedelta
        from django.db.models import Count
        from django.contrib.auth.models import User
        
        # Get selected year from request
        selected_year = int(request.GET.get('year', datetime.now().year))
        
        # Always show all 12 months
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        active_data = []
        inactive_data = []
        
        for month_num in range(1, 13):
            # Count active employees who joined up to this month in the selected year
            active_count = Member.objects.filter(
                user__date_joined__year=selected_year,
                user__date_joined__month=month_num,
                account_status=True,
                role='employee',
                user__is_superuser=False
            ).count()
            
            # Count inactive employees who joined in this month in the selected year
            inactive_count = Member.objects.filter(
                user__date_joined__year=selected_year,
                user__date_joined__month=month_num,
                account_status=False,
                role='employee',
                user__is_superuser=False
            ).count()
            
            active_data.append(active_count)
            inactive_data.append(inactive_count)
        
        return JsonResponse({
            'success': True,
            'months': months,
            'active_data': active_data,
            'inactive_data': inactive_data
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_product_monthly_data(request):
    """AJAX endpoint to get monthly product stock data for analytics charts"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    if not (request.user.is_superuser or (hasattr(request.user, 'member') and request.user.member.role == 'hr')):
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        from datetime import datetime, timedelta
        from django.db.models import Count
        
        # Get selected year from request
        selected_year = int(request.GET.get('year', datetime.now().year))
        
        # Always show all 12 months
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        in_stock_data = []
        out_of_stock_data = []
        
        for month_num in range(1, 13):
            # Count products created in this specific month that are in stock
            in_stock_count = Product.objects.filter(
                created_at__year=selected_year,
                created_at__month=month_num,
                current_stock__gt=0
            ).count()
            
            # Count products created in this specific month that are out of stock
            out_of_stock_count = Product.objects.filter(
                created_at__year=selected_year,
                created_at__month=month_num,
                current_stock=0
            ).count()
            
            in_stock_data.append(in_stock_count)
            out_of_stock_data.append(out_of_stock_count)
        
        return JsonResponse({
            'success': True,
            'months': months,
            'in_stock_data': in_stock_data,
            'out_of_stock_data': out_of_stock_data
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_order_monthly_data(request):
    """AJAX endpoint to get monthly order data for analytics charts"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    if not (request.user.is_superuser or (hasattr(request.user, 'member') and request.user.member.role == 'hr')):
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        from datetime import datetime, timedelta
        from django.db.models import Count
        
        # Get selected year from request
        selected_year = int(request.GET.get('year', datetime.now().year))
        
        # Always show all 12 months
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        completed_data = []
        pending_data = []
        
        for month_num in range(1, 13):
            # Count completed orders for this specific month
            completed_count = Invoice.objects.filter(
                invoice_date__year=selected_year,
                invoice_date__month=month_num,
                payment_status='paid'
            ).count()
            
            # Count pending orders for this specific month
            pending_count = Invoice.objects.filter(
                invoice_date__year=selected_year,
                invoice_date__month=month_num,
                payment_status='pending'
            ).count()
            
            completed_data.append(completed_count)
            pending_data.append(pending_count)
        
        return JsonResponse({
            'success': True,
            'months': months,
            'completed_data': completed_data,
            'pending_data': pending_data
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_employee_status_data(request):
    """AJAX endpoint to get employee status data for pie charts"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    if not (request.user.is_superuser or (hasattr(request.user, 'member') and request.user.member.role == 'hr')):
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        from datetime import datetime
        
        # Get selected year and month from request
        selected_year = int(request.GET.get('year', datetime.now().year))
        selected_month = request.GET.get('month')
        
        if selected_month:
            # Filter by specific month and year
            selected_month = int(selected_month)
            
            # Count employees who joined up to the selected month/year
            active_employees = Member.objects.filter(
                user__date_joined__year__lte=selected_year,
                user__date_joined__month__lte=selected_month if selected_year == datetime.now().year else 12,
                account_status=True,
                role='employee',
                user__is_superuser=False
            ).count()
            
            inactive_employees = Member.objects.filter(
                user__date_joined__year__lte=selected_year,
                user__date_joined__month__lte=selected_month if selected_year == datetime.now().year else 12,
                account_status=False,
                role='employee',
                user__is_superuser=False
            ).count()
        else:
            # Filter by year only
            active_employees = Member.objects.filter(
                user__date_joined__year__lte=selected_year,
                account_status=True,
                role='employee',
                user__is_superuser=False
            ).count()
            
            inactive_employees = Member.objects.filter(
                user__date_joined__year__lte=selected_year,
                account_status=False,
                role='employee',
                user__is_superuser=False
            ).count()
        
        total_employees = active_employees + inactive_employees
        
        return JsonResponse({
            'success': True,
            'active_employees': active_employees,
            'inactive_employees': inactive_employees,
            'total_employees': total_employees
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_product_status_data(request):
    """AJAX endpoint to get product status data for pie charts"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    if not (request.user.is_superuser or (hasattr(request.user, 'member') and request.user.member.role == 'hr')):
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        from datetime import datetime
        
        # Get selected year and month from request
        selected_year = int(request.GET.get('year', datetime.now().year))
        selected_month = request.GET.get('month')
        
        if selected_month:
            # Filter by specific month and year
            selected_month = int(selected_month)
            
            # Count products created up to the selected month/year
            available_products = Product.objects.filter(
                created_at__year__lte=selected_year,
                created_at__month__lte=selected_month if selected_year == datetime.now().year else 12,
                current_stock__gt=0
            ).count()
            
            out_of_stock_products = Product.objects.filter(
                created_at__year__lte=selected_year,
                created_at__month__lte=selected_month if selected_year == datetime.now().year else 12,
                current_stock=0
            ).count()
        else:
            # Filter by year only
            available_products = Product.objects.filter(
                created_at__year__lte=selected_year,
                current_stock__gt=0
            ).count()
            
            out_of_stock_products = Product.objects.filter(
                created_at__year__lte=selected_year,
                current_stock=0
            ).count()
        
        total_products = available_products + out_of_stock_products
        
        return JsonResponse({
            'success': True,
            'available_products': available_products,
            'out_of_stock_products': out_of_stock_products,
            'total_products': total_products
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_order_status_data(request):
    """AJAX endpoint to get order status data for pie charts"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    if not (request.user.is_superuser or (hasattr(request.user, 'member') and request.user.member.role == 'hr')):
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        from datetime import datetime
        
        # Get selected year and month from request
        selected_year = int(request.GET.get('year', datetime.now().year))
        selected_month = request.GET.get('month')
        
        if selected_month:
            # Filter by specific month and year
            selected_month = int(selected_month)
            
            # Count orders for the selected month/year
            completed_orders = Invoice.objects.filter(
                invoice_date__year=selected_year,
                invoice_date__month=selected_month,
                payment_status='paid'
            ).count()
            
            pending_orders = Invoice.objects.filter(
                invoice_date__year=selected_year,
                invoice_date__month=selected_month,
                payment_status='pending'
            ).count()
        else:
            # Filter by year only
            completed_orders = Invoice.objects.filter(
                invoice_date__year=selected_year,
                payment_status='paid'
            ).count()
            
            pending_orders = Invoice.objects.filter(
                invoice_date__year=selected_year,
                payment_status='pending'
            ).count()
        
        total_orders = completed_orders + pending_orders
        
        return JsonResponse({
            'success': True,
            'completed_orders': completed_orders,
            'pending_orders': pending_orders,
            'total_orders': total_orders
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_customer_monthly_data(request):
    """AJAX endpoint to get monthly customer data for analytics charts"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    if not (request.user.is_superuser or (hasattr(request.user, 'member') and request.user.member.role == 'hr')):
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        from datetime import datetime, timedelta
        from django.db.models import Count
        
        # Get selected year from request
        selected_year = int(request.GET.get('year', datetime.now().year))
        
        # Always show all 12 months
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        active_data = []
        inactive_data = []
        
        for month_num in range(1, 13):
            # Count active customers who joined in this month in the selected year
            active_count = Customer.objects.filter(
                user__date_joined__year=selected_year,
                user__date_joined__month=month_num,
                is_active=True
            ).count()
            
            # Count inactive customers who joined in this month in the selected year
            inactive_count = Customer.objects.filter(
                user__date_joined__year=selected_year,
                user__date_joined__month=month_num,
                is_active=False
            ).count()
            
            active_data.append(active_count)
            inactive_data.append(inactive_count)
        
        return JsonResponse({
            'success': True,
            'months': months,
            'active_data': active_data,
            'inactive_data': inactive_data
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_customer_status_data(request):
    """AJAX endpoint to get customer status data for pie charts"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    if not (request.user.is_superuser or (hasattr(request.user, 'member') and request.user.member.role == 'hr')):
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        from datetime import datetime
        
        # Get selected year and month from request
        selected_year = int(request.GET.get('year', datetime.now().year))
        selected_month = request.GET.get('month')
        
        if selected_month:
            # Filter by specific month and year
            selected_month = int(selected_month)
            
            # Count customers who joined up to the selected month/year
            active_customers = Customer.objects.filter(
                user__date_joined__year__lte=selected_year,
                user__date_joined__month__lte=selected_month if selected_year == datetime.now().year else 12,
                is_active=True
            ).count()
            
            inactive_customers = Customer.objects.filter(
                user__date_joined__year__lte=selected_year,
                user__date_joined__month__lte=selected_month if selected_year == datetime.now().year else 12,
                is_active=False
            ).count()
        else:
            # Filter by year only
            active_customers = Customer.objects.filter(
                user__date_joined__year__lte=selected_year,
                is_active=True
            ).count()
            
            inactive_customers = Customer.objects.filter(
                user__date_joined__year__lte=selected_year,
                is_active=False
            ).count()
        
        total_customers = active_customers + inactive_customers
        
        return JsonResponse({
            'success': True,
            'active_customers': active_customers,
            'inactive_customers': inactive_customers,
            'total_customers': total_customers
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



