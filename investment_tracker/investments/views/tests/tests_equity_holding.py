from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from investments.models.tests.factories.equity_holding import EquityHoldingFactory
from investments.views.equity_holding import EquityHoldingList
from investments.views.equity_holding import EquityHoldingRetrieve


class TestEquityHoldingListView(TestCase):
    def setUp(self) -> None:
        self.holding = EquityHoldingFactory()
        self.account = self.holding.account
        self.holding_2 = EquityHoldingFactory(account=self.account)
        self.holdings = [self.holding, self.holding_2]

        self.request_factory = APIRequestFactory()
        self.view = EquityHoldingList.as_view()
        self.path = "accounts/{}/equity".format(self.account.id)

    def test_list_holdings(self):
        request = self.request_factory.get(self.path, format="json")
        response = self.view(request, account_id=self.account.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        holding_id_strings = [str(hld.id) for hld in self.holdings]

        for item in response.data:
            self.assertIn(item["id"], holding_id_strings)


class TestEquityHoldingRetrieveView(TestCase):
    def setUp(self) -> None:
        self.holding = EquityHoldingFactory()
        self.account = self.holding.account

        self.request_factory = APIRequestFactory()
        self.view = EquityHoldingRetrieve.as_view()
        self.path = "accounts/{}/equity/{}".format(self.account.id, self.holding.id)

    def test_retrieve_holding(self):
        request = self.request_factory.get(self.path, format="json")
        response = self.view(request, account_id=self.account.id, id=self.holding.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(self.holding.id))
        self.assertEqual(
            Decimal(response.data["cumulative_units"]), self.holding.cumulative_units
        )
        self.assertEqual(
            Decimal(response.data["cumulative_cost"]), self.holding.cumulative_cost
        )
        self.assertEqual(
            Decimal(response.data["average_purchase_price"]), self.holding.average_cost
        )
        self.assertEqual(
            Decimal(response.data["current_holding_value"]), self.holding.holding_value
        )
