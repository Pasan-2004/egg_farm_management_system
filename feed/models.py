
from decimal import Decimal

from django.db import models, transaction
from django.db.models import F
from django.core.exceptions import ValidationError

from chickens.models import ChickenBatch


class FeedStock(models.Model):
    feed_name = models.CharField(max_length=100)
    quantity_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    price_per_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return (
            f"{self.feed_name} "
            f"(ID: {self.pk}, Rs. {self.price_per_kg}/kg)"
        )


class FeedConsumption(models.Model):
    batch = models.ForeignKey(
        ChickenBatch,
        on_delete=models.PROTECT
    )
    feed = models.ForeignKey(
        FeedStock,
        on_delete=models.PROTECT
    )
    date = models.DateField()
    quantity_used_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    @property
    def total_cost(self):
        return self.quantity_used_kg * self.feed.price_per_kg

    def save(self, *args, **kwargs):
        with transaction.atomic():

            if self.quantity_used_kg <= 0:
                raise ValidationError(
                    "Quantity must be greater than zero."
                )

            old_feed_id = None
            old_quantity = Decimal("0.00")

            if self.pk:
                old = FeedConsumption.objects.select_for_update().get(
                    pk=self.pk
                )
                old_feed_id = old.feed_id
                old_quantity = old.quantity_used_kg

            if old_feed_id:
                FeedStock.objects.filter(
                    pk=old_feed_id
                ).update(
                    quantity_kg=F('quantity_kg') + old_quantity
                )

            updated = FeedStock.objects.filter(
                pk=self.feed_id,
                quantity_kg__gte=self.quantity_used_kg
            ).update(
                quantity_kg=F('quantity_kg') - self.quantity_used_kg
            )

            if not updated:
                raise ValidationError(
                    "Not enough feed stock available."
                )

            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            FeedStock.objects.filter(
                pk=self.feed_id
            ).update(
                quantity_kg=F('quantity_kg') + self.quantity_used_kg
            )
            super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.batch} - {self.date}"
