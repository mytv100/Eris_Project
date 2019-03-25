from django.urls import path
from rest_framework import routers

from movie_recommendation import views

router = routers.SimpleRouter()

# 고객 - 영화 M2M
# 각 고객의 각 영화 평점 /customerMovie/
# 각 고객에 대한 영화 추천 리스트 /customerMovie/movie_list/
router.register(r'customerMovie', views.CustomerMovieAPIViewSet)

# 업체 - 영화 M2M
# 각 업체별 소유한 영화 /businessPartnerMovie
router.register(r'businessPartnerMovie', views.BusinessPartnerMovieAPIViewSet)

# 배우 - 영화
# 영화에 출연하는 배우들 /actorMovie/
router.register(r'actorMovie', views.ActorMovieAPIViewSet)

# 고객
# 업체의 고객 정보 /customer/
router.register(r'customer', views.CustomerAPIViewSet)


urlpatterns = [
    # 회원가입 -> 바로 로그인되서 /api/doc/로 넘어감
    path('join/', views.signup, name='join'),
]

urlpatterns += router.urls
