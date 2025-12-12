SECRET_KEY = "fake-key"

INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    # Extra apps
    "captcha",
    "django_celery_beat",
    # Local apps
    "core_main_app",
    "core_main_registry_app",
    "core_website_app",
    "core_parser_app",
    "core_curate_app",
    "core_user_registration_app",
    "tests",
]

# SERVER URI
SERVER_URI = "http://example.com"

# IN-MEMORY TEST DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}

MIDDLEWARE = (
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core_main_app.utils.custom_context_processors.domain_context_processor",  # Needed by any curator app
                "django.template.context_processors.i18n",
            ],
        },
    },
]

LOGIN_URL = "/login"
STATIC_URL = "/static/"
ROOT_URLCONF = "tests.urls"
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
PASSWORD_HASHERS = ("django.contrib.auth.hashers.UnsaltedMD5PasswordHasher",)

DATA_SORTING_FIELDS = ["+title"]

CUSTOM_NAME = "Curator"
ENABLE_ALLAUTH = False
ENABLE_SAML2_SSO_AUTH = False
CELERYBEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = False
MONGODB_INDEXING = False
MONGODB_ASYNC_SAVE = False

CELERY_ALWAYS_EAGER = True
