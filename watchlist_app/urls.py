from django.urls import path

from django.urls import include
from watchlist_app.views import movie_list, movie_details,add_movie,stream_list,stream_details,AddStreamingPlatform,view_streaming_platforms,genre_list,ticket_sales,rating_analysis, post_movie_reviews

urlpatterns = [
    path('list/', movie_list, name='movie_list'),
    path('<int:pk>', movie_details, name='movie_details'),
    path('add/', add_movie, name='add_movie'),
    path('genre_list/', genre_list, name='genre_list'),
    path('rating_analysis/', rating_analysis, name='rating_analysis'),
    
    path('stream/', stream_list, name='stream_list'),
    path('stream/list', view_streaming_platforms, name='view_streaming_platform_list'),
    path('stream/add_stream_platform', AddStreamingPlatform, name='add_stream_platform'),
    path('stream/<int:pk>', stream_details, name='stream_details'),
    path('ticket_sales/', ticket_sales, name='ticket_sales'),
    path('post_movie_reviews/', post_movie_reviews, name='post_movie_reviews')
    
]
