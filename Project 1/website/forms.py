from django import forms
from .models import EventSignup

class EventSignupForm(forms.ModelForm):
    class Meta:
        model = EventSignup
        fields = ['name', 'age', 'phone', 'email', 'time', 'introduction']
