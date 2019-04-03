# Create your models here.
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.fields import CreationDateTimeField


# BusinessPartner table 안 생김 super&sub type
class BusinessPartner(User):
    """
    업체(추천 서비스를 직접 사용하는)
    proxy 모델로 만들어서 django의  auth_user 테이블을 그대로 사용한다.
    """

    class Meta:
        proxy = True


class Movie(models.Model):
    """
    영화 데이터
    title 제목
    genre 장르
    description 줄거리
    rate 평점
    running_time 영화 시간(분)
    created_at 이 객체가 생성된 시간
    director 감독
    movie_owner 이 영화를 가지고 있는 업체 (ManyToManyField 로 through 클래스로 구현)

    """
    title: str = models.CharField(
        max_length=128,
        null=False,
    )

    genre: str = models.CharField(
        max_length=128,
        null=False,
    )

    description: str = models.CharField(
        max_length=256,
        null=False,
    )

    rate: float = models.FloatField(
        null=False,
        default=None,
    )
    running_time: int = models.IntegerField(
        help_text="영화 시간, 분을 기준으로",
        default=0,
    )

    created_at: datetime = CreationDateTimeField()

    director: str = models.CharField(
        max_length=64,
        null=False,
    )

    movie_owner: BusinessPartner = models.ManyToManyField(
        BusinessPartner,
        through='BusinessPartnerMovie',
    )

    # class Meta:
    #     # pk 대신 조회에 사용할 키
    # 없어도 되겠는데..?
    #     # unique_index
    #     unique_together = (("title", "director"),)


class BusinessPartnerMovie(models.Model):
    """
    업체와 영화 사이의 M2M 클래스 ( 업체가 보유한 영화 )
    businessPartner 업체
    movie 영화
    """
    businessPartner: BusinessPartner = models.ForeignKey(
        BusinessPartner,
        on_delete=models.CASCADE
    )

    movie: Movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE
    )


class Actor(models.Model):
    """
    배우 데이터
    name 이름
    created_at 이 객체가 생성된 시간
    movie 배우가 출연한 영화 ( M2M field through 클래스로 구현)
    """
    name: str = models.CharField(
        max_length=64,
        null=False,
    )

    created_at: datetime = CreationDateTimeField()

    movie: Movie = models.ManyToManyField(
        Movie,
        through='ActorMovie',
        through_fields=('actor', 'movie'),
    )


class ActorMovie(models.Model):
    """
    배우와 영화 사이의 M2M 클래스 ( 영화에 출연한 배우)
    actor 배우
    movie 영화
    created_at 이 객체가 생성된 시간
    """
    actor: Actor = models.ForeignKey(
        Actor,
        on_delete=models.CASCADE
    )

    movie: Movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE
    )

    created_at: datetime = CreationDateTimeField()


class Customer(models.Model):
    """
    고객 데이터 (업체의 고객)
    gender 성별
    age 나이
    nickname 아이디, 닉네임 (저장할 때는 업체별로 회원이 겹칠 수 있으므로 businessPartner-nickname 으로 저장
    associated_bp 소속된 업체 (FK)
    movie 고객이 평가한 영화 ( M2M field through 클래스로 구현)
    created_at 이 객체가 생성된 시간
    """
    # booleanField 로 변경 가능
    gender: str = models.CharField(
        max_length=16,
        null=False,
        default="man",
    )

    age: int = models.IntegerField(
        null=False
    )

    nickname: str = models.CharField(
        max_length=64,
        null=False,
    )

    associated_bp: BusinessPartner = models.ForeignKey(
        to=BusinessPartner,
        on_delete=models.CASCADE
    )

    movie: Movie = models.ManyToManyField(
        Movie,
        through='CustomerMovie',
        through_fields=('customer', 'movie'),
    )

    created_at: datetime = CreationDateTimeField()


class CustomerMovie(models.Model):
    """
    고객과 영화 사이의 M2M 클래스 ( 고객이 평가한 영화 )
    customer 고객
    movie 영화
    rate 평점
    created_at 이 객체가 생성된 시간
    """
    customer: Customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )

    movie: Movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE
    )

    rate: float = models.FloatField(null=False, default=None)

    created_at: datetime = CreationDateTimeField()
