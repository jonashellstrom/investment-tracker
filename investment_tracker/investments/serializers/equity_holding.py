from rest_framework import serializers

from investments.models.equity_holding import EquityHolding


class EquityHoldingSerializer(serializers.ModelSerializer):
    """
    Serializer for equity holding model
    """

    account = serializers.PrimaryKeyRelatedField(source="account.id", read_only=True)

    # Expose property attributes to view
    projected_dividend = serializers.DecimalField(max_digits=32, decimal_places=2)
    average_purchase_price = serializers.DecimalField(
        source="average_cost", max_digits=32, decimal_places=2
    )
    current_holding_value = serializers.DecimalField(
        source="holding_value", max_digits=32, decimal_places=2
    )

    class Meta:

        model = EquityHolding
        fields = (
            "id",
            "ticker",
            "exchange",
            "account",
            "cumulative_units",
            "cumulative_cost",
            "projected_dividend",
            "average_purchase_price",
            "current_holding_value",
        )
