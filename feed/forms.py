
from django import forms
from .models import FeedStock, FeedConsumption


class FeedStockForm(forms.ModelForm):
    class Meta:
        model = FeedStock
        fields = [
            'feed_name',
            'quantity_kg',
            'price_per_kg'
        ]


class FeedConsumptionForm(forms.ModelForm):
    class Meta:
        model = FeedConsumption
        fields = [
            'batch',
            'feed',
            'date',
            'quantity_used_kg'
        ]

        widgets = {
            'date': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            )
        }

    def clean_quantity_used_kg(self):
        quantity = self.cleaned_data['quantity_used_kg']

        if quantity <= 0:
            raise forms.ValidationError(
                'Quantity must be greater than zero.'
            )

        return quantity

    def clean(self):
        cleaned_data = super().clean()

        feed = cleaned_data.get('feed')
        quantity = cleaned_data.get('quantity_used_kg')

        if feed is not None and quantity is not None:
            available = feed.quantity_kg

            if self.instance.pk:
                old = FeedConsumption.objects.filter(
                    pk=self.instance.pk
                ).first()

                if old and old.feed_id == feed.pk:
                    available += old.quantity_used_kg

            if quantity > available:
                raise forms.ValidationError(
                    f'Not enough feed stock! '
                    f'Available: {available} kg'
                )

        return cleaned_data
