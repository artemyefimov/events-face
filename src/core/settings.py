from datetime import timedelta
from pathlib import Path

from environ import Env

BASE_DIR = Path(__file__).resolve().parent.parent

env = Env(
    SECRET_KEY=(
        str,
        "django-insecure-y4-==%qs9uwc1e!1)^kex3z8vw(y$duzzd&^h8ig^nw1$l_o29",
    ),
    DEBUG=(bool, True),
    ALLOWED_HOSTS=(list[str], ["localhost", "127.0.0.1"]),
    DB_ENGINE=(str, "django.db.backends.sqlite3"),
    DB_NAME=(str, "sqlite3.db"),
    EVENTS_PROVIDER_URL=(str, "https://events.k3scluster.tech/api/events/"),
    EVENTS_PROVIDER_ACCESS_TOKEN=(
        str,
        "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc19zdGFmZiI6ZmFsc2UsInN1YiI6IjI2IiwiZXhwIjoxNzY0ODI0NTQ3LCJpYXQiOjE3NjQ3MzgxNDd9.cla59HPFh4X9JgepHvfAqZ2XLx9X4JR8nZddvePrk0mZ1D9ZUCDsmxUHDcJw82am4H0kEdHKBP4f4q0AvlpfGNCnnFbrffXw5nYEPZVzKBJWEz0yU48BoSRsCEI2CMlG0e4q3B-Gfft3p8CsNC1mUN2KSj-i6a1GGbgqSM50e5visD581ThlFQZcgRCzypoE7pkC9WVJ8x2RJloiSqo6oLlzqRY0WBM2z_HutBz0THezwwBjP4r4Qt_2S9E59sgSOo9q3hdEFeECUVlVBn0I_BnbIFxoDk2z20xNbek2Fmro8_vbDMPJweolNOrCoxiEB2XZrJJ2GZM3Vwta3kNLdQ",
    ),
    NOTIFICATIONS_URL=(str, "https://notifications.k3scluster.tech/api/notifications"),
    NOTIFICATIONS_ACCESS_TOKEN=(
        str,
        "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc19zdGFmZiI6ZmFsc2UsInN1YiI6IjI2IiwiZXhwIjoxNzY0ODI0NTQ3LCJpYXQiOjE3NjQ3MzgxNDd9.cla59HPFh4X9JgepHvfAqZ2XLx9X4JR8nZddvePrk0mZ1D9ZUCDsmxUHDcJw82am4H0kEdHKBP4f4q0AvlpfGNCnnFbrffXw5nYEPZVzKBJWEz0yU48BoSRsCEI2CMlG0e4q3B-Gfft3p8CsNC1mUN2KSj-i6a1GGbgqSM50e5visD581ThlFQZcgRCzypoE7pkC9WVJ8x2RJloiSqo6oLlzqRY0WBM2z_HutBz0THezwwBjP4r4Qt_2S9E59sgSOo9q3hdEFeECUVlVBn0I_BnbIFxoDk2z20xNbek2Fmro8_vbDMPJweolNOrCoxiEB2XZrJJ2GZM3Vwta3kNLdQ",
    ),
    NOTIFICATIONS_OWNER_ID=(str, "76442b72-4129-4d57-8108-c8a160fbdd73"),
)

SECRET_KEY = env("SECRET_KEY")

DEBUG = env("DEBUG")

ALLOWED_HOSTS = env("ALLOWED_HOSTS")

EVENTS_PROVIDER_URL = env("EVENTS_PROVIDER_URL")
EVENTS_PROVIDER_ACCESS_TOKEN = env("EVENTS_PROVIDER_ACCESS_TOKEN")

NOTIFICATIONS_URL = env("NOTIFICATIONS_URL")
NOTIFICATIONS_ACCESS_TOKEN = env("NOTIFICATIONS_ACCESS_TOKEN")
NOTIFICATIONS_OWNER_ID = env("NOTIFICATIONS_OWNER_ID")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "django_filters",
    "events",
    "auth_app",
]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

ROOT_URLCONF = "urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = "core.asgi.application"

DB_ENGINE = env("DB_ENGINE")

if DB_ENGINE == "django.db.backends.sqlite3":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / env("DB_NAME"),  # type: ignore
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": DB_ENGINE,
            "NAME": env("DB_NAME"),
            "USER": env("DB_USER"),
            "PASSWORD": env("DB_PASSWORD"),
            "HOST": env("DB_HOST"),
            "PORT": env("DB_PORT"),
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


STATIC_URL = "static/"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
