from django.db import models
from django.core.validators import MinValueValidator
from chickens.models import ChickenBatch


class MortalityRecord(models.Model):

    batch = models.ForeignKey(
        ChickenBatch,
        on_delete=models.PROTECT
    )

    date = models.DateField()

    dead_count = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    reason = models.CharField(
        max_length=200
    )

    notes = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"{self.batch} - {self.dead_count} deaths"