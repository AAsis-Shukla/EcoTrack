from django.contrib import admin
from .models import Donor


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'donor_type',
        'management',
        'zone',
        'status',
        'is_active'
    )

    search_fields = ('name', 'phone', 'email')
    list_filter = ('donor_type', 'management', 'zone', 'status')