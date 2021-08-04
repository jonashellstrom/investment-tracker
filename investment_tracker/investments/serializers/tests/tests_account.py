from decimal import Decimal
from django.test import TestCase

from investments.models.tests.factories.account import AccountFactory
from investments.serializers.account import AccountSerializer


class TestAccountSerializer(TestCase):
    def setUp(self) -> None:
        self.account = AccountFactory()

    def test_serializer_attributes(self):
        serializer = AccountSerializer(self.account)

        expected_data = dict(
            id=str(self.account.id),
            name=self.account.name,
            account_type=self.account.account_type,
            currency=self.account.currency,
            cash_position="{:.2f}".format(self.account.cash_position),
        )

        self.assertEqual(serializer.data, expected_data)
