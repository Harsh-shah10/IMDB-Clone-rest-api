from django.shortcuts import render
from rest_framework.decorators import api_view

# import models
from .models import WatchList, StreamingPlatform
from django.http import JsonResponse
import json

from rest_framework import status
from rest_framework.response import Response


# viewing movies list
@api_view(['GET'])
def movie_list(request):
    Movies = WatchList.objects.all()
    data = {'status': 'success', 'movie list': list(
        Movies.values()), 'status_code': 200}
    return JsonResponse(data)


# viewing movies details
# @api_view() # by default it's been set to GET REQUEST
@api_view(['GET', 'DELETE', 'PUT'])
def movie_details(request, pk):
    if request.method == 'GET':
        try:
            movie = WatchList.objects.get(id=int(pk))
        except WatchList.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'No movie exists with the following Movie-ID', 'status_code': 400})

        data = {'status': 'success', 'id': movie.id, 'title': movie.title,
                'storyline': movie.storyline, 'active': movie.active, 'Platform': movie.platform.name, 'status_code': 200}
        return JsonResponse(data)

    if request.method == 'DELETE':
        try:
            movie = WatchList.objects.get(id=int(pk))
        except WatchList.DoesNotExist:
            data = {'status': 'fail',
                    'message': 'No movie exists with the following Movie-ID', 'status_code': 404}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        data = {'status': 'success', 'id': movie.id, 'title': movie.title,
                'message': 'Movie Entry has been deleted successfully', 'status_code': 200}
        movie.delete()
        return JsonResponse(data)

    if request.method == 'PUT':
        received_json_data = json.loads(request.body)
        if len(received_json_data) == 0:
            return JsonResponse({'status': 'fail', 'message': 'Payload cannot be Empty', 'status_code': 400})

        if 'title' in received_json_data:
            title = received_json_data['title']
        else:
            title = None
        if 'storyline' in received_json_data:
            storyline = received_json_data['storyline']
        else:
            storyline = None
        if 'active' in received_json_data:
            active = received_json_data['active']
            if active not in ['Y', 'N']:
                return JsonResponse({'status': 'fail', 'message': "Pass active as 'Y' or 'N' ", 'status_code': 400})
            else:
                if active == 'Y':
                    active = True
                if active == 'N':
                    active = False
        else:
            active = None

        try:
            movie = WatchList.objects.get(id=int(pk))
        except WatchList.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'No movie exists with the following Movie-ID', 'status_code': 400})

        if title:
            movie.title = title
        if storyline:
            movie.storyline = storyline
        if active:
            movie.active = active
        movie.save()
        data = {'status': 'success', 'Movie ID': movie.id, 'title': movie.title,
                'storyline': movie.storyline, 'active': movie.active, 'message': 'Movie updated sucessfully', 'status_code': 200}
        return JsonResponse(data)


# adding new movies
@api_view(['POST'])
def add_movie(request):
    received_json_data = json.loads(request.body)

    if len(received_json_data) == 0:
        return JsonResponse({'status': 'fail', 'message': 'Payload cannot be Empty', 'status_code': 400})

    # Internal fucn can be used to minimize the code
    if 'title' in received_json_data:
        title = received_json_data['title']
    else:
        return JsonResponse({'status': 'fail', 'message': "Pass 'title' key", 'status_code': 400})

    if 'storyline' in received_json_data:
        storyline = received_json_data['storyline']
    else:
        storyline = None

    if 'active' in received_json_data:
        active = received_json_data['active']
    else:
        return JsonResponse({'status': 'fail', 'message': "Pass 'active' key", 'status_code': 400})

    if active not in ['Y', 'N']:
        return JsonResponse({'status': 'fail', 'message': "Pass active as 'Y' or 'N' ", 'status_code': 400})
    else:
        if active == 'Y':
            active = True
        if active == 'N':
            active = False

    if 'Pid' in received_json_data:
        Pid = received_json_data['Pid']
    else:
        return JsonResponse({'status': 'fail', 'message': "Pass 'Pid' key", 'status_code': 400})

    movie_obj = WatchList()
    movie_obj.title = title
    if storyline:
        movie_obj.storyline = storyline
    movie_obj.active = active
    movie_obj.platform_id = Pid
    movie_obj.save()

    data = {'status': 'success',
            'message': 'Movie Added successfully', 'status_code': 200}
    return Response(data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def stream_list(request):
    # getting all the platforms and the movies associated to those platforms
    Platforms = StreamingPlatform.objects.all().values('id')
    if Platforms:
        queryset = StreamingPlatform.objects.raw("SELECT streaming_platform.id, streaming_platform.name, Watch_List.title FROM streaming_platform  JOIN Watch_List ON streaming_platform.id = Watch_List.platform_id")
        print(str(queryset))
        # Using a for loop
        data = [{'platform_name': row.name, 'movie_name': row.title} for row in queryset]

        # create an empty dictionary to store the result
        result = {}
        # iterate over the raw data and append the movies to the corresponding platform
        for row in data:
            platform_name = row['platform_name']
            movie_name = row['movie_name']
            if platform_name in result:
                result[platform_name].append(movie_name)
            else:
                result[platform_name] = [movie_name]

        # convert the result to the desired format (list of dictionaries)
        output = [{'platform_name': k, 'movie_name': v} for k, v in result.items()]
        data = {'status': 'success', 'Stream list': output, 'status_code': 200} 
        return JsonResponse(data, status=status.HTTP_200_OK)
    else:
        data = {'status': 'fail',
                'message': "No Steaming platform's found", 'status_code': 404}
        return Response(data, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'DELETE', 'PUT'])
def stream_details(request, pk):
    if request.method == 'GET':
        try:
            movie = WatchList.objects.get(id=int(pk))
        except WatchList.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'No movie exists with the following Movie-ID', 'status_code': 400})

        data = {'status': 'success', 'id': movie.id, 'title': movie.title,
                'storyline': movie.storyline, 'active': movie.active, 'Platform': movie.platform.name, 'status_code': 200}
        return JsonResponse(data)

    if request.method == 'DELETE':
        try:
            movie = WatchList.objects.get(id=int(pk))
        except WatchList.DoesNotExist:
            data = {'status': 'fail',
                    'message': 'No movie exists with the following Movie-ID', 'status_code': 404}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        data = {'status': 'success', 'id': movie.id, 'title': movie.title,
                'message': 'Movie Entry has been deleted successfully', 'status_code': 200}
        movie.delete()
        return JsonResponse(data)

# #to get all the movies with their corresponding genre names
# @api_view(['GET'])
# def genre_details(request):
#     # inner join
#     queryset = StreamingPlatform.objects.raw("SELECT movie.title, movie.description, movie.year, movie.rating, genre.genre_name FROM movie INNER JOIN genre ON movie.genre_id = genre.id")
#     print(str(queryset))
    
    
# # get the no of ticekts sold
# @api_view(['GET'])
# def box_office_collection(request):
#     queryset = StreamingPlatform.objects.raw("SELECT watchlist.title AS movie_name, streaming_platform.name AS platform_name, COUNT(ticket.id) AS tickets_sold FROM  watchlist LEFT JOIN streaming_platform ON watchlist.platform_id = streaming_platform.id LEFT JOIN ticket ON watchlist.id = ticket.watchlist_id GROUP BY watchlist.id, streaming_platform.id ORDER BY watchlist.title")
#     print(str(queryset))
    
# #display a list of all movies with their average rating, including movies that haven't been rated yet, using a right join
# def rating_analysis(request):
#     queryset = StreamingPlatform.objects.raw("SELECT movies.title, AVG(ratings.rating) AS average_rating FROM movies RIGHT JOIN ratings ON movies.id = ratings.movie_id GROUP BY movies.title")
#     print(str(queryset))