from .base import *

DEBUG = False

ALLOWED_HOSTS = ['fashion-cloud-crm-1.onrender.com']

# Поддержка базы данных через URL:
import dj_database_url
DATABASES = {
    "default": dj_database_url.config(default=os.getenv("DATABASE_URL"))
}
