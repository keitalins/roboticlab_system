from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Equipment, Category, MaintenanceLog
from .forms import EquipmentForm, CategoryForm, MaintenanceLogForm


@login_required
def equipment_list(request):
    qs = Equipment.objects.select_related('category').all()
    q = request.GET.get('q', '')
    status = request.GET.get('status', '')
    category = request.GET.get('category', '')

    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(serial_number__icontains=q))
    if status:
        qs = qs.filter(status=status)
    if category:
        qs = qs.filter(category_id=category)

    categories = Category.objects.all()
    context = {
        'equipment_list': qs,
        'categories': categories,
        'statuses': Equipment.STATUS_CHOICES,
        'q': q,
        'selected_status': status,
        'selected_category': category,
    }
    return render(request, 'inventory/equipment_list.html', context)


@login_required
def equipment_detail(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    logs = equipment.maintenance_logs.select_related('performed_by').all()
    return render(request, 'inventory/equipment_detail.html', {'equipment': equipment, 'logs': logs})


@login_required
def equipment_create(request):
    if not (request.user.is_admin() or request.user.is_technician()):
        messages.error(request, 'Permission denied.')
        return redirect('inventory:equipment_list')
    if request.method == 'POST':
        form = EquipmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipment added successfully.')
            return redirect('inventory:equipment_list')
    else:
        form = EquipmentForm()
    return render(request, 'inventory/equipment_form.html', {'form': form, 'title': 'Add Equipment'})


@login_required
def equipment_edit(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    if not (request.user.is_admin() or request.user.is_technician()):
        messages.error(request, 'Permission denied.')
        return redirect('inventory:equipment_list')
    if request.method == 'POST':
        form = EquipmentForm(request.POST, request.FILES, instance=equipment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipment updated.')
            return redirect('inventory:equipment_detail', pk=pk)
    else:
        form = EquipmentForm(instance=equipment)
    return render(request, 'inventory/equipment_form.html', {'form': form, 'title': 'Edit Equipment'})


@login_required
def equipment_delete(request, pk):
    if not request.user.is_admin():
        messages.error(request, 'Permission denied.')
        return redirect('inventory:equipment_list')
    equipment = get_object_or_404(Equipment, pk=pk)
    if request.method == 'POST':
        equipment.delete()
        messages.success(request, 'Equipment deleted.')
        return redirect('inventory:equipment_list')
    return render(request, 'inventory/equipment_confirm_delete.html', {'equipment': equipment})


@login_required
def maintenance_add(request, equipment_pk):
    equipment = get_object_or_404(Equipment, pk=equipment_pk)
    if not (request.user.is_admin() or request.user.is_technician()):
        messages.error(request, 'Permission denied.')
        return redirect('inventory:equipment_detail', pk=equipment_pk)
    if request.method == 'POST':
        form = MaintenanceLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.equipment = equipment
            log.performed_by = request.user
            log.save()
            equipment.last_maintenance = log.date
            equipment.save()
            messages.success(request, 'Maintenance log added.')
            return redirect('inventory:equipment_detail', pk=equipment_pk)
    else:
        form = MaintenanceLogForm()
    return render(request, 'inventory/maintenance_form.html', {'form': form, 'equipment': equipment})
