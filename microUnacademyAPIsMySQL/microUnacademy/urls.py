from django.urls import path 
from microUnacademy import views 
 
urlpatterns = [ 
   path(r'api/v1/videos', views.CreateVideo.as_view(), name='create_video'),
   path(r'api/v1/videos/filter', views.VideoDashboardList.as_view(), name='video_dashboard_list'),
   path(r'api/v1/videos/<int:video_id>', views.DeleteVideo.as_view(), name='delete_video'),
   path(r'api/v1/videos/delete', views.DeleteAllVideos.as_view(), name='delete_all_videos'),
   path(r'api/v1/videos/<int:video_id>/<str:vote_type>', views.SendVideoVotesToQueue.as_view(), name='video_votes'),
]