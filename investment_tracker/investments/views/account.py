from rest_framework.generics import (
    RetrieveAPIView,
    CreateAPIView,
)

from investments.models.account import Account
from investments.serializers.account import AccountSerializer
from investments.views.auth import AuthMixin


class AccountRetrieve(AuthMixin, RetrieveAPIView):
    """
    Retrieve view for an equity holding.
    """

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_field = "id"


class AccountCreate(AuthMixin, CreateAPIView):
    """
    Create view for equity holdings.
    """

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
