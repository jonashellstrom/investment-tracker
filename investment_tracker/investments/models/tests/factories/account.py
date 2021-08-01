import factory


class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "investments.Account"

    name = "Growth Account"
    account_type = "STANDARD"
    currency = "CAD"
    cash_position = 10_000
