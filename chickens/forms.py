
from django import forms
from django.utils import timezone
from .models import ChickenBatch


class ChickenBatchForm(forms.ModelForm):

    class Meta:
        model = ChickenBatch

        fields = [
            'batch_name',
            'breed',
            'quantity',
            'age_weeks',
            'arrival_date',
        ]

        widgets = {
            'arrival_date': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            )
        }

    # Validate Batch Name
    def clean_batch_name(self):
        name = self.cleaned_data['batch_name'].strip()

        if not name:
            raise forms.ValidationError(
                "Batch name cannot be empty."
            )

        # Check duplicate batch names
        existing = ChickenBatch.objects.filter(
            batch_name__iexact=name
        )

        # Allow the current batch when editing
        if self.instance.pk:
            existing = existing.exclude(
                pk=self.instance.pk
            )

        if existing.exists():
            raise forms.ValidationError(
                "A chicken batch with this name already exists."
            )

        return name

    # Validate Chicken Quantity
    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']

        if quantity is not None and quantity <= 0:
            raise forms.ValidationError(
                "Chicken quantity must be greater than zero."
            )

        return quantity

    # Validate Chicken Age
    def clean_age_weeks(self):
        age = self.cleaned_data['age_weeks']

        if age is not None and age < 0:
            raise forms.ValidationError(
                "Chicken age cannot be negative."
            )

        return age

    # Validate Arrival Date
    def clean_arrival_date(self):
        arrival_date = self.cleaned_data['arrival_date']

        if arrival_date and arrival_date > timezone.localdate():
            raise forms.ValidationError(
                "Arrival date cannot be in the future."
            )

        return arrival_date
