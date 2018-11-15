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
        title="불화의 여신 Eris와 함께하는 신나는 졸업작품 프로젝트",
        default_version='version Alpha 0.0.1 버전은 자유롭게 작성되는 문자열',
        description="여기는 문서 상세 설명 넣는 부분 ",
        terms_of_service="https://github.com/mytv100/Eris_Project",
        # 여기 너 이메일 적으셈  이메일 형식 안맞으면 internal error 떠서 내꺼 넣어놓음
        contact=openapi.Contact(email="KimSoungRyoul@gmail.com"),
        license=openapi.License(name="NO Licence!!!!"),
    ),
    validators=['flex', 'ssv'],
    public=True,
    permission_classes=(permissions.AllowAny,),

)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui', ),
    path('api/doc/redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('product-recommend/', include('product_recommendation.urls'), name='product-recommend-app'),

]
