from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import LabSession
from .forms import LabSessionForm, ApprovalForm


@login_required
def session_list(request):
    user = request.user
    if user.is_admin() or user.is_technician():
        sessions = LabSession.objects.select_related('requested_by', 'approved_by').all()
    else:
        sessions = LabSession.objects.filter(requested_by=user)

    status_filter = request.GET.get('status', '')
    if status_filter:
        sessions = sessions.filter(status=status_filter)

    return render(request, 'schedules/session_list.html', {
        'sessions': sessions,
        'statuses': LabSession.STATUS_CHOICES,
        'selected_status': status_filter,
    })


@login_required
def session_detail(request, pk):
    session = get_object_or_404(LabSession, pk=pk)
    can_approve = request.user.is_admin() or request.user.is_technician()
    return render(request, 'schedules/session_detail.html', {
        'session': session,
        'can_approve': can_approve,
    })


@login_required
def session_create(request):
    if request.method == 'POST':
        form = LabSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.requested_by = request.user
            session.save()
            form.save_m2m()
            messages.success(request, 'Session request submitted for approval.')
            return redirect('schedules:session_list')
    else:
        form = LabSessionForm()
    return render(request, 'schedules/session_form.html', {'form': form, 'title': 'Book Lab Session'})


@login_required
def session_edit(request, pk):
    session = get_object_or_404(LabSession, pk=pk)
    if session.requested_by != request.user and not request.user.is_admin():
        messages.error(request, 'Permission denied.')
        return redirect('schedules:session_list')
    if request.method == 'POST':
        form = LabSessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            messages.success(request, 'Session updated.')
            return redirect('schedules:session_detail', pk=pk)
    else:
        form = LabSessionForm(instance=session)
    return render(request, 'schedules/session_form.html', {'form': form, 'title': 'Edit Session'})


@login_required
def session_approve(request, pk):
    if not (request.user.is_admin() or request.user.is_technician()):
        messages.error(request, 'Permission denied.')
        return redirect('schedules:session_list')
    session = get_object_or_404(LabSession, pk=pk)
    if request.method == 'POST':
        form = ApprovalForm(request.POST, instance=session)
        if form.is_valid():
            s = form.save(commit=False)
            s.approved_by = request.user
            s.save()
            messages.success(request, f'Session {s.get_status_display()}.')
            return redirect('schedules:session_detail', pk=pk)
    else:
        form = ApprovalForm(instance=session)
    return render(request, 'schedules/session_approve.html', {'form': form, 'session': session})


@login_required
def session_cancel(request, pk):
    session = get_object_or_404(LabSession, pk=pk)
    if session.requested_by != request.user and not request.user.is_admin():
        messages.error(request, 'Permission denied.')
        return redirect('schedules:session_list')
    if request.method == 'POST':
        session.status = LabSession.STATUS_CANCELLED
        session.save()
        messages.success(request, 'Session cancelled.')
        return redirect('schedules:session_list')
    return render(request, 'schedules/session_confirm_cancel.html', {'session': session})
