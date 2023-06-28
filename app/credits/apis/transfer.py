from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from app.api.mixins import ApiAuthMixin

from app.credits.serializers.transfer import TransferInputSerializer
from app.credits.services.transfer import TransferService


# [POST] api/organizations/increase-balance/
class TransferApi(APIView):
    @extend_schema(responses=TransferInputSerializer)
    def post(self, request):
        serializer = TransferInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        TransferService.transfer_credit_by_phone_number(**serializer.validated_data)

        return Response(status=status.HTTP_200_OK)
