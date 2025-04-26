from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from home.models import Movie, Genre
from .forms import MovieForm

def get_base_context():
    return {
        'genres': Genre.objects.all(),
        'movie_types': Movie.TYPE_CHOICES
    }


def home(request):
    movies = Movie.objects.all().order_by('-release_date')
    query = request.GET.get('q')
    
    if query:
        # Clean the query and search across multiple fields
        clean_query = query.strip()
        movies = movies.filter(
            Q(title__icontains=clean_query) |
            Q(description__icontains=clean_query) |
            Q(cast__icontains=clean_query) |
            Q(director__icontains=clean_query) |
            Q(release_date__year__icontains=clean_query)
        ).distinct()

        context = {
            'movies': movies,
            'search_query': query
        }
    else:
        context = {
            'top_rated_movies': Movie.objects.filter(type='movie')
                            .annotate(avg_rating=Avg('review__rating'))
                            .order_by('-avg_rating')[:8],
            'top_rated_series': Movie.objects.filter(type='series')
                            .annotate(avg_rating=Avg('review__rating'))
                            .order_by('-avg_rating')[:8],
            'recent_movies': Movie.objects.all()
                            .order_by('-created_at')[:8],
            'highlighted_genres': Genre.objects.filter(
                name__in=['Action', 'Adventure', 'Thriller']
            ).prefetch_related('movie_set')
        }
    
    return render(request, 'home/home_page.html', context)

# Add this new view function
def recent_movies(request):
    movies = Movie.objects.all().order_by('-created_at')
    return render(request, 'home/movies_list.html', {
        'movies': movies,
        'title': 'Recently Added Content'
    })

# Update type_movies view
def type_movies(request, type_name):
    movies = Movie.objects.filter(type=type_name).annotate(  # Add annotation
        avg_rating=Avg('review__rating')
    )
    
    # Existing search functionality
    query = request.GET.get('q')
    if query:
        movies = movies.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(cast__icontains=query) |
            Q(director__icontains=query)
        )

    context = get_base_context()
    context.update({
        'title': f"{dict(Movie.TYPE_CHOICES).get(type_name)}",
        'movies': movies,
        'type_name': type_name
    })
    return render(request, 'home/movies_list.html', context)

# Create your views here.


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Movie, Genre, Review, ContactMessage
from .forms import MovieForm, ReviewForm, ContactForm
from django.db.models import Avg

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    reviews = Review.objects.filter(movie=movie)
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return redirect('movie_detail', movie_id=movie_id)
    else:
        form = ReviewForm()
    
    context = {
        'movie': movie,
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'home/movie_detail.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def add_movie(request):
    if request.method == 'POST':
        # Print POST data for debugging
        print("POST data:", request.POST)
        print("FILES data:", request.FILES)
        
        # Check if genres were selected
        genres_selected = request.POST.getlist('genres')
        print("Selected genres:", genres_selected)
        
        if not genres_selected:
            messages.error(request, 'Please select at least one genre.')
        
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save()
            messages.success(request, f'"{movie.title}" added successfully!')
            return redirect('movie_detail', movie_id=movie.id)
        else:
            # Print detailed form errors for debugging
            for field, errors in form.errors.items():
                print(f"Field: {field}, Errors: {errors}")
                # Print the value that caused the error
                if field in request.POST:
                    print(f"Value for {field}: {request.POST.get(field)}")
                elif field in request.FILES:
                    print(f"File for {field}: {request.FILES.get(field)}")
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MovieForm()
    
    return render(request, 'admin/add_movie.html', {
        'form': form,
        'genres': Genre.objects.all()  # Pass genres to template
    })


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Automatically add logged-in user's info if available
            contact_message = form.save(commit=False)
            if request.user.is_authenticated:
                contact_message.name = f"{request.user.username} (Registered User)"
                contact_message.email = request.user.email
            contact_message.save()
            
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        initial = {}
        if request.user.is_authenticated:
            initial = {'email': request.user.email}
        form = ContactForm(initial=initial)
    
    return render(request, 'home/contact.html', {'form': form})

def about(request):
    return render(request, 'home/about.html')


def genre_movies(request, genre_id):
    genre = get_object_or_404(Genre, pk=genre_id)
    movies = Movie.objects.filter(genres=genre)
    
    # Add search functionality
    query = request.GET.get('q')
    if query:
        movies = movies.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(cast__icontains=query) |
            Q(director__icontains=query)
        )

    context = get_base_context()
    context.update({
        'title': f"{genre.name} Movies",
        'movies': movies,
        'genre': genre  # Add this line
    })
    return render(request, 'home/movies_list.html', context)

def type_movies(request, type_name):
    movies = Movie.objects.filter(type=type_name)
    # Add search functionality
    query = request.GET.get('q')
    if query:
        movies = movies.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(cast__icontains=query) |
            Q(director__icontains=query)
        )

    context = get_base_context()
    context.update({
        'title': f"{dict(Movie.TYPE_CHOICES).get(type_name)}",
        'movies': movies,
        'type_name': type_name  # Add this line
    })
    return render(request, 'home/movies_list.html', context)

# register
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
        else:
            # Show form errors
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = UserCreationForm()
    
    return render(request, 'home/register.html', {'form': form})