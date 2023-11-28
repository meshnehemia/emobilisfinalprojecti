from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='intertainmenthome'),
    path('search/', views.searchdata, name='search'),
    path('videosales/', views.sales, name='videosales'),
    path('uploadVideo/', views.upload_video, name='uploadvideo'),
    path('updateVideo/<int:video_id>', views.update_video, name='updatevideo'),
    path('profile/', views.profile, name='videosprofile'),
    path('userprofile/<int:pk>', views.videouserprofile, name='videosuserprofile'),
    path('video/<int:pk>', views.videodetails, name='videodetails'),
    path('watchvideo/<int:pk>', views.videowatch, name='watch'),
    path('deletevideo/<int:pk>', views.deletevideo, name='deletevideo'),
]
