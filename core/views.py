import numpy as np
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, ListView
from django.views.generic.detail import DetailView
from sklearn.metrics.pairwise import cosine_similarity
from tinytag import TinyTag

from utils.song_utils import generate_key
from .forms import *
from .models import Song, PlaybackHistory


def home(request):
    context = {
        'artists': Artist.objects.all(),
        'genres': Genre.objects.all()[:6],
        'latest_songs': Song.objects.all()[:6]
    }
    return render(request, "home.html", context)


class SongUploadView(CreateView):
    form_class = SongUploadForm
    template_name = "songs/create.html"

    @method_decorator(login_required(login_url=reverse_lazy('core:home')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SongUploadView, self).get_context_data(**kwargs)
        context['artists'] = Artist.objects.all()
        context['genres'] = Genre.objects.all()
        return context

    def get_form_kwargs(self):
        kwargs = super(SongUploadView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=200)

    def form_valid(self, form):
        song = TinyTag.get(self.request.FILES['song'].file.name)
        form.instance.audio_id = generate_key(15, 15)
        form.instance.user = self.request.user
        form.instance.playtime = song.duration
        form.instance.size = song.filesize
        artists = []
        for a in self.request.POST.getlist('artists[]'):
            try:
                artists.append(int(a))
            except:
                artist = Artist.objects.create(name=a)
                artists.append(artist)
        form.save()
        form.instance.artists.set(artists)
        form.save()
        data = {
            'status': True,
            'message': "Successfully submitted form data.",
            'redirect': reverse_lazy('core:upload-details', kwargs={'audio_id': form.instance.audio_id})
        }
        return JsonResponse(data)


class SongDetailsView(DetailView):
    model = Song
    template_name = 'songs/show.html'
    context_object_name = 'song'
    slug_field = 'audio_id'
    slug_url_kwarg = 'audio_id'

    def get_recommendations(self, user_id, num_recommendations=5, current_song_id=None):
        if not current_song_id:
            return Song.objects.none()

        current_song = Song.objects.filter(id=current_song_id).first()
        if not current_song:
            return Song.objects.none()

        # Step 1: Content-based filtering part - prioritize current song's genre
        genre_songs = Song.objects.filter(genre=current_song.genre).exclude(id=current_song_id)

        # Step 2: Collaborative filtering part
        # Get all user playback histories excluding the current song
        all_playbacks = PlaybackHistory.objects.exclude(song_id=current_song_id).values('user_id', 'song_id')
        all_users = list(set([playback['user_id'] for playback in all_playbacks]))
        all_songs = list(set([playback['song_id'] for playback in all_playbacks]))

        # Create a user-song matrix
        user_song_matrix = np.zeros((len(all_users), len(all_songs)))

        for playback in all_playbacks:
            user_index = all_users.index(playback['user_id'])
            song_index = all_songs.index(playback['song_id'])
            user_song_matrix[user_index, song_index] = 1

        # Calculate similarity between users
        user_similarity = cosine_similarity(user_song_matrix)

        # Find the index of the current user
        if user_id in all_users:
            current_user_index = all_users.index(user_id)
            similar_users = user_similarity[current_user_index]

            # Rank users by similarity
            similar_user_indices = np.argsort(similar_users)[::-1][1:]  # exclude the first one (itself)

            # Aggregate song preferences from similar users
            recommended_song_ids = set()
            for idx in similar_user_indices:
                liked_songs = np.where(user_song_matrix[idx] == 1)[0]
                for song_id in liked_songs:
                    recommended_song_ids.add(all_songs[song_id])
                    if len(recommended_song_ids) >= num_recommendations:
                        break
                if len(recommended_song_ids) >= num_recommendations:
                    break

            # Filter recommended songs by the current song's genre
            recommended_songs = genre_songs.filter(id__in=recommended_song_ids)
        else:
            # Fallback if the current user has no history
            recommended_songs = genre_songs.order_by('?')[:num_recommendations]

        return recommended_songs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        song = get_object_or_404(Song, audio_id=self.kwargs['audio_id'])

        # Get the current user from the request
        current_user = self.request.user

        # Check if the user is authenticated and get recommendations
        if current_user.is_authenticated:
            recommended_songs = self.get_recommendations(current_user.id, num_recommendations=4,
                                                         current_song_id=song.id)
            # If the user hasn't listened to any songs, fallback to genre-based recommendations
            if not recommended_songs.exists():
                recommended_songs = Song.objects.filter(genre=song.genre).exclude(pk=song.pk)[:4]
        else:
            # Fallback to genre-based recommendations for anonymous users
            recommended_songs = Song.objects.filter(genre=song.genre).exclude(pk=song.pk)[:4]

        context['recommended_songs'] = recommended_songs

        return context


class GenreListView(ListView):
    model = Genre
    template_name = 'genres/index.html'
    context_object_name = 'genres'


class SongsByGenreListView(DetailView):
    model = Genre
    template_name = 'genres/songs-by-genre.html'
    context_object_name = 'genre'

    def get_context_data(self, **kwargs):
        context = super(SongsByGenreListView, self).get_context_data(**kwargs)
        context['songs'] = self.get_object().song_set.all
        return context


class ArtistListView(ListView):
    model = Artist
    template_name = 'artists/index.html'
    context_object_name = 'artists'


class ArtistDetailView(DetailView):
    model = Artist
    template_name = 'artists/show.html'
    context_object_name = 'artist'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super(ArtistDetailView, self).get_context_data(**kwargs)
        context['songs'] = self.get_object().songs.all()
        return context


class FavoriteCreateView(CreateView):
    form_class = FavoriteForm
    http_method_names = ['post']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(FavoriteCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            data = {
                'status': True,
                'message': "Please login first",
                'redirect': None
            }
            return JsonResponse(data=data)
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def favoriteunfavorite(request):
    if request.method == "POST":
        if request.POST.get('decision') == 'make':
            song = Song.objects.get(id=request.POST.get('song_id'))
            if not Favorite.objects.filter(user=request.user, song=song).exists():
                Favorite.objects.create(user=request.user, song=song)
                data = {
                    'status': True,
                    'message': "Song marked as favorite",
                    'redirect': None
                }
                return JsonResponse(data)
            else:
                data = {
                    'status': True,
                    'message': "Already favorite",
                    'redirect': None
                }

                return JsonResponse(data)
        else:
            song = Song.objects.get(id=request.POST.get('song_id'))
            Favorite.objects.filter(user=request.user, song=song).delete()
            data = {
                'status': True,
                'message': "Song unfavorited",
                'redirect': None
            }
            return JsonResponse(data)
    else:
        data = {
            'status': False,
            'message': "Method not allowed",
            'redirect': None
        }

        return JsonResponse(data)


class UnFavoriteView(DeleteView):
    model = Favorite

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        data = {
            'status': True,
            'message': "Song unfavorited.",
            'redirect': None
        }

        return JsonResponse(data)


@login_required
@require_POST
def record_playback(request):
    song_id = request.POST.get('song_id')
    user = request.user

    if song_id:
        try:
            song = Song.objects.get(id=song_id)
            PlaybackHistory.objects.create(user=user, song=song)
            return JsonResponse({'status': 'success', 'message': 'Playback recorded successfully'})
        except Song.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Song does not exist'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

# from django.db.models import Count, Q
# from django.db.models.functions import Coalesce

# def get_ml_recommendations(user, num_recommendations=5):
# # Get all the songs played by the user
# user_playback_history = PlaybackHistory.objects.filter(user=user).values_list('song', flat=True)

# # Find other users who have played the same songs
# similar_users = PlaybackHistory.objects.filter(
#     song__in=user_playback_history
# ).exclude(
#     user=user
# ).values_list('user', flat=True).distinct()

# # Find songs played by those users
# recommended_songs = PlaybackHistory.objects.filter(
#     user__in=similar_users
# ).values('song').annotate(
#     play_count=Coalesce(Count('song'), 0)
# ).order_by('-play_count')[:num_recommendations]

# # Get the actual Song objects for the recommended song IDs
# recommended_song_ids = [rec['song'] for rec in recommended_songs]
# return Song.objects.filter(id__in=recommended_song_ids)
