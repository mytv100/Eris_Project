# Generated by Django 2.1.7 on 2019-08-08 06:28

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('movie_recommendation', '0011_auto_20190803_1512'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('created_at', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='newmovie',
            name='action',
        ),
        migrations.RemoveField(
            model_name='newmovie',
            name='adventure',
        ),
        migrations.RemoveField(
            model_name='newmovie',
            name='animation',
        ),
        migrations.RemoveField(
            model_name='newmovie',
            name='children',
        ),
        migrations.RemoveField(
            model_name='newmovie',
            name='comedy',
        ),
        migrations.RemoveField(
            model_name='newmovie',
            name='crime',
        ),
        migrations.RemoveField(
            model_name='newmovie',
            name='documentary',
        ),
        migrations.RemoveField(
            model_name='newmovie',
            name='drama',
        ),
        migrations.RemoveField(
            model_name='newmovie',
            name='fantasy',
        ),
        migrations.RemoveField(
            model_name='newmovie',
            name='film_noir',
        ),
        migrations.RemoveField(
            model_name='newmovie',
            name='horror',
        ),
        migrations.RemoveField(
            model_name='newmovie',
            name='musical',
        ),
        migrations.RemoveField(
            model_name='newmovie',
            name='mystery',
        ),
        migrations.RemoveField(
            model_name='newmovie',
            name='romance',
        ),
        migrations.RemoveField(
            model_name='newmovie',
            name='sci_fi',
        ),
        migrations.RemoveField(
            model_name='newmovie',
            name='thriller',
        ),
        migrations.RemoveField(
            model_name='newmovie',
            name='unknown',
        ),
        migrations.RemoveField(
            model_name='newmovie',
            name='war',
        ),
        migrations.RemoveField(
            model_name='newmovie',
            name='western',
        ),
        migrations.AddField(
            model_name='newmovie',
            name='genre_set',
            field=models.ManyToManyField(to='movie_recommendation.Genre'),
        ),
    ]
