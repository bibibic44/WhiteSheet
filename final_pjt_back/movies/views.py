from django.shortcuts import get_list_or_404, get_object_or_404
from requests.api import get
from rest_framework import serializers, status
from rest_framework import response
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import MovieListSerializer, ReviewListSerializer, ReviewDetailSerializer, \
    CommentSerializer, CommentDetailSerializer
from .models import Movie, Review, Comment, Recommendation
import json, requests



@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def movie_list(request):
    if request.method == 'POST':
        host = 'https://api.themoviedb.org/3'
        API_KEY = 'api_key=fb9be8dd33947a81a9eb5a9e7fca2f5e'
        # total_pages = requests.get(
        #     f'{host}/movie/popular?{API_KEY}').json().get('total_pages')
        # for page in range(1, int(total_pages) + 1):
        temp = Movie.objects.count()
        if temp == 0:
            # 데이터 1000개 미만으로 받아오기
            for page in range(1, 51):
                results = requests.get(
                    f'{host}/movie/popular?{API_KEY}&language=ko-KR&page={page}').json().get('results')
                for result in results:
                    movie = Movie(title=result.get('title'), overview=result.get(
                        'overview'), release_date=result.get('release_date'), poster_path=result.get('poster_path'),
                        genre=result.get('genre_ids'), vote_average=result.get('vote_average'), movie_key=result.get('id'))
                    # 제목이 중복되는 영화는 DB에 저장하지 않는다.
                    if not Movie.objects.filter(title=movie.title):
                        movie.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def movie_search(request):
    if request.method == 'POST':
        q = request.data.get('movie')
        movies = Movie.objects.filter(title__contains=q)
        if movies:
            serializer = MovieListSerializer(movies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def reviews(request):
    if request.method == 'GET':
        # reviews = get_list_or_404(Review)
        reviews = Review.objects.order_by('-pk')
        if reviews:
            serializer = ReviewListSerializer(reviews, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'POST':
        print(request.user)
        # print(request.data.get('movie')['title'])
        # print(Movie.objects.all().count())
        # movie = Movie.objects.filter(title=request.data.get('movie')['title']).values('pk')
        movie = Movie.objects.filter(
            title=request.data.get('movie')).values('pk')
        print(movie)
        # print(movie[0].get('pk'))
        if movie:
            updated_data = request.data
            updated_data['movie_title'] = request.data.get('movie')
            updated_data['movie'] = movie[0].get('pk')
            # print(updated_data)
            serializer = ReviewDetailSerializer(data=updated_data)
            if serializer.is_valid(raise_exception=True):
                # serializer
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT', 'DELETE', 'GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def review_update_delete(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    print(request.user)

    if not request.user.reviews.filter(pk=review_pk).exists():
        return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        if not request.user.reviews.filter(pk=review_pk).exists():
            return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = ReviewDetailSerializer(review, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def review_detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if review:
        serializer = ReviewDetailSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def comments(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'GET':
        comments = review.comment_set.all()
        if comments:
            serializer = CommentDetailSerializer(comments, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid(raise_exception=True):
            print(serializer)
            serializer.save(review=review, user=request.user, username=request.user )
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE', 'GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def comment_delete(request, review_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    print(request.user)

    if request.method == 'GET':
        if not request.user.comments.filter(pk=comment_pk).exists():
            return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_200_OK)

    if not request.user.comments.filter(pk=comment_pk).exists():
        return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'DELETE':
        comment.delete()
        return Response({'id': review_pk})


@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def recommended_movies(request):
    if request.method == 'POST':
        genres = request.data.get('genres')
        # print(request.data)
        if genres:
            recommendation = Recommendation(
                interested_genre=genres, user=request.user)
            recommendation.save()

        # 추천 알고리즘
        your_genres = Recommendation.objects.filter(user=request.user)
        # 유저가 누른 모든 영화들의 장르를 파싱하여 카운트한다. 영화는 중복될 수 있다.
        all_genres = []
        count_genres = {}
        for i in range(0, your_genres.count()):
            # all_genres.append(your_genres.values('interested_genre')[i].get('interested_genre'))
            str_data = your_genres.values('interested_genre')[
                i].get('interested_genre')
            tmp = str_data[1:len(str_data)-1].split(',')
            for element in tmp:
                all_genres.append(element.strip())
        # print(all_genres, type(all_genres))
        for key in all_genres:
            count_genres[key] = count_genres.get(key, 0) + 1
        # print(count_genres)

        # DB에서 선호 장르(빈도수)가 많이 겹치는 영화를 찾는다. 영화가 10개 이상일 경우에는 평점순으로 고른다.

        # 1. 선호 장르 순으로 정렬할 리스트를 만든다.
        count_genres_list = sorted(
            count_genres.items(), reverse=True, key=lambda item: item[1])
        # print(count_genres_list)
        # 1.5 선호 장르가 없는 경우 빈 값을 리턴한다.
        if not count_genres_list:
            return Response('', status=status.HTTP_201_CREATED)
        # print(request.user)

        # 2. 선호 장르 순으로 영화를 필터링한다. 필터링이 끝나기 전 영화가 10개 이하가 되면 필터링을 중단한다.
        filtered_movies = Movie.objects.all()
        for genre in count_genres_list:
            print(genre[0])
            movies = filtered_movies.filter(genre__contains=genre[0])
            if movies.count() <= 10:
                break
            else:
                filtered_movies = movies.order_by('-vote_average')

        # 3. 필터링된 영화를 평점순으로 6개를 고른다.
        filtered_movies = filtered_movies[:6]
        print(type(filtered_movies))
        serializer = MovieListSerializer(filtered_movies, many=True)
        # print(serializer.data)
        # if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        # print(serializer.errors)
        # return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def recommend_clear(request):
    user = request.user
    user.recommendation_set.clear()
    return Response(status=status.HTTP_205_RESET_CONTENT)
