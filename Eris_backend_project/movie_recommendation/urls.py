from django.urls import path, include
from rest_framework import routers

from movie_recommendation import views

simple_router = routers.SimpleRouter()
default_router = routers.DefaultRouter()

default_router.register(r'movie', views.MovieAPIViewSet)

urlpatterns = [
    # path('', views.initData),


]

urlpatterns += simple_router.urls
urlpatterns += default_router.urls
