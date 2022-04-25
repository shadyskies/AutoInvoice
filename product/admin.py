from django.contrib import admin
from .models import Product, Order, ProductOrder

class OrderAdmin(admin.ModelAdmin):
    fields = ["customer", "phone", "address", "total", "invoice_file"]
    read_only_fields = ['invoice_id']


admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(ProductOrder)