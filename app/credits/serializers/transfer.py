from decimal import Decimal
from rest_framework import serializers, status


class TransferInputSerializer(serializers.Serializer):
    destination_phone = serializers.CharField()
    amount = serializers.DecimalField(
        max_digits=12, decimal_places=2, min_value=Decimal(0.01)
    )
