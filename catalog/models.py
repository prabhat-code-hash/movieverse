from django.db import models  # type: ignore[import]
from django.db.models import Avg # type: ignore[import]
from django.contrib.auth.models import User  # type: ignore[import] # Built-in User model

# Create your models here.
# OTT Platform Model
class Platform(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()

    # This makes the platform name show up nicely in the admin panel
    def __str__(self):
        return self.name

# Movie Model
class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    
    # Many-to-Many: A movie can be on Netflix AND Hulu. Netflix has MANY movies.
    platforms = models.ManyToManyField(Platform)
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)
    genres = models.ManyToManyField('Genre', related_name='movies', blank=True)
    languages = models.ManyToManyField('Language', related_name='movies', blank=True)
    cast = models.ManyToManyField('Actor', related_name='movies', blank=True)

    @property
    def average_rating(self):
        # We use aggregate to get the average of all the 'rating' fields from related reviews
        result = self.reviews.aggregate(Avg('rating'))
        if result['rating__avg']:
            return round(result['rating__avg'], 1) # Round to 1 decimal place
        return "No ratings yet"

    def __str__(self):
        return self.title

# Song Model
class Song(models.Model):
    title = models.CharField(max_length=200)
    singer = models.CharField(max_length=200)
    
    # One-to-Many: A song belongs to ONE movie. A movie has MANY songs.
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='songs')

    def __str__(self):
        return f"{self.title} ({self.singer})"

#Review Model
class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 11)]) # 1 to 10
    comment = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} ({self.rating}/10)"

#Watchlist Model
class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    movies = models.ManyToManyField(Movie, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Watchlist"

#Genre Model
class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

#language Model
class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

#Actor Model
class Actor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


