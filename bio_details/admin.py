from django.contrib import admin
from .models import Member,Category,Product,Brand,Cart,CartItem,Order,OrderItem,Invoice,InvoiceItem,Currency,Country,Tax

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
