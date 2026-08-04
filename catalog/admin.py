from django.contrib import admin  # type: ignore[reportMissingImports]
from .models import Platform, Movie, Song, Genre, Language, Actor  # type: ignore[reportMissingImports]

# Register your models here.
admin.site.register(Platform)
admin.site.register(Movie)
admin.site.register(Song)
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Actor)
