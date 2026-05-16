from django import forms
from .models import Patient, PatientDocument 


class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = [
            "national_id",
            "full_name",
            "birth_date",
            "gender",
            "phone_number",
            "governorate",
            "affiliated_branch",
            "diagnosis",
        ]

        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "diagnosis": forms.Textarea(attrs={"rows": 3}),
        }
        
from django import forms
from .models import PatientDocument


class PatientDocumentForm(forms.ModelForm):

    class Meta:
        model = PatientDocument
        fields = ["document_type", "file"]

        widgets = {
            "document_type": forms.Select(attrs={
                "class": "form-input"
            }),

            "file": forms.FileInput(attrs={
                "class": "form-input"
            })
        }
        
class PatientUpdateForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            "full_name",
            "phone_number",
            "governorate",
            "affiliated_branch",
            "diagnosis",
        ]