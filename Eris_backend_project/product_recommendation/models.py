# Create your models here.
from django.db import models


class Asdf(models.Model):
    aaa = models.CharField(
        help_text='여기는 이 필드가 뭔지 주석 쓰는 부분 여기 작성하면 api문서가 알아서 문서화 해줌',
        max_length=100,
        null=False,
        default='비어있음'
    )

    bbb = models.CharField(
        help_text='여기는 이 필드가 뭔지 주석 쓰는 부분 여기 작성하면 api문서가 알아서 문서화 해줌22',
        max_length=100,
        null=False,
        default='비어있음'
    )

