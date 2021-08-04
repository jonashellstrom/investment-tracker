from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from investments.views.tests.force_authentication_mixin import ForceAuthenticationMixin
from investments.models.tests.factories.account import AccountFactory
from investments.views.account import AccountCreate, AccountRetrieve


class TestAccountCreateView(ForceAuthenticationMixin, TestCase):
    def setUp(self) -> None:
        self.account_name = "My Investment Account"
        self.account_cash_position = 10_000
        self.account_type = "STANDARD"

        self.request_factory = APIRequestFactory()
        self.view = AccountCreate.as_view()
        self.path = "accounts"
        super().setUp()

    def test_create_account(self):
        request = self.request_factory.post(
            self.path,
            data=dict(
                name=self.account_name,
                account_type=self.account_type,
                currency="CAD",
                cash_position=self.account_cash_position,
            ),
            format="json",
        )
        force_authenticate(request, user=self.user)
        response = self.view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], self.account_name)
        self.assertEqual(response.data["account_type"], self.account_type)
        self.assertEqual(
            response.data["cash_position"],
            "{:.2f}".format(self.account_cash_position),
        )


class TestAccountRetrieveView(ForceAuthenticationMixin, TestCase):
    def setUp(self) -> None:
        self.account = AccountFactory()

        self.request_factory = APIRequestFactory()
        self.view = AccountRetrieve.as_view()
        self.path = "accounts/{}".format(self.account.id)
        super().setUp()

    def test_retrieve_holding(self):
        request = self.request_factory.get(self.path, format="json")
        force_authenticate(request, user=self.user)
        response = self.view(request, id=self.account.id)

        expected_response_data = dict(
            id=str(self.account.id),
            name=self.account.name,
            account_type=self.account.account_type,
            currency=self.account.currency,
            cash_position="{:.2f}".format(self.account.cash_position),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response_data)
