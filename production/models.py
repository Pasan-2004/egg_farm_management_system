from django.db import models
from chickens.models import ChickenBatch


class EggProduction(models.Model):
    batch = models.ForeignKey(
        ChickenBatch,
        on_delete=models.PROTECT
    )
    date = models.DateField()
    eggs_collected = models.PositiveIntegerField()
    damaged_eggs = models.PositiveIntegerField(default=0)

    @property
    def good_eggs(self):
        return self.eggs_collected - self.damaged_eggs

    def __str__(self):
        return f"{self.batch} - {self.date}"