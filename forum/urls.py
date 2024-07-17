from django.contrib import admin
from django.urls import path

from .views import *


urlpatterns = [
    path('forum/', TopicListView.as_view(), name='forum-index'),
    path('forum/topic/add/', TopicCreateView.as_view(), name='topic-add'),
    path('forum/topic/<int:pk>/', TopicDetailView.as_view(), name='topic-detail'),
    path('forum/topic/<int:pk>/update/', TopicUpdateView.as_view(), name='topic-update'),
    path('forum/topic/<int:pk>/delete/', TopicDeleteView.as_view(), name='topic-delete'),
    path('forum/topic/<int:pk>/newpost/', PostCreateView.as_view(), name='post-create'),
    path('forum/post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('forum/post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('forum/post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    
]
    





    

