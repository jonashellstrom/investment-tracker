from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory, force_authenticate

from investments.models.tests.factories.equity_holding import EquityHoldingFactory
from investments.views.equity_holding import EquityHoldingListCreate
from investments.views.equity_holding import EquityHoldingRetrieve


class ForceAuthenticationMixin:
    def setUp(self) -> None:
        User = get_user_model()
        self.user = User.objects.create_user(username="foo", password="bar")


class TestEquityHoldingListCreateView(ForceAuthenticationMixin, TestCase):
    def setUp(self) -> None:
        self.holding = EquityHoldingFactory()
        self.account = self.holding.account
        self.holding_2 = EquityHoldingFactory(account=self.account)
        self.holdings = [self.holding, self.holding_2]

        self.request_factory = APIRequestFactory()
        self.view = EquityHoldingListCreate.as_view()
        self.path = "accounts/{}/equity".format(self.account.id)
        super().setUp()

    def test_list_holdings(self):
        request = self.request_factory.get(self.path, format="json")
        force_authenticate(request, user=self.user)
        response = self.view(request, account_id=self.account.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        holding_id_strings = [str(hld.id) for hld in self.holdings]

        for item in response.data:
            self.assertIn(item["id"], holding_id_strings)

    def test_create_holding(self):
        request = self.request_factory.post(
            self.path,
            data=dict(ticker="RY.TO", exchange="TSX", dividend_schedule=["JAN"]),
            format="json",
        )
        force_authenticate(request, user=self.user)
        response = self.view(request, account_id=self.account.id)

        self.assertEqual(response.status_code, 201)


class TestEquityHoldingRetrieveView(ForceAuthenticationMixin, TestCase):
    def setUp(self) -> None:
        self.holding = EquityHoldingFactory()
        self.account = self.holding.account

        self.request_factory = APIRequestFactory()
        self.view = EquityHoldingRetrieve.as_view()
        self.path = "accounts/{}/equity/{}".format(self.account.id, self.holding.id)
        super().setUp()

    def test_retrieve_holding(self):
        request = self.request_factory.get(self.path, format="json")
        force_authenticate(request, user=self.user)
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
