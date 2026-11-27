from django.contrib import admin
from .models import Management, Zone


@admin.register(Management)
class ManagementAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin', 'city', 'state', 'is_active')
    search_fields = ('name', 'city', 'registration_number')
    list_filter = ('city', 'state', 'is_active')


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'management', 'city', 'pincode', 'is_active')
    search_fields = ('name', 'city', 'pincode')
    list_filter = ('management', 'is_active')