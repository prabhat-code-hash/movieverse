from django.urls import path  # type: ignore[import]
from . import views

urlpatterns = [
    # Homepage URL routes to movie_list view
    path('', views.movie_list, name='movie_list'),
    
    # Dynamic URL: <int:pk> captures the ID from the URL (e.g., /movie/1/)
    path('movie/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('movie/<int:pk>/watchlist/', views.toggle_watchlist, name='toggle_watchlist'),
    path('register/', views.register, name='register'),
    path('profile/', views.user_profile, name='user_profile'),  
]