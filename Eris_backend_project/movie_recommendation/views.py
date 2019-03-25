# Create your views here.
from typing import Any
from urllib.request import Request

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from forms.signup import UserForm
from movie_recommendation.models import ActorMovie, CustomerMovie, BusinessPartnerMovie, \
    Customer, BusinessPartner, Movie
from movie_recommendation.serializers import ActorMovieSerializer, CustomerMovieSerializer, \
    BusinessPartnerMovieSerializer, CustomerSerializer, MovieListSerializer


def signup(request):
    """
    회원가입을 위한 view
    form 에 입력된 데이터가 적절하면(유효하면)
    로그인 처리하고, /api/doc/ 으로 넘어감

    적절하지 않다면 다시 회원가입 페이지 보여줌
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            return redirect('/api/doc/')
        else:
            form = UserForm()
            return render(request, 'signup.html', {'form': form})


class BusinessPartnerMovieAPIViewSet(viewsets.ModelViewSet):
    """
    업체가 보유한 영화
    """
    queryset = BusinessPartnerMovie.objects.all()
    serializer_class = BusinessPartnerMovieSerializer
    # 로그인 해야만 접근 가능
    permission_classes = [IsAuthenticated]

    def create(self, request: Request, *args: Any, **kwargs: Any):
        # 중복 확인해서 이미 데이터베이스에 있는 데이터면 code 202 반환
        for query in self.queryset.filter(businessPartner=request.user):
            if request.data['movie']['title'] == query.movie.title:
                headers = self.get_success_headers(None)
                # 202 말고 다른 error 필요함 뭔지 잘 모르겠음
                # 중복된 거 있으면 안받아줌
                return Response(None, status=status.HTTP_202_ACCEPTED, headers=headers)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 로그인한 사용자(업체)의 username 값을 넣어줌
        serializer.validated_data["businesspartner"] = {"username": request.user.username}
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CustomerAPIViewSet(viewsets.ModelViewSet):
    # 로그인 해야만 접근 가능
    permission_classes = [IsAuthenticated]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any):
        # 중복 확인해서 이미 데이터베이스에 있는 데이터면 code 202 반환
        for query in self.queryset:
            if request.user.username + "-" + request.data["nickname"] == query.nickname:
                headers = self.get_success_headers(None)
                # 202 말고 다른 error 필요함 뭔지 잘 모르겠음
                # 중복된 거 있으면 안받아줌
                return Response(None, status=status.HTTP_202_ACCEPTED, headers=headers)

        request.data["nickname"] = request.user.username + "-" + request.data["nickname"]
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
        # 중복 확인해서 이미 데이터베이스에 있는 데이터면 code 202 반환
        for query in self.queryset:
            if request.data['movie']['title'] == query.movie.title:
                headers = self.get_success_headers(None)
                # 202 말고 다른 error 필요함 뭔지 잘 모르겠음
                # 중복된 거 있으면 안받아줌
                return Response(None, status=status.HTTP_202_ACCEPTED, headers=headers)

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

    # overriding
    def create(self, request: Request, *args: Any, **kwargs: Any):
        # 중복 확인해서 이미 데이터베이스에 있는 데이터면 code 202 반환
        for query in self.queryset:
            if request.user.username + "-" + request.data['customer']["nickname"] == query.customer.nickname:
                for m in Movie.objects.filter(title=request.data['movie']['title']):
                    if query.movie == m:
                        headers = self.get_success_headers(None)
                        # 202 말고 다른 error 필요함 뭔지 잘 모르겠음
                        # 중복된 거 있으면 안받아줌
                        return Response(None, status=status.HTTP_202_ACCEPTED, headers=headers)
        # customer nickname 으로 구분할 수 있도록 Businesspartner.name-Customer.nickname 으로 구성
        request.data['customer']["nickname"] = request.user.username + "-" + request.data['customer']["nickname"]
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # Custom API
    # swagger에 나오는 것 까지만 확인함
    @action(detail=False, methods=['post'], serializer_class=MovieListSerializer)
    def movie_list(self, request: Request):
        """
        고객 닉네임과 선택된 영화(없어도 됨)를 받아서
        필터링(추천 알고리즘) 과정을 거쳐서
        리스트로 반환해줌
        """
        customers = Customer.objects.filter(associated_bp=request.user)
        for customer in customers:
            if customer.nickname == request.user.username + "-" + request.data['customer']['nickname']:
                # result_list = movie_filtering(customer, request.data['movie'])
                result_list = None
                serializer = self.get_serializer(result_list, many=True)
                return Response(serializer.data)

        return Response(None)
