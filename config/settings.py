import os
from pathlib import Path

from config.env import BASE_DIR, env


env.read_env(os.path.join(BASE_DIR, ".env"))

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "bx!1h^dv*s5t3py4qjf%lbl_^te-tbf@$_e(bo-%+ag6^ax*xx"

DEBUG = True

ALLOWED_HOSTS = []

LOCAL_APPS = [
    "b2b_credit_service.credits.apps.CreditsConfig",
    "b2b_credit_service.api.apps.ApiConfig",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "drf_spectacular",
    "django_extensions",
    "debug_toolbar",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    *THIRD_PARTY_APPS,
    *LOCAL_APPS,
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda request: True}

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": env.str("DB_NAME", "credit_service"),
#         "USER": env.str("DB_USER", "postgres"),
#         "PASSWORD": env.str("DB_PASSWORD", "password"),
#         "HOST": env.str("DB_HOST", "localhost"),
#         "PORT": env.str("DB_PORT", 5432),
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "credit_service",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "localhost",
        "PORT": 5432,
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"

MEDIA_ROOT_NAME = "media"
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_ROOT_NAME)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SHELL_PLUS_PRINT_SQL = True

# https://docs.celeryproject.org/en/stable/userguide/configuration.html
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND")
CELERY_TIMEZONE = "UTC"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "loggers": {
        "api": {
            "handlers": ["console"],
            "level": os.environ.get("DJANGO_LOG_LEVEL", "DEBUG"),
        },
        "django": {
            "handlers": ["console"],
            "propagate": True,
            "level": "INFO",
        },
    },
    "formatters": {
        "verbose": {
            "format": "[{asctime}] ({levelname}) - {name} - {message}",
            "datefmt": "%Y/%m/%d %H:%M:%S",
            "style": "{",
        }
    },
}