# Create your views here.

from rest_framework import generics
from rest_framework import viewsets

from product_recommendation.models import Asdf
from product_recommendation.serializers import AsdfSerializer


class AsdfViewSet(viewsets.ModelViewSet):
    queryset = Asdf.objects.all()
    serializer_class = AsdfSerializer


class AsdfAPIView(generics.ListCreateAPIView):
    queryset = Asdf.objects.all()
    serializer_class = AsdfSerializer
