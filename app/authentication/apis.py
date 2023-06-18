from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app.authentication.serializers import SignupInputSerializer
from app.authentication.services import AuthenticationService


class SignupApi(APIView):
    def post(self, request):
        serializer = SignupInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            AuthenticationService.sign_up(
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
                phone=serializer.validated_data["phone"],
                organization_name=serializer.validated_data["organization_name"],
            )
        except Exception as ex:
            return Response(f"Error {ex}", status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)
