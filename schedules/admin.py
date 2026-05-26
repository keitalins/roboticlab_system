from django.contrib import admin
from .models import LabSession


@admin.register(LabSession)
class LabSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'requested_by', 'start_time', 'end_time', 'status', 'approved_by')
    list_filter = ('status',)
    search_fields = ('title', 'requested_by__username')
    date_hierarchy = 'start_time'
