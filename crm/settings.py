from pathlib import Path
import django_heroku
import pyrebase

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-vxbo_p3fw2z^q(-0z&s52mtfo7ql$l#tf63awy3ww(nk^is=u@"

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "strava",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "crm.urls"

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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

SECURE_SSL_REDIRECT = False

STATIC_URL = "staticfiles"
django_heroku.settings(locals())

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Firebase
config = {
    "apiKey": "AIzaSyDw-AwAd3BKC7OCcPAQvl3wGfd1L5bb5HQ",
    "authDomain": "jahn-strava.firebaseapp.com",
    "projectId": "jahn-strava",
    "storageBucket": "jahn-strava.appspot.com",
    "messagingSenderId": "338542951365",
    "appId": "1:338542951365:web:a1d3246cd529880d72e9ac",
    "measurementId": "G-L99XGR7RQY",
    "databaseURL": "https://jahn-strava-default-rtdb.firebaseio.com",
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()
