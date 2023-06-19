from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(("app.api.urls", "api"), namespace="apis")),
    # Swagger endpoints
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(), name="swagger"),
    path("api/redoc/", SpectacularRedocView.as_view(), name="redoc"),
]

# add django-debug-toolbar urls if the environment is "dev"
from config.settings.debug_toolbar.setup import DebugToolbarSetup

urlpatterns = DebugToolbarSetup.do_urls(urlpatterns)