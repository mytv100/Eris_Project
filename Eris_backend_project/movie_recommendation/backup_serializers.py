from collections import OrderedDict
from typing import Any

from django.db.models import Model
from rest_framework import serializers
from rest_framework.fields import CharField, SkipField
from rest_framework.relations import PKOnlyObject

from movie_recommendation.models import Movie, ActorMovie, CustomerMovie, BusinessPartnerMovie
from movie_recommendation.models import Actor
from movie_recommendation.models import Customer
from movie_recommendation.models import BusinessPartner


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        exclude = ('movie_owner',)


class CustomerSerializer(serializers.ModelSerializer):
    """
    고객 정보 입력 및 출력용
    입력 : C
    출력 : C, R, D
    """

    class Meta:
        model = Customer
        exclude = ['associated_bp', 'movie']

    def to_internal_value(self, data: Any):
        age = data.get('age')
        nickname = data.get('nickname')
        gender = data.get('gender')

        if not nickname:
            raise serializers.ValidationError({
                'nickname': 'This field is required.'
            })
        if not age:
            raise serializers.ValidationError({
                'age': 'This field is required.'
            })
        if gender == "":
            raise serializers.ValidationError({
                'gender': 'This field is required.'
            })

        return {
            "age": age,
            "gender": gender,
            "nickname": nickname,
        }

    def to_representation(self, instance):
        ret = OrderedDict()

        fields = self._readable_fields
        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue

            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                if field.field_name == "id":
                    continue
                elif field.field_name == "gender":
                    if field.to_representation(attribute):
                        ret[field.field_name] = "man"
                    else:
                        ret[field.field_name] = "woman"
                    continue
                else:
                    ret[field.field_name] = field.to_representation(attribute)
        return ret


class CustomerUpdateSerializer(serializers.ModelSerializer):
    update_field = serializers.DictField(child=CharField())
    """
    고객 닉네임과 dictionary field 만 있는 serializer
    고객 데이터 조회시 pk 값 대신 닉네임 + BP 로 조회함
    dictionary field 를 통해서 update할 값을 받아줌
    Update 입출력
    """

    class Meta:
        model = Customer
        fields = ['update_field']

    def update(self, instance: Model, validated_data: Any):

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_internal_value(self, data: Any):
        age = data.get('update_field').get('age')
        gender = data.get('update_field').get('gender')
        ret = OrderedDict()

        if gender == "":
            raise serializers.ValidationError({
                'gender': 'This field is required.'
            })

        if age:
            ret['age'] = age

        if gender is not None:
            ret['gender'] = gender

        return ret

    def to_representation(self, instance):
        if instance.gender == 0:
            gender = 'woman'
        else:
            gender = 'man'
        return {
            "age": instance.age,
            "gender": gender,
            "nickname": instance.nickname,
        }


class MovieTitleSerializer(serializers.ModelSerializer):
    """
    영화 제목과 감독명만 있는 serializer
    ( business_partner 가 재공하는 정보로, movie_pk 대신 식별에 사용함 )
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
        business_partner_movie = BusinessPartnerMovie.objects.create(businessPartner=validated_data.get('movie_owner'),
                                                                     movie=movie)
        return business_partner_movie

    def to_internal_value(self, data: Any):
        movie = data.get('movie')

        if not movie["title"]:
            raise serializers.ValidationError({
                'title': 'This field is required.'
            })
        if not movie["director"]:
            raise serializers.ValidationError({
                'director': 'This field is required.'
            })

        return {
            'movie': {
                "title": movie["title"],
                "director": movie["director"]
            }
        }


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        exclude = ('movie',)


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


class CustomerMovieUpdateSerializer(serializers.ModelSerializer):
    rate = serializers.FloatField()

    class Meta:
        model = CustomerMovie
        fields = ['rate']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_representation(self, instance: Any):
        ret = OrderedDict()

        ret['title'] = instance.movie.title
        ret['director'] = instance.movie.director
        ret['nickname'] = instance.customer.nickname
        ret['rate'] = instance.rate

        return ret


class CustomerMovieSerializer(serializers.ModelSerializer):
    """
    Customer 와 Movie 의 M2M (through 클래스) serializer
    """
    movie = MovieTitleSerializer()
    nickname = serializers.CharField()
    rate = serializers.FloatField()

    class Meta:
        model = CustomerMovie
        fields = ('movie', 'nickname', 'rate')

    def create(self, validated_data: Any):
        customer = validated_data.get('customer').get(associated_bp=validated_data.get('associated_bp'))
        movie = validated_data.get('movie').get()
        rate = validated_data.get('rate')

        customer_movie = CustomerMovie.objects.create(movie=movie, customer=customer, rate=rate)
        return customer_movie

    def update(self, instance, validated_data):
        instance.objects.update(rate=validated_data('rate'))
        instance.save()
        return instance

    def to_internal_value(self, data: Any):
        movie = data.get('movie')
        nickname = data.get('nickname')
        rate = data.get('rate')
        if not movie["title"]:
            raise serializers.ValidationError({
                'title': 'This field is required.'
            })
        if not movie["director"]:
            raise serializers.ValidationError({
                'director': 'This field is required.'
            })
        if not nickname:
            raise serializers.ValidationError({
                'nickname': 'This field is required.'
            })
        if not rate:
            raise serializers.ValidationError({
                'rate': 'This field is required'
            })
        movie_instance = Movie.objects.filter(title=movie['title'], director=movie['director'])
        customer_instance = Customer.objects.filter(nickname=nickname)
        return {
            'movie': movie_instance,
            'customer': customer_instance,
            'rate': rate
        }

    def to_representation(self, instance: Any):
        ret = OrderedDict()

        ret['title'] = instance.movie.title
        ret['director'] = instance.movie.director
        ret['nickname'] = instance.customer.nickname
        ret['rate'] = instance.rate

        return ret


class BusinessPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessPartner
        fields = ['username', 'password']
        write_only_fields = ('password',)

    def create(self, validated_data: Any):
        business_partner = BusinessPartner.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email='',
        )
        return business_partner


class CustomerNameSerializer(serializers.ModelSerializer):
    """
    고객 닉네임만 있는 serializer
    고객 데이터 조회시 pk 값 대신 닉네임 + BP 로 조회함
    입력 : R, D
    """

    class Meta:
        model = Customer
        fields = ["nickname", ]


class CustomMovieListSerializer(serializers.Serializer):

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

#
#
# class CustomActorMovieSerializer(serializers.Serializer):
#
#     def save(self):
#         movie = self.validated_data['movie']
#         actor = self.validated_data['actor']
#         actor_movie = ActorMovie.objects.create(actor=actor, movie=movie)
#         return actor_movie
#
#     def to_internal_value(self, data: Any):
#         actor = data.get("actor")
#         movie = data.get("movie")
#
#         if not actor:
#             raise serializers.ValidationError({
#                 'actor': "This field is required"
#             })
#         if not movie:
#             raise serializers.ValidationError({
#                 "movie": "This field is required"
#             })
#
#         return {
#             "actor": actor,
#             "movie": movie
#         }
#
#
