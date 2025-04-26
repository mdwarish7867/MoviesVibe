from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.decorators.http import require_POST

urlpatterns = [
    # Home and Movies
    path('', views.home, name='home'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('add-movie/', views.add_movie, name='add_movie'),
    path('genre/<int:genre_id>/', views.genre_movies, name='genre_movies'),
    path('type/<str:type_name>/', views.type_movies, name='type_movies'),
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='home/login.html'), name='login'),
    # home/urls.py
    path('logout/', require_POST(auth_views.LogoutView.as_view(next_page='home')), name='logout'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('recent/', views.recent_movies, name='recent_movies'),
]