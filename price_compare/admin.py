from django.contrib import admin
from .models import Tracked_Products


class TrackingDateAdmin(admin.ModelAdmin):
    readonly_fields = ('start_tracking_date','start_price_change_date')

# Register your models here.
admin.site.register(Tracked_Products,TrackingDateAdmin)