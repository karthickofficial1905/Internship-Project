from django.contrib import admin
from .models import Member,Category,Product,Brand,Cart,CartItem,Order,OrderItem,Invoice,InvoiceItem,Currency,Country,Tax,Attendance,LeaveApplication,Customer,ProductReview

admin.site.register(Member)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)
admin.site.register(Currency)
admin.site.register(Country)
admin.site.register(Tax)
admin.site.register(Customer)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'status', 'check_in', 'check_out', 'total_hours']
    list_filter = ['status', 'date', 'user']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    date_hierarchy = 'date'
    ordering = ['-date']


@admin.register(LeaveApplication)
class LeaveApplicationAdmin(admin.ModelAdmin):
    list_display = ['user', 'leave_type', 'from_date', 'to_date', 'duration', 'status', 'applied_at']
    list_filter = ['leave_type', 'duration', 'status', 'applied_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'reason']
    date_hierarchy = 'applied_at'
    ordering = ['-applied_at']
    readonly_fields = ['applied_at', 'total_days']


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at', 'product']
    search_fields = ['product__name', 'user__username', 'comment']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
