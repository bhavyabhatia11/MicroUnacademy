from rest_framework import serializers 
from microUnacademy.models import Video
from microUnacademy.models import VideoVotes
 
 
class VideoSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Video
        fields = (
                  'id',
                  'uid',
                  'name',
                  'description',
                  'likes',
                  'url',
                  'created_at',
                  'updated_at')


class VideoVoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoVotes
        fields = (
                  'video_id',
                  'upvote',
                  'downvote',
                  'created_at',
                  'updated_at')