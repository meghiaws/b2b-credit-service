from django.urls import include, path

from app.credits.apis.organization import OrganizationApi, OrganizationDetailApi, OrganizationIncreaseBalanceApi


organization_patterns = [
    path("", OrganizationApi.as_view(), name="organization"),
    path(
        "<int:organization_id>/",
        OrganizationDetailApi.as_view(),
        name="organization-detail",
    ),
    path(
        "<int:organization_id>/increase-balance/",
        OrganizationIncreaseBalanceApi.as_view(),
        name="organization-increase-balance",
    ),
]
urlpatterns = [
    path("organizations/", include((organization_patterns, "organizations"))),
]
