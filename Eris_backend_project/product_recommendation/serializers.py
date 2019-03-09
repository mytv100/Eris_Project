from typing import Any

from rest_framework import serializers

from product_recommendation.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    #movie_owner = serializers.IntegerField(help_text='업체의 PK', read_only=True)

    # def create(self, validated_data):
    #     self.validated_data['movie_owner'][0]
    #     return Movie()

    class Meta:
        model = Movie
        fields = "__all__"
        #exclude = ('movie_owner',)
        # example 주는 것 찾아보기
