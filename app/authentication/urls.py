from django.urls import include, path

from app.authentication.apis import SignupApi


urlpatterns = [
    path("signup/", SignupApi.as_view(), name="signup"),
]