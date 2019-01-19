# Create your views here.
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from product_recommendation.models import Asdf
from product_recommendation.serializers import AsdfSerializer


class AsdfViewSet(viewsets.ModelViewSet):
    queryset = Asdf.objects.all()
    serializer_class = AsdfSerializer


class AsdfAPIView(generics.ListCreateAPIView):
    queryset = Asdf.objects.all()
    serializer_class = AsdfSerializer


class LBHAPIView(APIView):

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)
