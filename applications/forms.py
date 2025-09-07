from django import forms
from .models import Application

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["resume_url", "cover_letter"]
        widgets = {
            "cover_letter": forms.Textarea(attrs={"rows": 7, "maxlength": 1000, 'placeholder': 'Write your cover letter here...'}),
        }
