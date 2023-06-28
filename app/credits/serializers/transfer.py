from decimal import Decimal
from rest_framework import serializers, status


class TransferInputSerializer(serializers.Serializer):
    organization_id = serializers.IntegerField(min_value=1)
    customer_phone = serializers.CharField()
    amount = serializers.DecimalField(
        max_digits=12, decimal_places=2, min_value=Decimal(0.01)
    )

    def validate_amount(self, value: Decimal):
        if float(value) < 0.01:
            raise serializers.ValidationError(
                {"message": "amount must be greater than or equal to 0.01"}
            )
        return value
