from typing import Any

from rest_framework import serializers

from movie_recommendation.models import Movie, ActorMovie, CustomerMovie, BusinessPartnerMovie
from movie_recommendation.models import Actor
from movie_recommendation.models import Customer
from movie_recommendation.models import BusinessPartner


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        exclude = ('movie',)


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        # 해당 필드만 제외 됨 % fields = "__all__" 과 같이 사용 불가능
        exclude = ('movie_owner',)


class ActorMovieSerializer(serializers.Serializer):
    """
    Actor 와 Movie 의 M2M (through 클래스) serializer
    """
    actor = ActorSerializer()
    movie = MovieSerializer()

    class Meta:
        model = ActorMovie
        fields = ["movie", 'actor']

    def create(self, validated_data: Any):
        movie = Movie.objects.create(**validated_data.get('movie'))
        # actor를 , 로 구분해서 여러 명 입력받아서 등록
        actor_dict = validated_data.get('actor')
        actor_list = actor_dict['name'].split(",")
        for name in actor_list:
            actor = Actor.objects.create(name=name)
            actor_movie = ActorMovie.objects.create(actor=actor, movie=movie)
        return actor_movie


class CustomActorMovieSerializer(serializers.Serializer):

    def save(self):
        movie = self.validated_data['movie']
        actor = self.validated_data['actor']
        actor_movie = ActorMovie.objects.create(actor=actor, movie=movie)
        return actor_movie

    def to_internal_value(self, data: Any):
        actor = data.get("actor")
        movie = data.get("movie")

        if not actor:
            raise serializers.ValidationError({
                'actor': "This field is required"
            })
        if not movie:
            raise serializers.ValidationError({
                "movie": "This field is required"
            })

        return {
            "actor": actor,
            "movie": movie
        }


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ['associated_bp', 'movie']


class MovieTitleSerializer(serializers.ModelSerializer):
    """
    영화 제목과 감독명만 있는 serializer
    """

    class Meta:
        model = Movie
        fields = ["title", "director"]


class BusinessPartnerMovieSerializer(serializers.ModelSerializer):
    """
    BusinessPartner 와 Movie 의 M2M (through 클래스) serializer
    """
    movie = MovieTitleSerializer()

    class Meta:
        model = BusinessPartnerMovie
        fields = ["movie", ]

    def create(self, validated_data: Any):
        movie = Movie.objects.get(**validated_data.get('movie'))
        business_partner = BusinessPartner.objects.get(**validated_data.get('business_partner'))
        business_partner_movie = BusinessPartnerMovie.objects.create(businessPartner=business_partner, movie=movie)
        return business_partner_movie


class CustomerNameSerializer(serializers.ModelSerializer):
    """
    고객 닉네임만 있는 serializer
    """

    class Meta:
        model = Customer
        fields = ["nickname", ]


class CustomerMovieSerializer(serializers.ModelSerializer):
    """
    Customer 와 Movie 의 M2M (through 클래스) serializer
    """
    customer = CustomerNameSerializer()
    movie = MovieTitleSerializer()

    class Meta:
        model = CustomerMovie
        fields = "__all__"

    def create(self, validated_data: Any):
        # 고객과 영화 데이터 가져와서
        # 평점과 함께 CustomerMovie에 저장
        customer = Customer.objects.get(**validated_data.get('customer'))
        movie = Movie.objects.get(**validated_data.get('movie'))
        rate = validated_data.get('rate')
        customer_movie = CustomerMovie.objects.create(customer=customer, movie=movie, rate=rate)
        return customer_movie


class MovieListSerializer(serializers.Serializer):
    """
    고객 닉네임과 영화 이름(선택)을 선택받아서
    추천 리스트 반환해주기 위한 Serializer
    """

    customer = CustomerNameSerializer(write_only=True)
    movie = MovieTitleSerializer(write_only=True)


class BusinessPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessPartner
        fields = ['username', 'password']
        write_only_fields = ('password',)

    def create(self, validated_data: Any):
        businesspartner = BusinessPartner.objects.create(
            username=validated_data['username'],
        )
        businesspartner.set_password(validated_data['password'])
        businesspartner.save()

        return businesspartner


class CustomMovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        exclude = ['movie_owner', 'created_at', 'movie_pk']

    def to_internal_value(self, data: Any):
        movie_list = []
        for i in range(len(data)):
            movie = data.get(i)
            movie_list.append(movie)
        if not movie_list:
            raise serializers.ValidationError({
                "movie_list": "This field is required"
            })

        return movie_list

    def to_representation(self, instance: Any):
        movie_list = {}
        for i, j in enumerate(instance):
            movie = Movie.objects.get(pk=j["movie"])
            movie_list[i] = {
                "movie_pk": movie.movie_pk,
                "title": movie.title,
                "genre": movie.genre,
                "director": movie.director,
                "running_time": movie.running_time,
                "rate": movie.rate,
                "description": movie.description,
            }
        return movie_list
