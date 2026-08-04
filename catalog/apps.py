from django.apps import AppConfig
import os
import sys

class CatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalog'

    def ready(self):
        # Only run when the live server (gunicorn or runserver) is starting up
        if 'runserver' in sys.argv or 'gunicorn' in ''.join(sys.argv):
            try:
                from django.contrib.auth.models import User
                from catalog.models import Movie
                from django.core.management import call_command
                
                # 1. Ensure superuser exists
                if not User.objects.filter(is_superuser=True).exists():
                    User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword123')
                    print("🚀 Default superuser created: admin / adminpassword123")
                
                # 2. If database has no movies, automatically run load_movies command!
                if Movie.objects.count() == 0:
                    print("🎬 Database is empty. Running load_movies command automatically...")
                    call_command('load_movies')
                    print("✅ Movies successfully loaded from TMDB on startup!")
            except Exception as e:
                print(f"Startup task note: {e}")