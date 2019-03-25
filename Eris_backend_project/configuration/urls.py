"""configuration URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="졸업작품 프로젝트",
        default_version='version Alpha 0.0.1',
        description="Movie recommendation service as API",
        terms_of_service="https://github.com/mytv100/Eris_Project",
        # 이메일 형식 안맞으면 internal error 발생함
        contact=openapi.Contact(email="mytv7609@gmail.com"),
        license=openapi.License(name="NO Licence!!!!"),
    ),
    validators=['flex', 'ssv'],

    # public = True면 모든 API가 권한에 상관없이 보여짐
    # False 로 설정해서 권한이 없는 API는 볼 수 없게함
    # 영화 & 배우 데이터를 저장하는건 관리자만 가능함
    public=False,

    permission_classes=(permissions.AllowAny,),

)
urlpatterns = [
    # 관리자 페이지
    path('admin/', admin.site.urls),

    # react without ui & only data
    # path('swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    # swagger ui design 2개
    path('api/doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui', ),
    path('api/doc/redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # 영화 추천 앱
    path('movie-recommend/', include('movie_recommendation.urls'), name='product-recommend-app'),

    # rest_framework Authentication (로그인, 로그아웃 기능)
    path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]
