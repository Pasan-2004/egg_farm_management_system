
from decimal import Decimal
from datetime import date

from django.db import transaction

from feed.models import FeedStock, FeedConsumption
from chickens.models import ChickenBatch


stock = FeedStock.objects.filter(
    quantity_kg__gte=Decimal("1.00")
).first()

batch = ChickenBatch.objects.first()

if stock is None or batch is None:
    print("ERROR: Feed stock or chicken batch not found.")

else:
    before = stock.quantity_kg

    try:
        with transaction.atomic():

            record = FeedConsumption(
                batch=batch,
                feed=stock,
                date=date.today(),
                quantity_used_kg=Decimal("1.00")
            )

            record.save()

            stock.refresh_from_db()

            print("Before:", before)
            print("After saving:", stock.quantity_kg)
            print("Expected:", before - Decimal("1.00"))

            # Roll back all test changes
            transaction.set_rollback(True)

    except Exception as error:
        print("ERROR:", error)

    stock.refresh_from_db()

    print("After rollback:", stock.quantity_kg)
