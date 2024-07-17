from django.urls import path
from  . import views
from .views import *

urlpatterns = [
    
    path('innovations/submit/', views.submit, name='submit'),
    path('innovations/submit/submit_innovation/', views.submit_innovation, name='submit_innovation'),
    path('innovations/', views.innovations, name='innovations'),
    path('innovations/innov_details/<int:id>', views.innov_details, name='innov_details'),
    path('innovations/search/', InnovationSearchList.as_view() ,name='search'),
    path('innovations/innov_details/<int:pk>/update/', InnovationUpdateView.as_view(), name='innovation-update'),
    path('innovations/innov_details/<int:pk>/delete/', InnovationDeleteView.as_view(), name='innovation-delete'),


]
