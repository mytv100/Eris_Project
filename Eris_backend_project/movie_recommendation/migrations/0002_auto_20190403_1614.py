# Generated by Django 2.1.7 on 2019-04-03 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie_recommendation', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='movie',
            unique_together={('title', 'director')},
        ),
    ]
