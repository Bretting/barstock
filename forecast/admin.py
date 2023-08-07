from django.contrib import admin
from .models import *

# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    search_fields = ['name']

class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name']


admin.site.register(Product, ProductAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(VolumeItem)
admin.site.register(Category)