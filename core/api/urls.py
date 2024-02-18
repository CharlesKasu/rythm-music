from django.urls import path

from core.api import views


urlpatterns = [
    path('default', views.default_song),
    path('home', views.HomeViewAPI.as_view()),
    path('songs', views.SongListAPIView.as_view()),
    path('artists', views.ArtistListAPIView.as_view()),
    path('artists/<slug:slug>', views.ArtistRetrieveAPIView.as_view()),
    path('genres', views.GenreListAPIView.as_view()),
    path('genres/<int:pk>/songs', views.SongsByGenreListAPIView.as_view()),
    path('songs/<int:pk>', views.SongRetrieveAPIView.as_view()),
    path('search/', views.SongSearchAPIView.as_view(), name='api_search'),
    path('songs/next/<str:current_song_id>/', views.next_song, name='next-song'),
    path('songs/prev/<str:current_song_id>/', views.previous_song, name='previous-song'),

]