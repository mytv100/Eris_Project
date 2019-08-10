from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers

from movie_recommendation import views

simple_router = routers.SimpleRouter()
default_router = routers.DefaultRouter()

default_router.register(r'movie', views.MovieAPIViewSet)
default_router.register(r'customer', views.CustomerAPIViewSet)

urlpatterns = [
    # path('init', views.initData),
    url(r'^recommend/(?P<customer_id>\d+)/(?P<movie_id>\d+)/?', views.MovieRecommend),
]

urlpatterns += simple_router.urls
urlpatterns += default_router.urls
