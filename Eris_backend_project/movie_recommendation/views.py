# Create your views here.
import random
from typing import Any
from urllib.request import Request

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework import mixins
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from movie_recommendation.models import ActorMovie, CustomerMovie, BusinessPartnerMovie, \
    Customer, BusinessPartner, Movie, Actor
from movie_recommendation.module.filtering import movie_filtering
from movie_recommendation.permissions import UserPermission
from movie_recommendation.serializers import ActorMovieSerializer, CustomerMovieSerializer, \
    BusinessPartnerMovieSerializer, CustomerSerializer, MovieListSerializer, BusinessPartnerSerializer, \
    ActorSerializer, CustomActorMovieSerializer, MovieSerializer, CustomMovieListSerializer
import csv


class BusinessPartnerMovieAPIViewSet(viewsets.ModelViewSet):
    """
    업체가 보유한 영화
    """
    queryset = BusinessPartnerMovie.objects.all()
    serializer_class = BusinessPartnerMovieSerializer
    # 로그인 해야만 접근 가능
    permission_classes = [IsAuthenticated]

    def create(self, request: Request, *args: Any, **kwargs: Any):
        # 중복 확인해서 이미 데이터베이스에 있는 데이터면 code 400 반환
        for query in self.queryset.filter(businessPartner=request.user):
            if request.data['movie']['title'] == query.movie.title and \
                    request.data['movie']['director'] == query.movie.director:
                headers = self.get_success_headers(None)
                return Response(None, status=status.HTTP_400_BAD_REQUEST, headers=headers)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 로그인한 사용자(업체)의 username 값을 넣어줌
        serializer.validated_data["business_partner"] = {"username": request.user.username}
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CustomerAPIViewSet(viewsets.ModelViewSet):
    # 로그인 해야만 접근 가능
    permission_classes = [IsAuthenticated]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any):
        # 중복 확인해서 이미 데이터베이스에 있는 데이터면 code 400 반환
        for query in self.queryset:
            if request.data["nickname"] == query.nickname and request.user.username == query.associated_bp.username:
                headers = self.get_success_headers(None)
                return Response(None, status=status.HTTP_400_BAD_REQUEST, headers=headers)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # validated_data에 "associated_bp" (FK BusinessPartner)의 값을 넣어줌
        serializer.validated_data["associated_bp"] = BusinessPartner.objects.get(username=request.user.username)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ActorMovieAPIViewSet(viewsets.ModelViewSet):
    """
    영화에 출연한 배우
    """
    # 관리자만 접근할 수 있음
    permission_classes = [IsAdminUser]
    queryset = ActorMovie.objects.all()
    serializer_class = ActorMovieSerializer

    # overriding
    def create(self, request: Request, *args: Any, **kwargs: Any):
        # 중복 확인해서 이미 데이터베이스에 있는 데이터면 code 400 반환
        for query in self.queryset:
            if request.data['movie']['title'] == query.movie.title and \
                    request.data['movie']['director'] == query.movie.director:
                headers = self.get_success_headers(None)
                return Response(None, status=status.HTTP_400_BAD_REQUEST, headers=headers)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CustomerMovieAPIViewSet(viewsets.ModelViewSet):
    """
    고객이 평가한 영화
    """
    # 로그인 해야만 접근 가능
    permission_classes = [IsAuthenticated]
    queryset = CustomerMovie.objects.all()
    serializer_class = CustomerMovieSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any):
        # 중복 확인해서 이미 데이터베이스에 있는 데이터면 code 400 반환
        for query in self.queryset:
            if request.data['customer']["nickname"] == query.customer.nickname:
                for m in Movie.objects.filter(title=request.data['movie']['title'],
                                              director=request.data['movie']['director']):
                    if query.movie == m:
                        headers = self.get_success_headers(None)
                        return Response(None, status=status.HTTP_400_BAD_REQUEST, headers=headers)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # Custom API
    @action(detail=False, methods=['post'], serializer_class=MovieListSerializer)
    def movie_list(self, request: Request):
        """
        고객 닉네임과 선택된 영화(없어도 됨)를 받아서
        필터링(추천 알고리즘) 과정을 거쳐서
        리스트로 반환해줌
        """
        customer = Customer.objects.get(associated_bp=request.user.id, nickname=request.data['customer']['nickname'])
        movie = Movie.objects.get(title=request.data['movie']['title'], director=request.data['movie']['director'])
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


# 회원가입을 처리하는 ViewSet
class CreateBusinessPartnerAPIViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = BusinessPartner.objects.all()
    serializer_class = BusinessPartnerSerializer
    permission_classes = (UserPermission,)

    def create(self, request: Request, *args: Any, **kwargs: Any):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class InitViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.UpdateModelMixin, ):
    queryset = BusinessPartner.objects.all()
    serializer_class = None
    permission_classes = [IsAdminUser]

    # Update
    def update(self, request: Request, *args: Any, **kwargs: Any):

        """  make customer dummy data

            j : user(업체) 1~4 (pk 2~5, 1 is root)
            i : customer(고객) 1~30
            for j in range(1, 5, 1):
                for i in range(1, 31, 1):
                    gender = True if random.randint(0, 1) else False
                    age = random.randrange(10, 60, 1)
                    nickname = "customer" + str(i)
                    associated_bp = "user" + str(j)
                    Customer.objects.create(gender=gender, age=age, nickname=nickname,
                                            associated_bp=BusinessPartner.objects.get(username=associated_bp))
        """

        """
        BP - Movie
        CU - Movie
        2 번 진행함
        4 * 30 * 100 * 2 = 24000개
        """

        movies = Movie.objects.all()
        for j in range(1, 5, 1):
            for i in range(1, 31, 1):
                business_partner = BusinessPartner.objects.get(username="user" + str(j))
                customer = Customer.objects.get(nickname='customer' + str(i), associated_bp=business_partner)
                for k in range(100):
                    movie = random.choice(movies)
                    rate = round(random.uniform(0.0, 10.0), 1)
                    CustomerMovie.objects.create(rate=rate, customer=customer, movie=movie)
                    BusinessPartnerMovie.objects.create(movie=movie, businessPartner=business_partner)

        return Response(None, status=status.HTTP_201_CREATED)

    # GET
    def list(self, request, *args, **kwargs):
        """
        영화와 배우를 서비스의 데이터베이스로 불러오는 역할을 함
        오래 걸리니까 데이터베이스 날려먹으면 안됨
        """

        # movie data
        f = open("movie_recommendation/data/movie.tsv", "r", encoding='utf-8')
        rows = csv.reader(f, delimiter='\t')
        for row in rows:
            if not row[5]:
                row[5] = 0.0
            if not row[6]:
                row[6] = 0
            if row[2] == "\\N":
                row[2] = 0
            if not row[3]:
                row[3] = "ETC"

            movie_data = {
                "movie_pk": row[0],
                "title": row[1],
                "running_time": row[2],
                "genre": row[3],
                "director": row[4],
                "rate": row[5],
                "votes": row[6],
            }
            serializer = MovieSerializer(data=movie_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        f.close()

        # actor data
        f = open("movie_recommendation/data/actor.tsv", "r", encoding='utf-8')
        rows = csv.reader(f, delimiter='\t')
        for row in rows:
            actor_data = {
                "actor_pk": row[0],
                "name": row[1],
            }
            serializer = ActorSerializer(data=actor_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        f.close()

        # actormovie data
        f = open("movie_recommendation/data/actormovie.tsv", "r", encoding='utf-8')
        rows = csv.reader(f, delimiter='\t')

        for row in rows:
            print(row)
            movie = Movie.objects.get(movie_pk=row[0])
            actors = Actor.objects.filter(actor_pk=row[1])
            for actor in actors:
                actormovie_data = {
                    "actor": actor,
                    "movie": movie,
                }
                serializer = CustomActorMovieSerializer(data=actormovie_data)
                print(serializer)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()

        f.close()

        headers = self.get_success_headers(None)
        return Response(None, status=status.HTTP_201_CREATED, headers=headers)
