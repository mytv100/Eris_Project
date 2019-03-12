from typing import Any

from rest_framework import serializers

from movie_recommendation.models import Movie


# 영화가 이미 데이터베이스에 존재하는지 확인해서
# 존재하면 영화는 추가하지않고 연관데이터베이스만 되게
# example 주는 것 찾아보기
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"

        read_only_fields = ('movie_owner',)
        # exclude = ('movie_owner',)  해당 필드만 제외 됨 % fields = "__all__" 과 같이 사용 불가능
