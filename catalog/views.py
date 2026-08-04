from django.shortcuts import render,get_object_or_404,redirect  # type: ignore[import]
from .models import Movie,Review,Watchlist
from .forms import ReviewForm
from django.contrib.auth.forms import UserCreationForm # type: ignore[import]
from django.contrib.auth import login  # type: ignore[import]
from django.contrib.auth.decorators import login_required # type: ignore[import]
from django.db.models import Avg # type: ignore[import]


@login_required
def user_profile(request):
    # Get the user's watchlist (or create an empty one if it doesn't exist)
    watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    
    # Get all the reviews this user has written
    user_reviews = Review.objects.filter(user=request.user)
    
    context = {
        'watchlist': watchlist.movies.all(),
        'reviews': user_reviews
    }
    return render(request, 'catalog/profile.html', context)

# Create your views here.
def movie_list(request):
    query = request.GET.get('q') 
    sort_by = request.GET.get('sort')
    platform_filter = request.GET.get('platform')
    
    # Start with all movies, and 'annotate' them with a temporary average rating column so we can sort them!
    all_movies = Movie.objects.annotate(avg_rating=Avg('reviews__rating'))

    if query:
        all_movies = all_movies.filter(title__icontains=query)
        
    if platform_filter:
        # Filter where the related platforms list contains a platform with this exact name
        all_movies = all_movies.filter(platforms__name__iexact=platform_filter)

    if sort_by == 'top_rated':
        # Sort by the annotated average rating (the minus sign means descending order)
        all_movies = all_movies.order_by('-avg_rating')
        
    context = {
        'movies': all_movies, 
        'query': query,
    }
    return render(request, 'catalog/movie_list.html', context)

def movie_detail(request, pk):
    # Fetch ONE movie based on its Primary Key (ID), or return a 404 error
    movie = get_object_or_404(Movie, pk=pk)

    if request.method == 'POST':
        # If the user clicks submit, grab their data
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False) # Pause saving for a second
            review.movie = movie             # Attach the specific movie
            review.user = request.user       # Attach the logged-in user
            review.save()                    # Now save to database!
            return redirect('movie_detail', pk=movie.pk) # Refresh page
    else:
        form = ReviewForm() # Show a blank form
    
    context = {'movie': movie}
    return render(request, 'catalog/movie_detail.html', context)

def toggle_watchlist(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    # Get the user's watchlist, or create one if it doesn't exist yet
    watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    
    if movie in watchlist.movies.all():
        watchlist.movies.remove(movie) # Remove if already there
    else:
        watchlist.movies.add(movie)    # Add if not there
        
    return redirect('movie_detail', pk=pk)

def movie_list(request):
    # Check if there is a search query in the URL (e.g., ?q=Batman)
    query = request.GET.get('q') 
    
    if query:
        # Filter movies where the title contains the query (case-insensitive)
        all_movies = Movie.objects.filter(title__icontains=query)
    else:
        all_movies = Movie.objects.all() 
        
    context = {'movies': all_movies, 'query': query}
    return render(request, 'catalog/movie_list.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Automatically log the user in after signing up
            return redirect('movie_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
