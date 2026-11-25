
from django.contrib import admin
from .models import EggOrder, EggPrice, Notification


@admin.register(EggPrice)
class EggPriceAdmin(admin.ModelAdmin):
    list_display = ('price_per_egg', 'updated_at')


admin.site.register(EggOrder)
admin.site.register(Notification)

