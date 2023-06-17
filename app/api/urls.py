from django.urls import include, path


urlpatterns = [
    path(
        "auth/",
        include(
            ("app.authentication.urls", "authentication"), namespace="authentication"
        ),
    ),
    path("", include(("app.credits.urls", "credits"), namespace="credits")),
]
