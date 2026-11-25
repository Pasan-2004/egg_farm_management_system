
from django.db import models
from django.core.validators import MinValueValidator


class ChickenBatch(models.Model):

    batch_name = models.CharField(
        max_length=100
    )

    breed = models.CharField(
        max_length=100
    )

    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    age_weeks = models.PositiveIntegerField()

    arrival_date = models.DateField()

    def __str__(self):
        return self.batch_name
