# Generated by Django 5.2 on 2025-04-27 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20250416_2350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='type',
            field=models.CharField(choices=[('movie', 'Movie'), ('series', 'TV Series'), ('anime', 'Anime'), ('documentary', 'Documentary'), ('shortfilm', 'Short Film'), ('cartoon', 'Cartoon')], max_length=20),
        ),
    ]
