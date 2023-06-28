from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from app.credits.models import Organization

from app.credits.services.organization import OrganizationService
from app.credits.serializers.organization import (
    OrganizationDetailInputSerializer,
    OrganizationOutputSerializer,
    OrganizationDetailOutputSerializer,
)


# [GET] api/organizations/
class OrganizationApi(APIView):
    @extend_schema(responses=OrganizationOutputSerializer)
    def get(self, request):
        query = OrganizationService.organization_list()

        serializer = OrganizationOutputSerializer(query, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# [GET, PUT, DELETE] api/organizations/{organization_id}/
class OrganizationDetailApi(APIView):
    @extend_schema(responses=OrganizationDetailInputSerializer)
    def put(self, request, organization_id):
        serializer = OrganizationDetailInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        OrganizationService.organization_update(
            organization_id=organization_id, **serializer.validated_data
        )

        return Response(status=status.HTTP_200_OK)

    @extend_schema(responses=OrganizationDetailOutputSerializer)
    def get(self, request, organization_id):
        try:
            organization = OrganizationService.organization_get(
                organization_id=organization_id
            )
        except Organization.DoesNotExist:
            return Response(
                {"message": "organization with provided id does not exists."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = OrganizationDetailOutputSerializer(organization)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, organization_id):
        try:
            OrganizationService.organization_delete(organization_id=organization_id)
        except Exception as ex:
            return Response(f"Error {ex}", status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)
