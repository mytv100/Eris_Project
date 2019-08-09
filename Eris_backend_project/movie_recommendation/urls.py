from django.urls import path
from rest_framework import routers

from movie_recommendation import views

simple_router = routers.SimpleRouter()

urlpatterns = [
    path('', views.InitData),
]

urlpatterns += simple_router.urls
