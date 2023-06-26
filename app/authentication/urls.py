from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from app.authentication.apis import CustomerSignupApi, OrganizationSignupApi


urlpatterns = [
    path("organizations/signup/", OrganizationSignupApi.as_view(), name="organizations-signup"),
    path("customers/signup/", CustomerSignupApi.as_view(), name="customers-signup"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
