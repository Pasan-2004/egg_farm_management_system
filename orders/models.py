
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class EggOrder(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Rejected', 'Rejected'),
    ]

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='egg_orders'
    )

    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    order_date = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    def __str__(self):
        return (
            f"Order #{self.id} - "
            f"{self.customer.username} - "
            f"{self.status}"
        )

class Notification(models.Model):

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    order = models.ForeignKey(
        EggOrder,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    message = models.CharField(
        max_length=255
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.message

class EggPrice(models.Model):
    price_per_egg = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Rs. {self.price_per_egg}"



