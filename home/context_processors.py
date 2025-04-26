from .models import Genre, Movie  # Adjust according to your structure

def genre_and_types(request):
    genres = Genre.objects.all()
    movie_types = Movie.TYPE_CHOICES  # dynamically fetch from model
    return {
        'genres': genres,
        'movie_types': movie_types,
    }
