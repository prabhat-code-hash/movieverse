import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from catalog.models import Movie, Genre, Language, Platform

class Command(BaseCommand):
    help = 'Fetch movies from TMDB API and load them into the database'

    def handle(self, *args, **kwargs):
        API_KEY = '016aca931b22034987e9d84eccfcd493'
        
        if API_KEY == 'YOUR_API_KEY_HERE':
            self.stdout.write(self.style.ERROR("⚠️ STOP! You need to put your real TMDB API key in the script!"))
            return

        # ==========================================
        # NEW: Loop through pages 1 to 5 (100 movies)
        # To get 1000 movies, change to range(1, 51)
        # ==========================================
        for page_number in range(1, 51):
            self.stdout.write(f"\nFetching popular movies from TMDB (Page {page_number})...")
            
            url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=en-US&page={page_number}"
            response = requests.get(url)
            popular_movies = response.json().get('results', [])

            for item in popular_movies:
                movie_id = item['id']
                
                # UPDATE: We added "&append_to_response=credits" to the end of this URL
                details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&append_to_response=credits"
                details = requests.get(details_url).json()

                title = details.get('title', 'Unknown Title')
                description = details.get('overview', 'No description available.')
                release_date = details.get('release_date')
                
                if not release_date:
                    continue 

                movie, created = Movie.objects.get_or_create(
                    title=title,
                    defaults={
                        'description': description,
                        'release_date': release_date,
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f"🎬 Created: {movie.title}"))
                    
                    poster_path = details.get('poster_path')
                    if poster_path:
                        image_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                        img_response = requests.get(image_url)
                        if img_response.status_code == 200:
                            file_name = f"{movie_id}_poster.jpg"
                            movie.poster.save(file_name, ContentFile(img_response.content), save=True)

                    for genre_data in details.get('genres', []):
                        genre_obj, _ = Genre.objects.get_or_create(name=genre_data['name'])
                        movie.genres.add(genre_obj)

                    for lang_data in details.get('spoken_languages', []):
                        lang_obj, _ = Language.objects.get_or_create(name=lang_data['english_name'])
                        movie.languages.add(lang_obj)
                        
                    # NEW: Get the top 5 cast members from the TMDB credits data
                    cast_data = details.get('credits', {}).get('cast', [])[:5]
                    
                    # We import Actor locally here to avoid circular imports at the top
                    from catalog.models import Actor 
                    for actor_data in cast_data:
                        actor_obj, _ = Actor.objects.get_or_create(name=actor_data['name'])
                        movie.cast.add(actor_obj)
                else:
                    self.stdout.write(self.style.WARNING(f"⚠️ Already exists: {movie.title}"))

        self.stdout.write(self.style.SUCCESS("\n✅ Successfully imported all TMDB pages!"))