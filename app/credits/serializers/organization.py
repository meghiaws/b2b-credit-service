from decimal import Decimal
from rest_framework import serializers, status

from app.credits.models import Organization


class OrganizationOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ("id", "name", "user_id", "balance")


class OrganizationDetailOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ("id", "name", "user_id", "balance")


class OrganizationIncreaseBalanceInputSerializer(serializers.Serializer):
    balance = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=Decimal(0.01))