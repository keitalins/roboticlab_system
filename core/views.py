from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from inventory.models import Equipment
from schedules.models import LabSession
from lab_reports.models import LabReport
from messaging_app.models import Message, Notification
from django.utils import timezone


@login_required
def dashboard(request):
    user = request.user
    now = timezone.now()

    # Stats vary by role
    if user.is_admin() or user.is_technician():
        total_equipment = Equipment.objects.count()
        available_equipment = Equipment.objects.filter(status=Equipment.STATUS_AVAILABLE).count()
        pending_sessions = LabSession.objects.filter(status=LabSession.STATUS_PENDING).count()
        total_reports = LabReport.objects.count()
        submitted_reports = LabReport.objects.filter(status=LabReport.STATUS_SUBMITTED).count()
        upcoming_sessions = LabSession.objects.filter(
            start_time__gte=now, status=LabSession.STATUS_APPROVED
        ).order_by('start_time')[:5]
        recent_reports = LabReport.objects.order_by('-created_at')[:5]
    else:
        total_equipment = Equipment.objects.filter(status=Equipment.STATUS_AVAILABLE).count()
        available_equipment = total_equipment
        pending_sessions = LabSession.objects.filter(requested_by=user, status=LabSession.STATUS_PENDING).count()
        total_reports = LabReport.objects.filter(author=user).count()
        submitted_reports = LabReport.objects.filter(author=user, status=LabReport.STATUS_SUBMITTED).count()
        upcoming_sessions = LabSession.objects.filter(
            requested_by=user, start_time__gte=now
        ).order_by('start_time')[:5]
        recent_reports = LabReport.objects.filter(author=user).order_by('-created_at')[:5]

    unread_messages = Message.objects.filter(recipient=user, is_read=False).count()
    unread_notifications = Notification.objects.filter(user=user, is_read=False).count()
    maintenance_due = Equipment.objects.filter(
        next_maintenance__lte=now.date(), status=Equipment.STATUS_AVAILABLE
    ).count()

    context = {
        'total_equipment': total_equipment,
        'available_equipment': available_equipment,
        'pending_sessions': pending_sessions,
        'total_reports': total_reports,
        'submitted_reports': submitted_reports,
        'upcoming_sessions': upcoming_sessions,
        'recent_reports': recent_reports,
        'unread_messages': unread_messages,
        'unread_notifications': unread_notifications,
        'maintenance_due': maintenance_due,
    }
    return render(request, 'core/dashboard.html', context)
