from django.http.response import JsonResponse
from pymysql import NULL
from rest_framework.parsers import JSONParser 
from rest_framework import status
from microUnacademy.models import Video,VideoVotes
from microUnacademy.serializers import VideoSerializer, VideoVoteSerializer
from rest_framework.views import APIView
from django.http import HttpResponse
from django.views import generic
from django.http import Http404
import json
from microUnacademy.queues import push_video_votes_to_queue


# 1. Create Video:
# POST https://{{base_host}}/api/v1/videos/ 
# { 
#         "name": "test_video", 
#         "description": "test description", 
#         "url": "https://www.youtube.com/" 
# }
class CreateVideo(APIView):
    def post(self, request, *args, **kwargs):
        video_data = JSONParser().parse(request)
        video_serializer = VideoSerializer(data=video_data)

        if video_serializer.is_valid():
            video_serializer.save()
            video_votes_data = {
                "video_id": video_serializer.data['id'],
                "upvote": 0,
                "downvote": 0
            }
            video_votes_serializer = VideoVoteSerializer(data=video_votes_data)
            if video_votes_serializer.is_valid():
                video_votes_serializer.save()
    
            return JsonResponse({ "video_id" : video_serializer.data['id'] }, status=status.HTTP_201_CREATED) 
        return JsonResponse(video_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# 2. To get all videos
# GET https://{{base_host}}/api/v1/videos/filter?limit=5&offset=0
class VideoDashboardList(APIView):
    def get(self, request):

        limit  =  5
        offset =  0
        if request.GET['limit']:
            limit = int(request.GET['limit'])
        if request.GET['offset']:
            offset = int(request.GET['offset'])

        videos = Video.objects.all()[offset*limit : (offset+1)*limit]
        video_serializer = VideoSerializer(videos, many=True)

        response = {
            "count" : len(Video.objects.all()),
            "next" : request.build_absolute_uri('?')+ '?limit=' + str(limit) + '&offset=' + str(offset + 1),
            "previous" :  request.build_absolute_uri('?')+ '?limit=' + str(limit) + '&offset=' + str(offset - 1) if offset<0 else None,
            "results" : video_serializer.data
        }

        return JsonResponse(response, safe=False)


# 3. Delete a Video
# https://{{base_host}}/api/v1/videos/{video_id}
class DeleteVideo(APIView):
    def delete(self, request, video_id, format=None):
        try: 
            video = Video.objects.get(pk=video_id) 
        except Video.DoesNotExist: 
            return JsonResponse({'message': 'The video does not exist'}, status=status.HTTP_404_NOT_FOUND)

        video.delete() 
        return JsonResponse({'message': 'Video was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


# 4. Video Upvote
# PUT https://{{base_host}}/api/v1/videos/{video_id}/upvote
class UpvoteVideo(APIView):
    def put(self, request, video_id, format=None):
        try: 
            video = Video.objects.get(pk=video_id) 
        except Video.DoesNotExist: 
            return JsonResponse({'message': 'The video does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        print(Video.objects.all())

        return JsonResponse({'message': 'Video was upvoted successfully!'}, status=status.HTTP_204_NO_CONTENT)


# 5. Video Downvote
# PUT https://{{base_host}}/api/v1/videos/{video_id}/downvote
class DownvoteVideo(APIView):
    pass

# 6. Delete all videos
# DELETE https://{{base_host}}/api/v1/videos/delete
class DeleteAllVideos(APIView):
    def delete(self, request, *args, **kwargs):
        count = Video.objects.all().delete()
        return JsonResponse({'message': '{} Videos were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)



class SendVideoVotesToQueue(APIView):
    def get(self, request, video_id, vote_type):
        try: 
            video_votes = VideoVotes.objects.get(pk=video_id)
            video_votes_serializer = VideoVoteSerializer(video_votes)
            video_votes_data= video_votes_serializer.data
        except VideoVotes.DoesNotExist: 
            return JsonResponse({'message': 'The video does not exist'}, status=status.HTTP_404_NOT_FOUND)

        print(video_votes_data)
        if vote_type == 'upvote':
            video_votes_data['upvote'] += 1
        elif vote_type == 'downvote':
            video_votes_data['downvote'] += 1
        else:    
            return JsonResponse({'message': 'Invalid URL'}, status=status.HTTP_404_NOT_FOUND)
        push_video_votes_to_queue(video_votes_data)

        return JsonResponse({'message': '{} Videos were pushed to queue successfully!'}, status=status.HTTP_204_NO_CONTENT)



