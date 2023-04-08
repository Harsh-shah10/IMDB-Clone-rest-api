from django.shortcuts import render
from rest_framework.decorators import api_view

# import models
from .models import WatchList, StreamingPlatform, Genre, Review, TicketSale
from django.http import JsonResponse
import json

from rest_framework import status
from rest_framework.response import Response
from django.db.models import F, Count, Sum, Avg

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


    if 'year' in received_json_data:
        year = int(received_json_data['year'])
    else:
        return JsonResponse({'status': 'fail', 'message': "Pass 'year' key", 'status_code': 400})

    if 'genres' in received_json_data:
        genre_ids = received_json_data['genres']
        try:
            genres = Genre.objects.filter(id__in=genre_ids)
        except Genre.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'Invalid genre id(s)', 'status_code': 400})
    else:
        return JsonResponse({'status': 'fail', 'message': "Pass 'genres' key", 'status_code': 400})


    movie_obj = WatchList()
    movie_obj.title = title
    if storyline:
        movie_obj.storyline = storyline
    movie_obj.active = active
    movie_obj.platform_id = Pid
    movie_obj.year = year
    movie_obj.save()
    movie_obj.genres.set(genres)

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

@api_view(['POST'])
def AddStreamingPlatform(request):
    received_json_data = json.loads(request.body)
    if len(received_json_data) == 0:
        return JsonResponse({'status': 'fail', 'message': 'Payload cannot be Empty', 'status_code': 400})

    # Check if all the required keys are present in the received JSON data
    required_keys = ['name', 'about', 'website']
    missing_keys = [key for key in required_keys if key not in received_json_data]
    if missing_keys:
        missing_keys_str = ', '.join(missing_keys)
        return JsonResponse({'status': 'fail', 'message': f'Missing required keys: {missing_keys_str}', 'status_code': 400})

    name = received_json_data['name']
    about = received_json_data['about']
    website = received_json_data['website']
    if name and about and website:
        streaming_platform = StreamingPlatform(
                name=name,
                about=about,
                website=website
            )
        streaming_platform.save()  
        
        response_data = {
            'message': 'Streaming platform added successfully',
            'data': {
                'id': streaming_platform.id,
                'name': streaming_platform.name,
                'about': streaming_platform.about,
                'website': streaming_platform.website
            }
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
    else:
        response_data = {
            'error': 'Incomplete data provided'
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def view_streaming_platforms(request):
    platforms = StreamingPlatform.objects.all()
    platforms_data = [{'Id': platform.id,'name': platform.name, 'about': platform.about, 'website': platform.website} for platform in platforms]
    return JsonResponse({'status': 'success', 'data': platforms_data})


#to get all the movies with their corresponding genre names
@api_view(['GET'])
def genre_list(request):
    # inner join
    results = WatchList.objects.annotate(genre_name=F('genres__name')).values('genre_name', 'id', 'title', 'storyline', 'year').order_by('genre_name')

    genres = {}
    for result in results:
        genre_name = result['genre_name']
        movie = {
            "id": result['id'],
            "title": result['title'],
            "storyline": result['storyline'],
            "year": result['year']
        }
        if genre_name in genres:
            genres[genre_name].append(movie)
        else:
            genres[genre_name] = [movie]
    
    return JsonResponse(genres)


# get the no of ticekts sold
@api_view(['GET'])
def ticket_sales(request):
    #queryset = WatchList.objects.raw("SELECT watch_list.id, watch_list.title AS movie_title,ticket_sales.amount AS amount, COUNT(ticket_sales.id) AS tickets_sold FROM watch_list INNER JOIN ticket_sales ON watch_list.id = ticket_sales.movie_id GROUP BY watch_list.title")
    queryset = WatchList.objects.annotate(
        tickets_sold=Count('ticketsale'),
        total_amount=Sum('ticketsale__amount')
    ).values('title', 'tickets_sold', 'total_amount')
    results = list(queryset)
    return JsonResponse({'results': results})

#display a list of all movies with their average rating, including movies that haven't been rated yet
@api_view(['GET'])
def rating_analysis(request):
    # movie_ratings = WatchList.objects.annotate(avg_rating=Avg('all_review__rating')).values('title', 'avg_rating')
    # results = []
    # for movie in movie_ratings:
    #     result = {
    #         'movie_title': movie['title'],
    #         'avg_rating': movie['avg_rating'] or 'Not rated yet'
    #     }
    #     results.append(result)

    # return JsonResponse({'results': results})

    query = WatchList.objects.raw('''SELECT watch_list.id,
        watch_list.title, 
        AVG(all_review.rating) AS avg_rating, 
        GROUP_CONCAT(all_review.name, ',') AS reviewers 
        FROM 
        watch_list 
        LEFT JOIN all_review ON watch_list.id = all_review.watchlist_id 
        GROUP BY 
        watch_list.id;
        ''')
    
    results = []
    for row in query:
        reviewers = row.reviewers.split(',') if row.reviewers else 0
        result = {
            'movie_title': row.title,
            'avg_rating': row.avg_rating or 'Not rated yet',
            'reviewers': reviewers
        }
        results.append(result)

    return JsonResponse({'results': results})


# api to add reviews to movies
@api_view(['POST'])
def post_movie_reviews(request):
    received_json_data = json.loads(request.body)
    if len(received_json_data) == 0:
        return JsonResponse({'status': 'fail', 'message': 'Payload cannot be Empty', 'status_code': 400})

    # Check if all the required keys are present in the received JSON data
    required_keys = ['watchlist_id','name','rating','description']
    missing_keys = [key for key in required_keys if key not in received_json_data]
    if missing_keys:
        missing_keys_str = ', '.join(missing_keys)
        return JsonResponse({'status': 'fail', 'message': f'Missing required keys: {missing_keys_str}', 'status_code': 400})

    name = received_json_data['name']
    rating = int(received_json_data['rating'])
    description = received_json_data['description']
    watchlist_id = received_json_data['watchlist_id']

    watchlist = WatchList.objects.get(id=watchlist_id)
    review = Review.objects.create(
            name=name,
            rating=rating,
            description=description,
            watchlist=watchlist
        )

    # Save the new review object to the database
    review.save()

    # Create the response data
    response_data = {
        'message': 'Review added successfully',
        'data': {
            'R_id': review.id,
            'name': review.name,
            'rating': review.rating,
            'description': review.description,
            'created': review.created,
            'update': review.update,
            'active': review.active,
            'movie_title': watchlist.title
        }
    }
    return JsonResponse(response_data, status=status.HTTP_201_CREATED)