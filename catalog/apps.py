from django.apps import AppConfig
import os

class CatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalog'

    def ready(self):
        # Automatically create a superuser on startup if it doesn't exist
        from django.contrib.auth.models import User
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword123')
            print("🚀 Default superuser created: admin / adminpassword123")