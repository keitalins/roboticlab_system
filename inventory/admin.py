from django.contrib import admin
from .models import Equipment, Category, MaintenanceLog


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'serial_number', 'category', 'status', 'location', 'last_maintenance')
    list_filter = ('status', 'category')
    search_fields = ('name', 'serial_number')
    date_hierarchy = 'created_at'


@admin.register(MaintenanceLog)
class MaintenanceLogAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'date', 'performed_by', 'cost')
    list_filter = ('date',)
