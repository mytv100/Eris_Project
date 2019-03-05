from django.urls import path

from product_recommendation import views

urlpatterns = [
    path('asdf/', views.AsdfAPIView.as_view()),
    path('lbh/', views.LBHAPIView.as_view()),

]
