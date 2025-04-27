from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator  # Add this import

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    TYPE_CHOICES = [
        ('movie', 'Movie'),
        ('series', 'TV Series'),
        ('anime', 'Anime'),
        ('documentary', 'Documentary'),
        ('shortfilm', 'Short Film'),
        ('cartoon', 'Cartoon'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    genres = models.ManyToManyField(Genre)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    release_date = models.DateField()
    duration = models.CharField(max_length=50)
    director = models.CharField(max_length=100)
    cast = models.TextField(help_text="Separate names with commas")
    poster = models.ImageField(upload_to='posters/')
    trailer_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)]  # Fixed validators
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)