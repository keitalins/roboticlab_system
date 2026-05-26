from django import forms
from .models import Message
from accounts.models import User


class ComposeForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('recipient', 'subject', 'body')

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if current_user:
            self.fields['recipient'].queryset = User.objects.exclude(pk=current_user.pk)
        for f in self.fields.values():
            f.widget.attrs['class'] = 'form-control'
