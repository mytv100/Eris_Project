from typing import Any

from rest_framework.decorators import api_view, schema, action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.schemas import AutoSchema

from movie_recommendation.models import NewCustomer, NewMovie, Genre, Ratings, BusinessPartner
from django.utils import timezone
from django.db.models import Sum, Count

from movie_recommendation.module.filtering import movie_filtering
from movie_recommendation.serializers import MovieSerializer, CustomerSerializer


@api_view()
def initData(request):
    businesspartner = BusinessPartner.objects.get(username='user1')

    # 장르 데이터
    f = open('movie_recommendation/module/data/ml-100k/u.genre', 'rb')
    genre_list = []
    for line in f.readlines():
        string = line.decode('ISO-8859-1')
        string_list = string.split('|')
        Genre.objects.create(name=string_list[0])
        genre_list.append(string_list[0])
        if string_list[0] == 'Western':
            break
    f.close()

    # 영화 데이터
    f = open('movie_recommendation/module/data/ml-100k/u.item', 'rb')

    for line in f.readlines():
        string = line.decode('ISO-8859-1')
        string_list = string.split('|')
        released_date = timezone.datetime.strptime(string_list[2], '%d-%b-%Y')  # .strftime('%Y-%m-%d')
        movie = NewMovie.objects.create(id=string_list[0], title=string_list[1], released_date=released_date)
        movie.businessPartner.add(businesspartner)

        for i in range(5, 24):
            if string_list[i]:
                genre = Genre.objects.get(name=genre_list[i - 5])
                movie.genre_set.add(genre)
    f.close()

    # 고객 데이터
    f = open('movie_recommendation/module/data/ml-100k/u.user', 'rb')

    for line in f.readlines():
        string = line.decode('ISO-8859-1')
        string_list = string.split('|')
        customer = NewCustomer.objects.create(id=string_list[0], age=string_list[1], gender=string_list[2],
                                              occupation=string_list[3])
        customer.businessPartner.add(businesspartner)
    f.close()

    # 평점 데이터
    f = open('movie_recommendation/module/data/ml-100k/u.data', 'rb')

    for line in f.readlines():
        string = line.decode('ISO-8859-1')
        string_list = string.split("\t")
        Ratings.objects.create(customer_id=string_list[0], movie_id=string_list[1], rate=string_list[2])

    f.close()

    # 영화 데이터에 평점, 투표 수 추가
    query_set = Ratings.objects.values('rate', 'movie__id')
    qs_annotate = query_set.values('movie__id').annotate(count=Count('movie__id'), sum=Sum('rate'))
    for q in qs_annotate:
        NewMovie.objects.filter(id=q['movie__id']).update(votes=q['count'], rate=round(q['sum'] / q['count'], 1))

    return Response(None)


class MovieAPIViewSet(viewsets.ModelViewSet):
    queryset = NewMovie.objects.all()
    serializer_class = MovieSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any):
        return super(MovieAPIViewSet, self).create(request, args, kwargs)

    def retrieve(self, request: Request, *args: Any, **kwargs: Any):
        return super(MovieAPIViewSet, self).retrieve(request, args, kwargs)

    def list(self, request: Request, *args: Any, **kwargs: Any):
        return super(MovieAPIViewSet, self).list(request, args, kwargs)

    def update(self, request: Request, *args: Any, **kwargs: Any):
        return super(MovieAPIViewSet, self).update(request, args, kwargs)

    def partial_update(self, request: Request, *args: Any, **kwargs: Any):
        return super(MovieAPIViewSet, self).partial_update(request, args, kwargs)

    def destroy(self, request: Request, *args: Any, **kwargs: Any):
        return super(MovieAPIViewSet, self).destroy(request, args, kwargs)


class CustomerAPIViewSet(viewsets.ModelViewSet):
    queryset = NewCustomer.objects.all()
    serializer_class = CustomerSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any):
        return super(CustomerAPIViewSet, self).create(request, args, kwargs)

    def retrieve(self, request: Request, *args: Any, **kwargs: Any):
        return super(CustomerAPIViewSet, self).retrieve(request, args, kwargs)

    def list(self, request: Request, *args: Any, **kwargs: Any):
        return super(CustomerAPIViewSet, self).list(request, args, kwargs)

    def update(self, request: Request, *args: Any, **kwargs: Any):
        return super(CustomerAPIViewSet, self).update(request, args, kwargs)

    def partial_update(self, request: Request, *args: Any, **kwargs: Any):
        return super(CustomerAPIViewSet, self).partial_update(request, args, kwargs)

    def destroy(self, request: Request, *args: Any, **kwargs: Any):
        return super(CustomerAPIViewSet, self).destroy(request, args, kwargs)


@api_view(['GET'])
def MovieRecommend(request, **kwargs):
    result_dict = {}
    movie_list = []

    result_list = movie_filtering(kwargs['customer_id'], kwargs['movie_id'], 2)
    for i, j in enumerate(result_list):
        result_dict[i] = j

    movie_list.append(result_dict)

    return Response(movie_list, status=status.HTTP_200_OK)
