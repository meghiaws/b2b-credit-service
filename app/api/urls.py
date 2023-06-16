from django.urls import include, path


urlpatterns = [
    path("defects/", include(("app.credits.urls", "credits"), namespace="credits")),
]