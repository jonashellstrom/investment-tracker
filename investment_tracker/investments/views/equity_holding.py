from rest_framework import generics
from investments.models.equity_holding import EquityHolding
from investments.serializers.equity_holding import EquityHoldingSerializer
from investments.views.pagination import HoldingPagination


class MultipleFieldLookupMixin:
    def get_object(self):
        queryset = self.get_queryset()  # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        multi_filter = {field: self.kwargs[field] for field in self.lookup_fields}
        obj = generics.get_object_or_404(queryset, **multi_filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj


class EquityHoldingRetrieve(MultipleFieldLookupMixin, generics.RetrieveAPIView):
    """
    Detail view for an equity holding.
    """

    queryset = EquityHolding.objects.all()
    serializer_class = EquityHoldingSerializer
    lookup_fields = ["account_id", "id"]


class EquityHoldingList(generics.ListAPIView):
    """
    List view for equity holdings.
    """

    queryset = EquityHolding.objects.all()
    should_paginate = True
    pagination_class = HoldingPagination
    serializer_class = EquityHoldingSerializer

    def get_queryset(self):
        """
        Retrieve the set of EquityHolding records for an account
        """
        account_id = self.kwargs.get("account_id")
        return super().get_queryset().filter(account_id=account_id)
