
from django import forms
from .models import HealthRecord


class HealthRecordForm(forms.ModelForm):

    class Meta:
        model = HealthRecord

        fields = [
            'batch',
            'record_type',
            'date',
            'description',
            'medicine_or_vaccine',
            'cost',
            'next_due_date',
            'notes',
        ]

        widgets = {
            'date': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),

            'next_due_date': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),

            'description': forms.Textarea(
                attrs={'rows': 3}
            ),

            'notes': forms.Textarea(
                attrs={'rows': 3}
            ),
        }
