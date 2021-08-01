from django.db import models
from django.contrib.postgres.fields import ArrayField
from investments.models.abstract_holding import AbstractHolding


class NotSufficientFunds(Exception):
    def __init__(self, message="Not sufficient funds for this trade") -> Exception:
        self.message = message


DIVIDEND_MONTHS = [
    ("JAN", "January"),
    ("FEB", "February"),
    ("MAR", "March"),
    ("APR", "April"),
    ("MAY", "May"),
    ("JUN", "June"),
    ("JUL", "July"),
    ("AUG", "August"),
    ("SEP", "September"),
    ("OCT", "October"),
    ("NOV", "November"),
    ("DEC", "December"),
]


class EquityHolding(AbstractHolding):

    exchange = models.CharField(max_length=32, blank=True)
    account = models.ForeignKey("Account", on_delete=models.CASCADE)
    dividend_yield = models.DecimalField(max_digits=16, decimal_places=3, default=0)
    dividend_schedule = ArrayField(
        models.CharField(max_length=3, blank=True, choices=DIVIDEND_MONTHS),
        default=list,
    )

    def __str__(self):
        return "Investment in {}, traded on {}".format(self.ticker, self.exchange)

    def _check_sufficient_cash_position(self, trade_value):
        if trade_value > self.account.cash_position:
            raise NotSufficientFunds(
                "Cash position of {} in {} does not cover trade value of {}".format(
                    self.account.cash_position, self.account.__str__(), trade_value
                )
            )

    def buy(self, units, ask_price):
        trade_value = units * ask_price
        self._check_sufficient_cash_position(trade_value)
        self.add_holding(units, ask_price)
        account = self.account
        account.cash_position -= trade_value
        account.save()

    def sell(self, units, bid_price):
        trade_value = units * bid_price
        self.add_holding(units, bid_price)
        account = self.account
        account.cash_position += trade_value
        account.save()

    def projected_dividend(self):
        return round(self.holdings_value * self.dividend_yield, 2)
