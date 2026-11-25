
from django import forms
from .models import EggProduction


class EggProductionForm(forms.ModelForm):
    class Meta:
        model = EggProduction
        fields = [
            'batch',
            'date',
            'eggs_collected',
            'damaged_eggs',
        ]

        widgets = {
            'date': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        eggs = cleaned_data.get('eggs_collected')
        damaged = cleaned_data.get('damaged_eggs')

        if eggs is not None and damaged is not None:
            if damaged > eggs:
                raise forms.ValidationError(
                    "Damaged eggs cannot exceed collected eggs."
                )

        return cleaned_data
