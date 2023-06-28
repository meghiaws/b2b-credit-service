from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from app.credits.serializers.increase_balance import IncreaseBalanceInputSerializer
from app.credits.services.increase_balance import IncreaseBalanceService
from app.credits.serializers.increase_balance import (
    IncreaseBalanceInputSerializer,
)



# [POST] api/organizations/increase-balance/
class IncreaseBalanceApi(APIView):
    @extend_schema(responses=IncreaseBalanceInputSerializer)
    def post(self, request):
        serializer = IncreaseBalanceInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        IncreaseBalanceService.increase_balance(
            **serializer.validated_data
        )

        return Response(status=status.HTTP_200_OK)
