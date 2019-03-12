# Create your models here.
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.fields import CreationDateTimeField


class BusinessPartner(User):
    class Meta:
        proxy = True


# BusinessPartner table 안 생김 super&sub type

class Movie(models.Model):
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

    # rate: float = models.DecimalField(
    #     help_text="평점",
    #     default=0,
    #     decimal_places=2,
    #     max_digits=5,
    # )

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

    movie_owner: BusinessPartner = models.ManyToManyField(BusinessPartner)


class Actor(models.Model):
    name: str = models.CharField(
        max_length=64,
        null=False,
    )

    created_at: datetime = CreationDateTimeField(auto_now_add=True)

    movies: Movie = models.ManyToManyField(Movie)


class Customer(models.Model):
    gender: str = models.CharField(
        max_length=16,
        null=False,
        default="man",
        # booleanField 로 변경 가능
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

    movies: Movie = models.ManyToManyField(
        Movie,
        through='PersonalMovie',
        through_fields=('customer', 'movie'),
    )

    created_at: datetime = CreationDateTimeField()


class PersonalMovie(models.Model):
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
