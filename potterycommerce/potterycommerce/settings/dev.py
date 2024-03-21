from .base import *
from django.core.management.utils import get_random_secret_key
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False") == "True"
#DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = "django-insecure-)o59lvz-83-d+v%0j=v5ak&+!z9*p3m(6k#1l)8v0vnm7iau6$"
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())
# SECURITY WARNING: define the correct hosts in production!
#ALLOWED_HOSTS = ["*"]
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "False") == "True"

try:
    from .local import *
except ImportError:
    pass

