from django.contrib import admin
from .models import Movie, Genre, Review, ContactMessage

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'release_date', 'director')
    list_filter = ('type', 'genres')
    search_fields = ('title', 'director', 'cast')
    filter_horizontal = ('genres',)
    date_hierarchy = 'release_date'

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'timestamp', 'short_message')
    search_fields = ('name', 'email', 'message')
    list_filter = ('timestamp',)
    readonly_fields = ('timestamp',)
    
    def short_message(self, obj):
        return f"{obj.message[:50]}..." if len(obj.message) > 50 else obj.message
    short_message.short_description = 'Message'

admin.site.register(Genre)
admin.site.register(Review)

# custom_admin
admin.site.site_header = "🎬 MoviesVibe Admin Panel"
admin.site.site_title = "MoviesVibe Admin"
admin.site.index_title = "Welcome to MoviesVibe Admin Dashboard"