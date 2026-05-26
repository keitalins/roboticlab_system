from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import LabReport
from .forms import LabReportForm, ReviewForm


@login_required
def report_list(request):
    user = request.user
    if user.is_admin() or user.is_technician():
        reports = LabReport.objects.select_related('author', 'session').all()
    else:
        reports = LabReport.objects.filter(author=user)
    return render(request, 'lab_reports/report_list.html', {'reports': reports})


@login_required
def report_detail(request, pk):
    report = get_object_or_404(LabReport, pk=pk)
    can_review = request.user.is_admin() or request.user.is_technician()
    return render(request, 'lab_reports/report_detail.html', {'report': report, 'can_review': can_review})


@login_required
def report_create(request):
    if request.method == 'POST':
        form = LabReportForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            report = form.save(commit=False)
            report.author = request.user
            report.save()
            messages.success(request, 'Report created.')
            return redirect('lab_reports:report_detail', pk=report.pk)
    else:
        form = LabReportForm(user=request.user)
    return render(request, 'lab_reports/report_form.html', {'form': form, 'title': 'New Report'})


@login_required
def report_edit(request, pk):
    report = get_object_or_404(LabReport, pk=pk)
    if report.author != request.user and not request.user.is_admin():
        messages.error(request, 'Permission denied.')
        return redirect('lab_reports:report_list')
    if request.method == 'POST':
        form = LabReportForm(request.POST, request.FILES, instance=report, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Report updated.')
            return redirect('lab_reports:report_detail', pk=pk)
    else:
        form = LabReportForm(instance=report, user=request.user)
    return render(request, 'lab_reports/report_form.html', {'form': form, 'title': 'Edit Report'})


@login_required
def report_submit(request, pk):
    report = get_object_or_404(LabReport, pk=pk, author=request.user)
    report.status = LabReport.STATUS_SUBMITTED
    report.save()
    messages.success(request, 'Report submitted for review.')
    return redirect('lab_reports:report_detail', pk=pk)


@login_required
def report_review(request, pk):
    if not (request.user.is_admin() or request.user.is_technician()):
        messages.error(request, 'Permission denied.')
        return redirect('lab_reports:report_list')
    report = get_object_or_404(LabReport, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=report)
        if form.is_valid():
            r = form.save(commit=False)
            r.reviewer = request.user
            r.save()
            messages.success(request, 'Review saved.')
            return redirect('lab_reports:report_detail', pk=pk)
    else:
        form = ReviewForm(instance=report)
    return render(request, 'lab_reports/review_form.html', {'form': form, 'report': report})
