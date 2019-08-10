from typing import Any

from django.db.models import Model
from rest_framework import serializers

from movie_recommendation.models import NewMovie, Genre, NewCustomer, BusinessPartner


class MovieSerializer(serializers.ModelSerializer):
    genres = serializers.ListField(child=serializers.CharField(max_length=64, default=''), )

    class Meta:
        model = NewMovie
        exclude = ('businessPartner', 'created_at', 'genre_set')

    def create(self, validated_data: Any):
        genre_list = validated_data.get('genres')
        movie = NewMovie.objects.create(title=validated_data.get('title'),
                                        description=validated_data.get('description'),
                                        released_date=validated_data.get('released_date'),
                                        )
        for i in genre_list:
            genre = Genre.objects.get(name=i)
            movie.genre_set.add(genre)

        return movie

    def update(self, instance: Model, validated_data: Any):
        NewMovie.objects.filter(id=instance.id). \
            update(title=validated_data.get('title'),
                   description=validated_data.get('description'),
                   released_date=validated_data.get('released_date'),
                   )

        instance.genre_set.clear()

        for i in validated_data.get('genres'):
            genre = Genre.objects.get(name=i)
            instance.genre_set.add(genre)
        return instance

    def to_internal_value(self, data: Any):
        genre_list = []
        if data.get('genres'):
            for i in data.get('genres'):
                genre_list.append(i)

        return {
            'id': data.get('id'),
            'title': data.get('title'),
            'description': data.get('description'),
            'rate': data.get('rate'),
            'votes': data.get('votes'),
            'released_date': data.get('released_date'),
            'genres': genre_list
        }

    def to_representation(self, instance: Any):
        genre_list = []
        for i in instance.genre_set.all():
            genre_list.append(i.name)

        return {
            'id': instance.id,
            'title': instance.title,
            'description': instance.description,
            'rate': instance.rate,
            'votes': instance.votes,
            'released_date': instance.released_date,
            'genre_set': genre_list,
        }


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewCustomer
        fields = ('gender', 'age', 'occupation')

        def create(self, validated_data: Any):
            businessPartner = BusinessPartner.objects.get(name='user1')
            customer = NewCustomer.objects. \
                create(gender=validated_data.get('gender'),
                       age=validated_data.get('age'),
                       occupation=validated_data.get('occupation'),
                       businessPartner=businessPartner
                       )
            return customer

        def update(self, instance: Model, validated_data: Any):
            NewCustomer.objects.filter(id=instance.id). \
                update(gender=validated_data.get('gender'),
                       age=validated_data.get('age'),
                       occupation=validated_data.get('occupation'),
                       )

            return instance

    def to_internal_value(self, data: Any):
        return {
            'gender': data.get('gender'),
            'age': data.get('age'),
            'occupation': data.get('occupation'),
        }

    def to_representation(self, instance: Any):
        return {
            'id': instance.id,
            'age': instance.age,
            'gender': instance.gender,
            'occupation': instance.occupation,
        }
