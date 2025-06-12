# # settings/base.py
# import os
# from pathlib import Path
# import dj_database_url
#
# BASE_DIR = Path(__file__).resolve().parent.parent
#
# SECRET_KEY = os.getenv("SECRET_KEY", "your-default-key")
# DEBUG = os.getenv("DEBUG", "True") == "True"
# ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")
#
# INSTALLED_APPS = [
#     "django.contrib.admin",
#     "django.contrib.auth",
#     "django.contrib.contenttypes",
#     "django.contrib.sessions",
#     "django.contrib.messages",
#     "django.contrib.staticfiles",
#     # твои кастомные приложения
# ]
#
# MIDDLEWARE = [
#     "django.middleware.security.SecurityMiddleware",
#     "whitenoise.middleware.WhiteNoiseMiddleware",  # если используешь whitenoise
#     "django.contrib.sessions.middleware.SessionMiddleware",
#     "django.middleware.common.CommonMiddleware",
#     "django.middleware.csrf.CsrfViewMiddleware",
#     "django.contrib.auth.middleware.AuthenticationMiddleware",
#     "django.contrib.messages.middleware.MessageMiddleware",
#     "django.middleware.clickjacking.XFrameOptionsMiddleware",
# ]
#
# ROOT_URLCONF = "crm_shop.urls"
#
# WSGI_APPLICATION = "crm_shop.wsgi.application"
#
# DATABASES = {
#     "default": dj_database_url.config(default=os.getenv("DATABASE_URL"))
# }
#
# STATIC_URL = "/static/"
# STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
#
# DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
