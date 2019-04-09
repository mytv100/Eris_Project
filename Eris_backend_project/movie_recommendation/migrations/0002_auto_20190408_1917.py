# Generated by Django 2.1.7 on 2019-04-08 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_recommendation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='director',
            field=models.CharField(help_text="감독명, ',' 를 기준으로 분류", max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='genre',
            field=models.CharField(help_text="영화 장르, ',' 를 기준으로 분류", max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='rate',
            field=models.FloatField(default=0.0, help_text='영화 평점', null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='running_time',
            field=models.IntegerField(default=0, help_text='영화 시간, 분을 기준으로', null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='votes',
            field=models.IntegerField(default=0, help_text='퍙점 투표수', null=True),
        ),
    ]
