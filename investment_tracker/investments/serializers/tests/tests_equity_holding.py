from decimal import Decimal
from django.test import TestCase

from investments.models.tests.factories.equity_holding import EquityHoldingFactory
from investments.serializers.equity_holding import (
    EquityHoldingSerializer,
)


class TestEquityHoldingSerializer(TestCase):
    def setUp(self) -> None:
        self.holding = EquityHoldingFactory()
        self.account = self.holding.account

    def test_includes_account(self):
        serializer = EquityHoldingSerializer(self.holding)
        self.assertIn("account", serializer.data)
        self.assertEqual(serializer.data["account"], self.account.id)

    def test_includes_property_attributes(self):
        serializer = EquityHoldingSerializer(self.holding)

        self.assertIn("projected_dividend", serializer.data)
        self.assertIn("average_purchase_price", serializer.data)
        self.assertIn("current_holding_value", serializer.data)

        self.assertEqual(
            Decimal(serializer.data["projected_dividend"]),
            self.holding.projected_dividend,
        )
        self.assertEqual(
            Decimal(serializer.data["average_purchase_price"]),
            self.holding.average_cost,
        )
        self.assertEqual(
            Decimal(serializer.data["current_holding_value"]),
            self.holding.holding_value,
        )
