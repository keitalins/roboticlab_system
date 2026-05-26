from django import forms
from .models import LabReport


class LabReportForm(forms.ModelForm):
    class Meta:
        model = LabReport
        fields = ('title', 'session', 'content', 'findings', 'conclusion', 'attachment')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs['class'] = 'form-control'
        if user and not (user.is_admin() or user.is_technician()):
            from schedules.models import LabSession
            self.fields['session'].queryset = LabSession.objects.filter(requested_by=user)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = LabReport
        fields = ('status', 'reviewer_notes')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs['class'] = 'form-control'
