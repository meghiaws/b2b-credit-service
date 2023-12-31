from decimal import Decimal
from rest_framework import serializers, status

from app.credits.models import Organization

# used in list api (api/organizations/)
class OrganizationOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ("id", "name", "user_id", "balance")


# used in detail api (api/organizations/{id})
class OrganizationDetailInputSerializer(serializers.Serializer):
    name = serializers.CharField()
    phone = serializers.CharField(max_length=11)


class OrganizationDetailOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ("id", "name", "user_id", "balance")