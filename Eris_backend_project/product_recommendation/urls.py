from django.urls import path

from product_recommendation import views

urlpatterns = [
    # view 를 여기에 등록
    path('asdf/', views.AsdfAPIView.as_view()),

]
