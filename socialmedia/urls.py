from django.contrib import admin
from django.urls import path
from socialmedia import views

urlpatterns = [
    path('', views.home, name='home'),
    path('mychats/<str:type>/', views.Mychats, name='mychats'),
    path('getmychats/<str:type>/', views.getchats, name='chatsget'),
    path('getgroupchats/<str:code>/', views.groupchat, name='groupchatsget'),
    path('groupchatscrean/<str:code>/', views.groupchatscreen, name='groupchatscreen'),
    path('getpersonalchats/<int:pk>/', views.loadpersonalchats, name='startchat'),
    path('deletepmessage/<int:pkmessage>/<int:pkroom>/', views.deletepmessage, name='deletemessage'),
    path('deletegroupmessage/<str:code>/<int:pk>/', views.deletegroupmessage, name='deletegroupmessage'),
    path('usersandgroups/', views.getusernames, name='usgpnames'),
    path('creategroup/', views.creategroup, name='creategroup'),

    path('login/', views.loginPage, name='login'),
    path('chatscreem/<int:pk>/', views.chatscreen, name='chatwithme'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('navbar/', views.navbar, name='navbar'),
    path('room/<str:pk>/', views.room, name='room'),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),
    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<str:pk>', views.updateRoom, name='update-room'),
    path('delete-room/<str:pk>', views.deleteRoom, name='delete-room'),
    path('delete-message/<str:pk>', views.deleteMessage, name='delete-message'),
    path('update-user/', views.updateUser, name='update-user'),
    path('topics/', views.topicsPage, name='topics'),
    path('activity/', views.activityPage, name='activity'),
    path('chatting/<int:pk>', views.chatting, name='searchchats'),
]
