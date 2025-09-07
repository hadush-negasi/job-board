from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["title", "location", "description", "job_type", "salary", "deadline"]  # only fields user can fill
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control input-pill", "placeholder": "Job title, e.g., Software Engineer"}),
            "location": forms.TextInput(attrs={"class": "form-control input-pill", "placeholder": "City, State or Remote"}),
            "description": forms.Textarea(attrs={"class": "form-control input-pill", "rows": 6, 'style': 'border-radius: 0 !important;', "placeholder": "Full job description here"}),
            "job_type": forms.Select(attrs={"class": "form-select"}),
            "salary": forms.NumberInput(attrs={"class": "form-control input-pill", "placeholder": "Salary (optional)"}),
            "deadline": forms.DateInput(attrs={"class": "form-control input-pill", "type": "date"}),
        }
