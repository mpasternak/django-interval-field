
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

usePSQL = False
if "PSQL" is os.environ:
    try:
        usePSQL = int(os.environ["PSQL"])
    except ValueError:
        usePSQL = os.environ["PSQL"]

if os.environ.get("PSQL", "0") == "1":
    print("Using PostgreSQL as the database backend")
    os.environ.setdefault("PSQL_ENGINE", "django.db.backends.postgresql_psycopg2")
    if "TRAVIS" in os.environ:
        os.environ.setdefault("PSQL_NAME", "travisci")
        os.environ.setdefault("PSQL_USER", "postgres")

    DATABASES = {
        'default': {
            'ENGINE':   os.environ.get("PSQL_ENGINE"),
            'NAME':     os.environ.get("PSQL_NAME"),
            'USER':     os.environ.get("PSQL_USER"),
            'PASSWORD': os.environ.get("PSQL_PASSWORD", ""),
            'HOST':     os.environ.get("PSQL_HOST", "localhost"),
            'PORT':     os.environ.get("PSQL_POST", ""),
        }
    }
else:
    print("Using SQLite3 as the database backend")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'test_project.sqlite3',
        }
}

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1

USE_I18N = True

USE_L10N = True

MEDIA_ROOT = ''

MEDIA_URL = ''

STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = '2m4%%l9nrwwd!p3#1xuk)oy-c$lfjsj(a2q^8#u@v(47#@&&^6'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'test_project.urls'

TEMPLATE_DIRS = (
)

STATIC_ROOT = os.path.join(
    os.path.dirname(__file__),
    'static'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'interval',
    'test_app'
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

TEST_RUNNER = 'django.test.runner.DiscoverRunner'
