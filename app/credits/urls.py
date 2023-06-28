from django.urls import include, path
from app.credits.apis.increase_balance import IncreaseBalanceApi

from app.credits.apis.organization import (
    OrganizationApi,
    OrganizationDetailApi,
)
from app.credits.apis.transfer import TransferApi


organization_patterns = [
    path("", OrganizationApi.as_view(), name="organization"),
    path(
        "<int:organization_id>/",
        OrganizationDetailApi.as_view(),
        name="organization-detail",
    ),
]

increase_balance_patterns = [
    path(
        "",
        IncreaseBalanceApi.as_view(),
        name="increase-balance",
    )
]

transfer_patterns = [
    path("", TransferApi.as_view(), name="transfer"),
]

urlpatterns = [
    path("organizations/", include((organization_patterns, "organizations"))),
    path(
        "increase-balance/", include((increase_balance_patterns, "increase-balances"))
    ),
    path("transfer/", include((transfer_patterns, "transfers"))),
]
