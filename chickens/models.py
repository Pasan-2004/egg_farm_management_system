from django.db import models

class ChickenBatch(models.Model):
    batch_name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    age_weeks = models.PositiveIntegerField()
    arrival_date = models.DateField()

    def __str__(self):
        return self.batch_name
