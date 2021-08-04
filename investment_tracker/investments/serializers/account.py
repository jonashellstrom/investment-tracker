from rest_framework import serializers

from investments.models.account import Account


class AccountSerializer(serializers.ModelSerializer):
    """
    Serializer for account model
    """

    class Meta:

        model = Account
        fields = "__all__"
