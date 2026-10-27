from django import forms
from .models import ChickenBatch

class ChickenBatchForm(forms.ModelForm):
    class Meta:
        model = ChickenBatch
        fields = [
            'batch_name',
            'breed',
            'quantity',
            'age_weeks',
            'arrival_date'
        ]

        widgets = {
            'arrival_date': forms.DateInput(
                attrs={'type': 'date'}
            )
        }
