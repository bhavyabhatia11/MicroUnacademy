from sre_compile import isstring
from django.db import models
from django.core.validators import RegexValidator
from datetime import datetime

alphaSpaces = RegexValidator(r'^[a-zA-Z]+$','Only alphabets, letters and spaces are allowed in the Name.')
class Video(models.Model):
    uid = models.CharField(max_length=6, default= "")
    name = models.CharField(max_length=40, validators=[alphaSpaces])
    description = models.CharField(max_length=1024)
    url = models.URLField(max_length=200,blank=False, default='')
    likes = models. PositiveIntegerField(blank=False, default=0)
    created_at = models.DateTimeField (auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

 

class VideoVotes(models.Model):
    video_id = models.CharField(primary_key=True, max_length=6, unique=True)
    upvote = models. PositiveIntegerField(blank=False, default=0)
    downvote = models. PositiveIntegerField(blank=False, default=0)
    created_at = models.DateTimeField (auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
