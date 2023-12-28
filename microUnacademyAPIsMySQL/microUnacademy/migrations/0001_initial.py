# Generated by Django 4.0.6 on 2022-07-15 05:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(default='', max_length=6)),
                ('name', models.CharField(max_length=40, validators=[django.core.validators.RegexValidator('^[a-zA-Z]+$', 'Only alphabets, letters and spaces are allowed in the Name.')])),
                ('description', models.CharField(max_length=1024)),
                ('url', models.URLField(default='')),
                ('likes', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='VideoVotes',
            fields=[
                ('video_id', models.CharField(max_length=6, primary_key=True, serialize=False, unique=True)),
                ('upvote', models.PositiveIntegerField(default=0)),
                ('downvote', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
