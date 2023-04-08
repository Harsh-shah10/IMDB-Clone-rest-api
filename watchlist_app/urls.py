from django.urls import path

from django.urls import include
from watchlist_app.views import movie_list, movie_details,add_movie,stream_list,stream_details

urlpatterns = [
    path('list/', movie_list, name='movie_list'),
    path('<int:pk>', movie_details, name='movie_details'),
    path('add/', add_movie, name='add_movie'),

    path('stream/', stream_list, name='stream_list'),
    path('stream/<int:pk>', stream_details, name='stream_details'),
]
