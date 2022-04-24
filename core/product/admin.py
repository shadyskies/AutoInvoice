from django.contrib import admin
from .models import Product, Invoice


admin.site.register(Product)
admin.site.register(Invoice)