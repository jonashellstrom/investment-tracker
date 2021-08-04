import uuid
from django.db import models


class AbstractHolding(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticker = models.CharField(max_length=8)
    first_added_at = models.DateTimeField(auto_now_add=True)

    cumulative_units = models.DecimalField(max_digits=32, decimal_places=6, default=0)
    cumulative_cost = models.DecimalField(max_digits=16, decimal_places=2, default=0)

    last_ask_price = models.DecimalField(max_digits=16, decimal_places=2, default=0)

    @property
    def average_cost(self):
        "Returns the cost average for a holding"
        return (
            round(self.cumulative_cost / self.cumulative_units, 2)
            if self.cumulative_units
            else 0
        )

    @property
    def holding_value(self):
        "Returns the current holding value based on the last ask price"
        return round(self.cumulative_units * self.last_ask_price, 2)

    def add_holding(self, units, bid_price):
        self.cumulative_units += units
        self.cumulative_cost += units * bid_price
        self.save()

    def reduce_holding(self, units, ask_price):
        self.cumulative_units -= units
        self.cumulative_cost -= units * ask_price
        self.save()

    def update_last_ask_price(self, ask_price):
        self.last_ask_price = ask_price
        self.save()
