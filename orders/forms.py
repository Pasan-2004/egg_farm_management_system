
from django import forms
from .models import EggOrder


class EggOrderForm(forms.ModelForm):

    class Meta:
        model = EggOrder
        fields = ['quantity']

        widgets = {
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Enter number of eggs'
            })
        }

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']

        if quantity < 1:
            raise forms.ValidationError(
                "Please order at least one egg."
            )

        return quantity
