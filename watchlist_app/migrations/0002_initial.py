# Generated by Django 4.1.1 on 2023-04-08 12:44

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('watchlist_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'genre_list',
            },
        ),
        migrations.CreateModel(
            name='StreamingPlatform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('about', models.CharField(max_length=200)),
                ('website', models.URLField(max_length=100)),
            ],
            options={
                'db_table': 'streaming_platform',
            },
        ),
        migrations.CreateModel(
            name='WatchList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('storyline', models.CharField(max_length=300)),
                ('year', models.IntegerField()),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('genres', models.ManyToManyField(to='watchlist_app.genre')),
                ('platform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='WatchList', to='watchlist_app.streamingplatform')),
            ],
            options={
                'db_table': 'watch_list',
            },
        ),
        migrations.CreateModel(
            name='TicketSale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('amount', models.PositiveIntegerField()),
                ('purchase_time', models.DateTimeField(auto_now_add=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='watchlist_app.watchlist')),
            ],
            options={
                'db_table': 'ticket_sales',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('description', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('watchlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='all_review', to='watchlist_app.watchlist')),
            ],
            options={
                'db_table': 'all_review',
            },
        ),
    ]