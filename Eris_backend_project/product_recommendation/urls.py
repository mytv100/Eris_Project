from django.urls import path
from rest_framework import routers

from product_recommendation import views

router = routers.SimpleRouter()
router.register(r'movie', views.MovieAPIViewSet)

urlpatterns = [

    path('lbh/', views.LBHAPIView.as_view()),

]

urlpatterns += router.urls
