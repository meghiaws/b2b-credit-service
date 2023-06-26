from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app.authentication.serializers import CustomerSignupInputSerializer, OrganizationSignupInputSerializer
from app.authentication.services import AuthenticationService


class OrganizationSignupApi(APIView):
    def post(self, request):
        serializer = OrganizationSignupInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            AuthenticationService.organization_sign_up(
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
                organization_name=serializer.validated_data["organization_name"],
            )
        except Exception as ex:
            return Response(f"Error {ex}", status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)


class CustomerSignupApi(APIView):
    def post(self, request):
        serializer = CustomerSignupInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            AuthenticationService.customer_sign_up(
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
                phone=serializer.validated_data["phone"],
            )
        except Exception as ex:
            return Response(f"Error {ex}", status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)