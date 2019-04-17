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
        # Dict of native values <- Dict of primitive datatypes.
        age = data.get('age')
        associated_bp = data.get('associated_bp')
        nickname = data.get('nickname')
        gender = data.get('gender')

        # Perform the data validation.

        if not nickname:
            raise serializers.ValidationError({
                'nickname': 'This field is required.'
            })
        if not age:
            raise serializers.ValidationError({
                'age': 'This field is required.'
            })
        if not associated_bp:
            raise serializers.ValidationError({
                'associated_bp': 'This field is required.'
            })
        if gender == "":
            raise serializers.ValidationError({
                'gender': 'This field is required.'
            })

        # Return the validated values. This will be available as
        # the `.validated_data` property.
        return {
            "age": age,
            "gender": gender,
            "nickname": nickname,
            "associated_bp": associated_bp,
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
        fields = ['nickname', 'update_field']

    def update(self, instance: Model, validated_data: Any):

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_internal_value(self, data: Any):
        nickname = data.get('nickname')
        associated_bp = data.get('associated_bp')
        age = data.get('update_field').get('age')
        gender = data.get('update_field').get('gender')
        ret = OrderedDict()

        if not nickname:
            raise serializers.ValidationError({
                'nickname': 'This field is required.'
            })

        if gender == "":
            raise serializers.ValidationError({
                'gender': 'This field is required.'
            })

        if age:
            ret['age'] = age

        if associated_bp:
            ret['associated_bp'] = associated_bp
        if gender is not None:
            ret['gender'] = gender
        ret['nickname'] = nickname

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
            "created_at": instance.created_at
        }


class CustomerNameSerializer(serializers.ModelSerializer):
    """
    고객 닉네임만 있는 serializer
    고객 데이터 조회시 pk 값 대신 닉네임 + BP 로 조회함
    입력 : R, D
    """

    class Meta:
        model = Customer
        fields = ["nickname", ]


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
        business_partner = BusinessPartner.objects.get(**validated_data.get('business_partner'))
        business_partner_movie = BusinessPartnerMovie.objects.create(businessPartner=business_partner, movie=movie)
        return business_partner_movie

    def update(self, instance: Model, validated_data: Any):
        pass

    def to_internal_value(self, data: Any):
        # Dict of native values <- Dict of primitive datatypes.
        movie = data.get('movie')
        business_partner = data.get('business_partner')

        # Perform the data validation.
        if not movie["title"]:
            raise serializers.ValidationError({
                'title': 'This field is required.'
            })
        if not movie["director"]:
            raise serializers.ValidationError({
                'director': 'This field is required.'
            })
        if not business_partner:
            raise serializers.ValidationError({
                'business_partner': 'This field is required.'
            })

        # Return the validated values. This will be available as
        # the `.validated_data` property.
        return {
            'movie': {
                "title": movie["title"],
                "director": movie["director"]
            },
            'business_partner': business_partner
        }

    def to_representation(self, instance):
        # list

        """
        Object instance -> Dict of primitive datatypes.
        """

        # We skip `to_representation` for `None` values so that fields do
        # not have to explicitly deal with that case.
        #
        # For related fields with `use_pk_only_optimization` we need to
        # resolve the pk value.
        return instance


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        exclude = ('movie',)


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
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
        business_partner = BusinessPartner.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email='',
        )
        return business_partner


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
