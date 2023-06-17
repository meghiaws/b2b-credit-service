from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import serializers, status
from drf_spectacular.utils import extend_schema

from app.credits.models import Organization
from app.credits.services.organization import OrganizationService
from app.credits.serializers.organization import (
    OrganizationIncreaseBalanceInputSerializer,
    OrganizationOutputSerializer,
    OrganizationDetailOutputSerializer,
)


# [POST, GET] api/organizations/
class OrganizationApi(APIView):
    @extend_schema(responses=OrganizationOutputSerializer)
    def get(self, request):
        query = OrganizationService.organization_list()

        serializer = OrganizationOutputSerializer(query, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# [GET, DELETE] api/organizations/{organization_id}/
class OrganizationDetailApi(APIView):
    @extend_schema(responses=OrganizationDetailOutputSerializer)
    def get(self, request, organization_id):
        defect_type = OrganizationService.organization_get(
            organization_id=organization_id
        )

        serializer = OrganizationDetailOutputSerializer(defect_type)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, organization_id):
        try:
            OrganizationService.organization_delete(organization_id=organization_id)
        except Exception as ex:
            return Response(f"Error {ex}", status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)


# [POST] api/organizations/{organization_id}/increase-balance/
class OrganizationIncreaseBalanceApi(APIView):
    @extend_schema(responses=OrganizationIncreaseBalanceInputSerializer)
    def post(self, request, organization_id):
        serializer = OrganizationIncreaseBalanceInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        OrganizationService.organization_increase_balance(
            organization_id=organization_id, **serializer.validated_data
        )

        return Response(status=status.HTTP_200_OK)
