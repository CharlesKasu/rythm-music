from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import Song
from .serializers import SongSerializer, ArtistSerializer, GenreSerializer, ArtistSongsSerializer


@api_view(['GET'])
def default_song(request):
    song = Song.objects.filter(type='free')[1]
    serializer = SongSerializer(song, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


class HomeViewAPI(APIView):
    """
        Get various type of data for home
    """

    def get(self, request, format=None):
        song_queryset = Song.objects.all()
        serializer = SongSerializer(data=song_queryset, many=True, context={'request': request})
        serializer.is_valid()

        return Response({'songs': serializer.data})


class SongListAPIView(ListAPIView):
    serializer_class = SongSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()


class SongsByGenreListAPIView(ListAPIView):
    """
        List of songs by genre
    """
    serializer_class = SongSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        try:
            genre_id = self.kwargs
            return self.model.objects.filter(genre_id=genre_id).order_by('-created_at')
        except:
            return self.model.objects.all().order_by('-created_at')


class ArtistListAPIView(ListAPIView):
    """
        List of artists
    """
    serializer_class = ArtistSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()


class ArtistRetrieveAPIView(RetrieveAPIView):
    """
        Artist details view with songs
    """
    serializer_class = ArtistSongsSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


class GenreListAPIView(ListAPIView):
    """
        List of genres
    """
    serializer_class = GenreSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()


class SongRetrieveAPIView(RetrieveAPIView):
   """
       Get song details and recommended songs (based on genre)
   """
#    serializer_class = SongSerializer
#    model = serializer_class.Meta.model
#    queryset = model.objects.all()



#    def get(self, request, pk):
#        song = self.get_object()
#        serializer = SongSerializer(song, context={'request': request})

#        # Simple Recommendation Logic (Same Genre)
#        recommended_songs = Song.objects.filter(genre=song.genre).exclude(pk=song.pk)[:5] 
#        recommended_serializer = SongSerializer(recommended_songs, many=True, context={'request': request})
#        return Response({
#            'song': serializer.data, 
#            'recommended_songs': recommended_serializer.data
#        })  

class SongSearchAPIView(APIView):
    def get(self, request):
        query = request.query_params.get('query', '')
        print(query)
        if query:
            songs = Song.objects.filter(title__icontains=query)
            print(songs)
            # Dodajemy kontekst z 'request' podczas tworzenia serializer'a
            serializer = SongSerializer(songs, many=True, context={'request': request})
            print(serializer.data)
            return Response(serializer.data)
        return Response([])


@api_view(('GET',))
def next_song(request, current_song_id):
    """
    Retrieve the next song based on the current song's audio ID.
    """
    # First, find the current song by its audio_id to get its id
    try:
        current_song = Song.objects.get(audio_id=current_song_id)
    except Song.DoesNotExist:
        return Response({"message": "Current song not found."}, status=status.HTTP_404_NOT_FOUND)

    next_songs = Song.objects.filter(id__gt=current_song.id).order_by('id')

    # Now, filter songs with an id greater than the current song's id
    if next_songs.exists():
        next_song = next_songs.first()
        print(f"Next song: {next_song.title}, ID: {next_song.id}, Audio ID: {next_song.audio_id}")
        serializer = SongSerializer(next_song, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        # If there is no next song, get the first song from the database
        first_song = Song.objects.all().order_by('id').first()
        if first_song:
            print(f"First song in DB: {first_song.title}, ID: {first_song.id}, Audio ID: {first_song.audio_id}")
            serializer = SongSerializer(first_song, context={'request': request})

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No songs available."}, status=status.HTTP_404_NOT_FOUND)


@api_view(('GET',))
def previous_song(request, current_song_id):
    """
    Retrieve the next song based on the current song's audio ID.
    """
    # First, find the current song by its audio_id to get its id
    try:
        current_song = Song.objects.get(audio_id=current_song_id)
    except Song.DoesNotExist:
        return Response({"message": "Current song not found."}, status=status.HTTP_404_NOT_FOUND)

    next_songs = Song.objects.filter(id__lt=current_song.id).order_by('id')

    # Now, filter songs with an id greater than the current song's id
    if next_songs.exists():
        next_song = next_songs.last()
        print(f"Next song: {next_song.title}, ID: {next_song.id}, Audio ID: {next_song.audio_id}")
        serializer = SongSerializer(next_song, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        # If there is no next song, get the first song from the database
        first_song = Song.objects.all().order_by('id').first()
        if first_song:
            print(f"First song in DB: {first_song.title}, ID: {first_song.id}, Audio ID: {first_song.audio_id}")
            serializer = SongSerializer(first_song, context={'request': request})

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No songs available."}, status=status.HTTP_404_NOT_FOUND)