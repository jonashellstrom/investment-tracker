from django.test import TestCase
from investments.models.tests.factories.equity_holding import EquityHoldingFactory
from investments.models.equity_holding import NotSufficientFunds, NotSufficientUnits


class TestEquityHoldingModel(TestCase):
    def test_buy_units(self):
        equity_holding = EquityHoldingFactory()
        account = equity_holding.account
        prev_account_cash_position = account.cash_position

        prev_units = equity_holding.cumulative_units
        buying_units = 10
        ask_price = 51

        equity_holding.buy(buying_units, ask_price)
        equity_holding.refresh_from_db()

        self.assertEqual(equity_holding.cumulative_units, prev_units + buying_units)
        self.assertEqual(
            account.cash_position,
            prev_account_cash_position - (buying_units * ask_price),
        )

    def test_does_not_allow_buy_orders_higher_than_cash_position(self):
        with self.assertRaises(NotSufficientFunds):
            equity_holding = EquityHoldingFactory()
            account_cash_position = equity_holding.account.cash_position
            equity_holding.buy(1, account_cash_position + 1)

    def test_allows_buy_orders_within_cash_position(self):
        try:
            equity_holding = EquityHoldingFactory()
            account_cash_position = equity_holding.account.cash_position
            equity_holding.buy(1, account_cash_position - 1)
        except NotSufficientFunds as exc:
            assert False, "Raised an exception {}".format(exc)

    def test_sell_units(self):
        equity_holding = EquityHoldingFactory()
        account = equity_holding.account
        prev_account_cash_position = account.cash_position

        prev_units = equity_holding.cumulative_units
        selling_units = 20
        bid_price = 53

        equity_holding.sell(selling_units, bid_price)
        equity_holding.refresh_from_db()

        self.assertEqual(equity_holding.cumulative_units, prev_units - selling_units)
        self.assertEqual(
            account.cash_position,
            prev_account_cash_position + (selling_units * bid_price),
        )

    def test_does_not_allow_sell_orders_where_offered_units_exceed_available_units(
        self,
    ):
        with self.assertRaises(NotSufficientUnits):
            equity_holding = EquityHoldingFactory()
            available_units = equity_holding.cumulative_units
            equity_holding.sell(available_units + 1, 50)

    def test_allows_sell_orders_where_offered_units_are_within_available_units(self):
        try:
            equity_holding = EquityHoldingFactory()
            available_units = equity_holding.cumulative_units
            equity_holding.sell(available_units - 1, 50)
        except NotSufficientUnits as exc:
            assert False, "Raised an exception {}".format(exc)
