
from django.db import models
from chickens.models import ChickenBatch


class HealthRecord(models.Model):

    RECORD_TYPES = [
        ('Vaccination', 'Vaccination'),
        ('Disease', 'Disease'),
        ('Treatment', 'Treatment'),
    ]

    batch = models.ForeignKey(
        ChickenBatch,
        on_delete=models.PROTECT,
        related_name='health_records'
    )

    record_type = models.CharField(
        max_length=20,
        choices=RECORD_TYPES
    )

    date = models.DateField()

    description = models.TextField()

    medicine_or_vaccine = models.CharField(
        max_length=150,
        blank=True
    )

    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    next_due_date = models.DateField(
        null=True,
        blank=True
    )

    notes = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"{self.batch} - {self.record_type} - {self.date}"
