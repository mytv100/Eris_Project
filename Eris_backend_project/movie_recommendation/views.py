# Create your views here.
import random
from typing import Any
from urllib.request import Request

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework import mixins
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from movie_recommendation.models import ActorMovie, CustomerMovie, BusinessPartnerMovie, \
    Customer, BusinessPartner, Movie, Actor
from movie_recommendation.module.filtering import movie_filtering
from movie_recommendation.permissions import UserPermission
from movie_recommendation.serializers import BusinessPartnerMovieSerializer, MovieSerializer, CustomerSerializer, \
    CustomerUpdateSerializer, CustomerMovieSerializer, BusinessPartnerSerializer, ActorMovieSerializer, \
    CustomerMovieUpdateSerializer, CustomMovieListSerializer
from movie_recommendation.mixin import mixin

import csv


class CustomerAPIViewSet(viewsets.GenericViewSet,
                         mixins.DestroyModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin, ):
    """
    Customer CRUD API for BusinessPartner
    """
    queryset = Customer.objects.all()
    permission_classes = [IsAuthenticated]  # 로그인 해야만 접근 가능
    serializer_class = CustomerSerializer
    lookup_field = ('nickname')  # id 값 대신 nickname 필드를 조회에 사용

    def create(self, request: Request, *args: Any, **kwargs: Any):
        """
        고객 데이터 입력(생성) - 양식
        "age" : 10,
        "gender" : true | 1 -> (man) or false | -0 > (woman)
        "nickname" : "string" (중복X)
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        queryset = self.get_queryset().filter(nickname=self.request.data['nickname'])
        if queryset.exists():
            raise ValidationError('Customer have already signed up')
        serializer.save(associated_bp=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """
        nickname으로 회원 정보 조회하기
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request: Request, *args: Any, **kwargs: Any):
        """
        업체가 보유한 고객 목록 조회
        """
        return super(CustomerAPIViewSet, self).list(request, args, kwargs)

    # custom view for update
    @action(detail=True, methods=['patch'], serializer_class=CustomerUpdateSerializer)
    def update_customer(self, request: Request, *args, **kwargs):
        """
        변경할 정보 입력 - 양식
        "age" : 10,
        "gender" : true | 1 -> (man) or false | -0 > (woman)
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """
        nickname 값으로 고객 삭제
        """
        return super(CustomerAPIViewSet, self).destroy(request, args, kwargs)

    def get_queryset(self):
        queryset = self.queryset.filter(associated_bp=self.request.user)
        return queryset


class BusinessPartnerMovieAPIViewSet(viewsets.GenericViewSet,
                                     mixins.CreateModelMixin,
                                     mixins.DestroyModelMixin,
                                     mixins.RetrieveModelMixin,
                                     mixins.ListModelMixin,
                                     mixin.DoubleFieldLookupMixin):
    """
    업체가 보유한 영화에 대한 API
    """
    queryset = Movie.objects.all()
    serializer_class = BusinessPartnerMovieSerializer
    permission_classes = [IsAuthenticated]  # 로그인 해야만 접근 가능
    lookup_fields = ('title', 'director')

    def create(self, request, *args, **kwargs):
        """
        title과 director 값으로 업체에서 보유중인 영화 추가
        "title" : "title"
        "director" : "director"
        """
        return super(BusinessPartnerMovieAPIViewSet, self).create(request, args, kwargs)

    def perform_create(self, serializer):
        queryset = self.get_queryset().filter(title=self.request.data['movie']['title'],
                                              director=self.request.data['movie']['director'])
        if queryset.exists():
            raise ValidationError("You have already this movie")
        serializer.save(movie_owner=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """
        title과 director 값으로 업체에서 보유중인 영화 조회
        """
        instance = self.get_object()
        serializer = MovieSerializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = MovieSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = MovieSerializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        title과 director 값으로 업체에서 보유중인 영화 삭제
        """
        return super(BusinessPartnerMovieAPIViewSet, self).destroy(request, args, kwargs)

    def perform_destroy(self, instance):
        businesspartner_movie_instance = BusinessPartnerMovie.objects.get(movie=instance)
        businesspartner_movie_instance.delete()

    def get_object(self):
        obj = mixin.DoubleFieldLookupMixin.get_object(self)
        return obj

    def get_queryset(self):
        queryset = self.queryset.filter(movie_owner=self.request.user)
        return queryset


class CustomerMovieAPIViewSet(viewsets.GenericViewSet,
                              mixins.CreateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.DestroyModelMixin,
                              mixins.ListModelMixin,
                              mixin.TripleFieldLookupMixin):
    """
    고객이 평가한 영화
    """
    # 로그인 해야만 접근 가능
    permission_classes = [IsAuthenticated]
    queryset = CustomerMovie.objects.all()
    # queryset = Movie.objects.all()
    serializer_class = CustomerMovieSerializer
    lookup_fields = ('title', 'director', 'nickname')

    def create(self, request, *args, **kwargs):
        """
        title과 director 값으로 업체의 고객이 평가한 영화 저장
        "title" : "title"
        "director" : "director"
        """
        return super(CustomerMovieAPIViewSet, self).create(request, args, kwargs)

    def perform_create(self, serializer):
        queryset = self.get_queryset().filter(movie__movie_owner=self.request.user,
                                              movie__title=self.request.data['movie']['title'],
                                              movie__director=self.request.data['movie']['director'],
                                              customer__nickname=self.request.data['nickname'])
        # queryset = self.get_queryset().filter(title=self.request.data['movie']['title'], director=self.request.data['movie']['director'],
        #                                       customermovie__customer__nickname=self.request.data['nickname'])
        if queryset.exists():
            raise ValidationError("Customer have already this movie")
        serializer.save(associated_bp=self.request.user)
        # serializer.save(associated_bp=self.request.user, nickname=self.request.data['nickname'])

    def retrieve(self, request, *args, **kwargs):
        """
        title과 director, nickname 값으로 업체의 고객이 평가한 영화 조회
        """
        instance = self.get_object()
        serializer = CustomerMovieSerializer(instance)
        return Response(serializer.data)

    def list(self, request: Request, *args: Any, **kwargs: Any):
        """
        업체의 고객들이 평가한 모든 영화 조회
        """
        return super(CustomerMovieAPIViewSet, self).list(request, args, kwargs)

    # Custom API
    @action(detail=True, methods=['get'])
    def movie_list(self, request: Request, *args, **kwargs):
        """
        고객 닉네임과 선택된 영화를 받아서
        필터링(추천 알고리즘) 과정을 거쳐서
        리스트로 반환해줌
        """
        customer = Customer.objects.filter(associated_bp=request.user, nickname=self.kwargs['nickname']).get()
        movie = Movie.objects.filter(title=self.kwargs['title'], director=self.kwargs['director']).get()
        result_dict = {}
        movie_list = []
        result_list = movie_filtering(customer.id, movie.movie_pk, request.user.id)
        for i, j in enumerate(result_list):
            result_dict[i] = j

        movie_list.append(result_dict)
        serializer = CustomMovieListSerializer(data=movie_list, many=True)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['patch'], serializer_class=CustomerMovieUpdateSerializer)
    def update(self, request, *args, **kwargs):
        """
        title 과 director, nickname 값으로 업체의 고객의 영화에 대한 평점 변경
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """
        title 과 director, nickname 값으로 업체의 고객의 영화에 대한 평점 삭제
        """
        return super(CustomerMovieAPIViewSet, self).destroy(request, args, kwargs)

    def perform_destroy(self, instance):
        instance.delete()

    def get_object(self):
        obj = mixin.TripleFieldLookupMixin.get_object(self)
        return obj

    def get_queryset(self):
        queryset = self.queryset.filter(customer__associated_bp=self.request.user)
        return queryset


class ActorMovieAPIViewSet(viewsets.ModelViewSet):
    """
    영화에 출연한 배우
    """
    # 관리자만 접근할 수 있음
    permission_classes = [IsAdminUser]
    queryset = ActorMovie.objects.all()
    serializer_class = ActorMovieSerializer

    def get_queryset(self):
        queryset = self.queryset.filter()
        return queryset


# 회원가입을 처리하는 ViewSet
class CreateBusinessPartnerAPIViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = BusinessPartner.objects.all()
    serializer_class = BusinessPartnerSerializer
    permission_classes = (UserPermission,)

    def create(self, request: Request, *args: Any, **kwargs: Any):
        """
        회원가입
        'username' : 'id'
        'password' : 'password'
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# class InitViewSet(viewsets.GenericViewSet,
#                   mixins.ListModelMixin,
#                   mixins.UpdateModelMixin, ):
#     queryset = BusinessPartner.objects.all()
#     serializer_class = None
#     permission_classes = [IsAdminUser]
#
#     # Update
#     def update(self, request: Request, *args: Any, **kwargs: Any):
#
#         """  make customer dummy data
#
#             j : user(업체) 1~4 (pk 2~5, 1 is root)
#             i : customer(고객) 1~30
#             for j in range(1, 5, 1):
#                 for i in range(1, 31, 1):
#                     gender = True if random.randint(0, 1) else False
#                     age = random.randrange(10, 60, 1)
#                     nickname = "customer" + str(i)
#                     associated_bp = "user" + str(j)
#                     Customer.objects.create(gender=gender, age=age, nickname=nickname,
#                                             associated_bp=BusinessPartner.objects.get(username=associated_bp))
#         """
#
#         """
#         BP - Movie
#         CU - Movie
#         2 번 진행함
#         4 * 30 * 100 * 2 = 24000개
#         """
#
#         movies = Movie.objects.all()
#         for j in range(1, 5, 1):
#             for i in range(1, 31, 1):
#                 business_partner = BusinessPartner.objects.get(username="user" + str(j))
#                 customer = Customer.objects.get(nickname='customer' + str(i), associated_bp=business_partner)
#                 for k in range(100):
#                     movie = random.choice(movies)
#                     rate = round(random.uniform(0.0, 10.0), 1)
#                     CustomerMovie.objects.create(rate=rate, customer=customer, movie=movie)
#                     BusinessPartnerMovie.objects.create(movie=movie, businessPartner=business_partner)
#
#         return Response(None, status=status.HTTP_201_CREATED)
#
#     # GET
#     def list(self, request, *args, **kwargs):
#         """
#         영화와 배우를 서비스의 데이터베이스로 불러오는 역할을 함
#         오래 걸리니까 데이터베이스 날려먹으면 안됨
#         """
#
#         # movie data
#         f = open("movie_recommendation/data/movie.tsv", "r", encoding='utf-8')
#         rows = csv.reader(f, delimiter='\t')
#         for row in rows:
#             if not row[5]:
#                 row[5] = 0.0
#             if not row[6]:
#                 row[6] = 0
#             if row[2] == "\\N":
#                 row[2] = 0
#             if not row[3]:
#                 row[3] = "ETC"
#
#             movie_data = {
#                 "movie_pk": row[0],
#                 "title": row[1],
#                 "running_time": row[2],
#                 "genre": row[3],
#                 "director": row[4],
#                 "rate": row[5],
#                 "votes": row[6],
#             }
#             serializer = MovieSerializer(data=movie_data)
#             if serializer.is_valid(raise_exception=True):
#                 serializer.save()
#         f.close()
#
#         # actor data
#         f = open("movie_recommendation/data/actor.tsv", "r", encoding='utf-8')
#         rows = csv.reader(f, delimiter='\t')
#         for row in rows:
#             actor_data = {
#                 "actor_pk": row[0],
#                 "name": row[1],
#             }
#             serializer = ActorSerializer(data=actor_data)
#             if serializer.is_valid(raise_exception=True):
#                 serializer.save()
#         f.close()
#
#         # actor_movie data
#         f = open("movie_recommendation/data/actormovie.tsv", "r", encoding='utf-8')
#         rows = csv.reader(f, delimiter='\t')
#
#         for row in rows:
#             print(row)
#             movie = Movie.objects.get(movie_pk=row[0])
#             actors = Actor.objects.filter(actor_pk=row[1])
#             for actor in actors:
#                 actor_movie_data = {
#                     "actor": actor,
#                     "movie": movie,
#                 }
#                 serializer = CustomActorMovieSerializer(data=actor_movie_data)
#                 print(serializer)
#                 if serializer.is_valid(raise_exception=True):
#                     serializer.save()
#
#         f.close()
#
#         headers = self.get_success_headers(None)
#         return Response(None, status=status.HTTP_201_CREATED, headers=headers)
