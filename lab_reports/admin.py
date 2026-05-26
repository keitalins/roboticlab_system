from django.contrib import admin
from .models import LabReport


@admin.register(LabReport)
class LabReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'session', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('title', 'author__username')
