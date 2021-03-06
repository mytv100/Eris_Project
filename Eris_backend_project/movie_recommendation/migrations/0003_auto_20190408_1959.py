# Generated by Django 2.1.7 on 2019-04-08 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_recommendation', '0002_auto_20190408_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='genre',
            field=models.CharField(default='genre', help_text="영화 장르, ',' 를 기준으로 분류", max_length=128),
        ),
        migrations.AlterField(
            model_name='movie',
            name='rate',
            field=models.FloatField(default=0.0, help_text='영화 평점'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='running_time',
            field=models.IntegerField(default=0, help_text='영화 시간, 분을 기준으로'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='votes',
            field=models.IntegerField(default=0, help_text='퍙점 투표수'),
        ),
    ]
