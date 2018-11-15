from rest_framework import serializers

from product_recommendation.models import Asdf


# django restframework  drf 방식의 직렬화 객체임 참고하셈
class AsdfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asdf
        fields = ['aaa', 'bbb']
