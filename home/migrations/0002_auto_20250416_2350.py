from django.db import migrations

def add_genres(apps, schema_editor):
    Genre = apps.get_model('home', 'Genre')
    genres = [
        "Action", "Adventure", "Animation", "Biography", "Comedy", "Crime",
        "Documentary", "Drama", "Fantasy", "History", "Horror", "Mystery",
        "Romance", "Sci-Fi", "Thriller", "War", "Western", "Musical",
        "Family", "Sport", "Superhero", "Noir", "Psychological", "Disaster",
        "Zombie", "Alien", "Time Travel", "Vampire", "Heist", "Cyberpunk"
    ]
    for genre in genres:
        Genre.objects.get_or_create(name=genre)

class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),  # replace with your real previous migration
    ]

    operations = [
        migrations.RunPython(add_genres),
    ]
