from django.urls import include, path


urlpatterns = [
    path("defects/", include(("b2b_credit_service.credits.urls", "credits"), namespace="credits")),
]