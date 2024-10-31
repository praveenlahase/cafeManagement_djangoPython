from django.contrib import admin
from .models import Product

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    search_fields = ['name']
    list_filter = ['price']

admin.site.register(Product,ProductAdmin)
