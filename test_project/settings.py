import os

DEBUG = True

# Test-only key. This project is a throwaway test harness that is never
# deployed anywhere; do not reuse this value for anything real.
SECRET_KEY = "django-insecure-test-project-key-not-for-production"

if os.environ.get("PSQL", "0") == "1":
    DATABASES = {
        "default": {
            "ENGINE": os.environ.get("PSQL_ENGINE", "django.db.backends.postgresql"),
            "NAME": os.environ.get("PSQL_NAME", "test_project"),
            "USER": os.environ.get("PSQL_USER", "postgres"),
            "PASSWORD": os.environ.get("PSQL_PASSWORD", ""),
            "HOST": os.environ.get("PSQL_HOST", "localhost"),
            "PORT": os.environ.get("PSQL_PORT", ""),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "test_project.sqlite3",
        }
    }

TIME_ZONE = "America/Chicago"
LANGUAGE_CODE = "en-us"
SITE_ID = 1
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(os.path.dirname(__file__), "static")

ROOT_URLCONF = "test_project.urls"

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "interval",
    "test_app",
]

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

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
