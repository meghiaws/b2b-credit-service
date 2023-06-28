from decimal import Decimal
from django.core.validators import DecimalValidator
from rest_framework import serializers




# used in increase income api (api/increase-balance/)
class IncreaseBalanceInputSerializer(serializers.Serializer):
    organization_id = serializers.IntegerField(min_value=1)
    balance = serializers.DecimalField(max_digits=12, decimal_places=2)

    def validate_balance(self, value: Decimal):
        if float(value) < 0.01:
            raise serializers.ValidationError('Value must be greater than or equal to 0.01')
        return value