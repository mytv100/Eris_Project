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

# 업체 회원 가입 /signup/
router.register(r'signup', views.CreateBusinessPartnerAPIViewSet)

# 데이터 초기화
router.register(r'init', views.InitViewSet)

urlpatterns = [
]

urlpatterns += router.urls
