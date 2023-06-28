from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from app.credits.models import Customer, Organization


class OrganizationSignupInputSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    password2 = serializers.CharField()
    organization_name = serializers.CharField()

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError("Entered passwords doesn't match.")
        return attrs


class CustomerSignupInputSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    password2 = serializers.CharField()
    phone = serializers.CharField(
        max_length=11, validators=[UniqueValidator(queryset=Customer.objects.all())]
    )

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError("Entered passwords doesn't match.")
        return attrs