# Generated by Django 4.1.7 on 2023-04-03 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='genres',
            field=models.ManyToManyField(to='watchlist_app.genre'),
        ),
    ]