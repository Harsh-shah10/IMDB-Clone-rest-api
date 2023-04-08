from django.urls import path

from django.urls import include
from watchlist_app.views import movie_list, movie_details,add_movie,stream_list,stream_details,AddStreamingPlatform,view_streaming_platforms,genre_list

urlpatterns = [
    path('list/', movie_list, name='movie_list'),
    path('<int:pk>', movie_details, name='movie_details'),
    path('add/', add_movie, name='add_movie'),
    path('genre_list/', genre_list, name='genre_list'),

    path('stream/', stream_list, name='stream_list'),
    path('stream/list', view_streaming_platforms, name='view_streaming_platform_list'),
    path('stream/add_stream_platform', AddStreamingPlatform, name='add_stream_platform'),
    path('stream/<int:pk>', stream_details, name='stream_details'),
]
