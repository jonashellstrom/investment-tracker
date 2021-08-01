import uuid

from django.db import models

ACCOUNT_TYPES = [
    ("STANDARD", "Standard cash or margin account"),
    ("TFSA", "Tax-Free Savings Account"),
    ("RRSP", "Registered Retirement Savings Plan"),
]
CURRENCIES = [("CAD", "Canadian Dollar"), ("USD", "U.S. Dollar")]


class Account(models.Model):
    """
    An investment account
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=32, blank=True)
    account_type = models.CharField(
        max_length=12, choices=ACCOUNT_TYPES, default="STANDARD"
    )
    currency = models.CharField(max_length=3, choices=CURRENCIES, default="CAD")
    cash_position = models.DecimalField(max_digits=16, decimal_places=2, default=0)

    def __str__(self):
        return "{} [{}]".format(self.name, self.account_type)
