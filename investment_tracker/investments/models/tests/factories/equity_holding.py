import factory


class EquityHoldingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "investments.EquityHolding"

    exchange = "TSX"
    account = factory.SubFactory(
        "investments.models.tests.factories.account.AccountFactory"
    )
    dividend_yield = 0.05
    dividend_schedule = ["JAN", "APR", "JUL", "OCT"]

    ticker = "ENB"

    cumulative_units = 100
    cumulative_cost = 5000

    last_ask_price = 49.50
