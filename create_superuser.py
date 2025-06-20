# create_superuser.py
from django.contrib.auth import get_user_model

User = get_user_model()
username = "admin"
password = "adminpass123"
email = "admin@example.com"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("✔ Superuser created")
else:
    print("ℹ Superuser already exists")
