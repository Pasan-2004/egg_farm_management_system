from django.contrib import admin
from .models import HealthRecord


@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = (
        'batch',
        'record_type',
        'date',
        'medicine_or_vaccine',
        'cost',
        'next_due_date',
    )

    list_filter = ('record_type', 'date')

    search_fields = (
        'batch__batch_name',
        'description',
        'medicine_or_vaccine',
    )