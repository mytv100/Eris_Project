# Generated by Django 2.1.7 on 2019-04-16 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movie_recommendation', '0005_auto_20190408_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customermovie',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='movie_recommendation.Customer'),
        ),
    ]