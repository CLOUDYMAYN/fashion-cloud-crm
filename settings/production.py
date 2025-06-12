import os
from pathlib import Path
from .base import *

DEBUG = False

ALLOWED_HOSTS = ['fashion-cloud-crm-1.onrender.com']

import dj_database_url
DATABASES = {
    "default": dj_database_url.config(default=os.getenv("DATABASE_URL"))
}

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')