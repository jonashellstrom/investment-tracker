import uuid
from django.db import models


class AbstractHolding(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticker = models.CharField(max_length=8)
    first_added_at = models.DateTimeField(auto_now_add=True)

    cumulative_units = models.DecimalField(max_digits=32, decimal_places=6, default=0)
    cumulative_cost = models.DecimalField(max_digits=16, decimal_places=2, default=0)

    last_ask_price = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    holdings_value = models.DecimalField(max_digits=32, decimal_places=2, default=0)

    class Meta:
        abstract = True

    def get_average_cost(self):
        return round(self.cumulative_cost + self.cumulative_units, 2)

    def add_holding(self, units, bid_price):
        self.cumulative_units += units
        self.cumulative_cost += units * bid_price
        self.save()

    def reduce_holding(self, units, ask_price):
        self.cumulative_units -= units
        self.cumulative_cost -= units * ask_price
        self.save()

    def _update_holdings_value(self, new_price):
        self.holdings_value = self.cumulative_units * new_price
        self.save()

    def update_last_ask_price(self, ask_price):
        self.last_ask_price = ask_price
        self.save()
        self._update_holdings_value(ask_price)
