from django.contrib import admin
from .models import Genre, Song, Artist, PlaybackHistory
from utils.song_utils import generate_key
from mutagen.mp3 import MP3

admin.site.register(Genre)


@admin.register(Song)
class SongModelAdmin(admin.ModelAdmin):
    # Dodaj playtime do listy pól tylko do odczytu
    readonly_fields = ('playtime',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['audio_id'].initial = generate_key(15, 20)
        return form

    def save_model(self, request, obj, form, change):
        if obj.song and not change:  # Sprawdza czy to nowe dodanie pliku
            try:
                audio = MP3(obj.song)  # Tutaj musisz się upewnić, że ścieżka do pliku jest dostępna
                obj.playtime = audio.info.length
            except Exception as e:
                # Logowanie błędów lub obsługa wyjątku
                pass
        super().save_model(request, obj, form, change)


@admin.register(Artist)
class ArtistModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class PlaybackHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'song', 'played_at')  # Customize the columns displayed
    list_filter = ('user', 'song')  # Add filters to the sidebar
    search_fields = ('user__email', 'song__title')  # Enable search

admin.site.register(PlaybackHistory, PlaybackHistoryAdmin)