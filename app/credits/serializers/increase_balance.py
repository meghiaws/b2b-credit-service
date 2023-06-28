from decimal import Decimal
from django.core.validators import DecimalValidator
from rest_framework import serializers


# used in increase income api (api/increase-balance/)
class IncreaseBalanceInputSerializer(serializers.Serializer):
    organization_id = serializers.IntegerField(min_value=1)
    balance = serializers.DecimalField(
        max_digits=12, decimal_places=2, min_value=Decimal("0.01")
    )

    def validate_balance(self, value: Decimal):
        if value < Decimal("0.01"):
            raise serializers.ValidationError(
                "Ensure value is greater than or equal to 0.01"
            )
        return value
