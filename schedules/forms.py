from django import forms
from .models import LabSession


class LabSessionForm(forms.ModelForm):
    class Meta:
        model = LabSession
        fields = ('title', 'description', 'equipment', 'start_time', 'end_time')
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'equipment': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, f in self.fields.items():
            if name not in ('start_time', 'end_time', 'equipment'):
                f.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_time')
        end = cleaned_data.get('end_time')
        if start and end and end <= start:
            raise forms.ValidationError('End time must be after start time.')
        return cleaned_data


class ApprovalForm(forms.ModelForm):
    class Meta:
        model = LabSession
        fields = ('status', 'rejection_reason')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs['class'] = 'form-control'
