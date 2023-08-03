from django.contrib import admin
from .models import *

# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    search_fields = ['name']

class SpiritAdmin(admin.ModelAdmin):
    search_fields = ['name']


admin.site.register(Spirit, SpiritAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(VolumeItem)
admin.site.register(Category)