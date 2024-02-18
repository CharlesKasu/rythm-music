import math
from time import strftime, gmtime
from mutagen.mp3 import MP3
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
import datetime
import os

from accounts.models import User
from utils.song_utils import generate_file_name


class Artist(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    thumbnail = models.ImageField(upload_to="artists", default="artists/default.png")
    bio = models.TextField(verbose_name='Artist Bio', null=True, blank=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Artist, self).save(*args, **kwargs)


class Genre(models.Model):
    name = models.CharField(max_length=50)
    thumbnail = models.ImageField(upload_to="genres", default="genres/default.png")

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey('Song', on_delete=models.CASCADE)


def song_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'songs/{0}/{1}'.format(strftime('%Y/%m/%d'), generate_file_name() + '.' + filename.split('.')[-1])


class Song(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    audio_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200, verbose_name="Song name")
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="thumbnails", blank=False)
    song = models.FileField(upload_to=song_directory_path, max_length=500)
    # audio_location = models.CharField(max_length=255)
    genre = models.ForeignKey(Genre, on_delete=models.DO_NOTHING)
    artists = models.ManyToManyField(Artist, related_name='songs')
    size = models.IntegerField(default=0)
    playtime = models.CharField(default='00:00', editable=False, verbose_name="Playtime", max_length=5)
    explicit = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(verbose_name='Created At', default=timezone.now)

    def __str__(self):
        return self.title

    @property
    def duration(self):
        # Konwertuje playtime na format MM:SS
        minutes = int(self.playtime // 60)
        seconds = int(self.playtime % 60)
        return "{:02d}:{:02d}".format(minutes, seconds)


    def save(self, *args, **kwargs):
        # Automatyczne ustawianie długości utworu podczas zapisywania
        if self.song and not self.pk:  # Sprawdza, czy piosenka jest nowa
            audio = MP3(self.song.file)  # Użyj mutagen do analizy pliku
            self.playtime = audio.info.length  # Odczytaj długość utworu

        super().save(*args, **kwargs)


class UserArtist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_artists')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='fans')

    class Meta:
        unique_together = ('user', 'artist')  # Zapobiega duplikatom

    def __str__(self):
        return f"{self.user.email} - {self.artist.name}"


class UserGenre(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_genres')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='listeners')

    class Meta:
        unique_together = ('user', 'genre')  # Zapobiega duplikatom

    def __str__(self):
        return f"{self.user.email} - {self.genre.name}"


class PlaybackHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playback_history')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='played_by')
    played_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-played_at']  # Sortuje historię odtworzeń od najnowszej do najstarszej

    def __str__(self):
        return f"{self.user.email} played {self.song.audio_id} on {self.played_at.strftime('%Y-%m-%d %H:%M:%S')}"
