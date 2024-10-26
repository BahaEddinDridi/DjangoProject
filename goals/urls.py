# goals/urls.py

from django.urls import path
from .views import *
from . import views
urlpatterns = [
    path('', views.goal_list, name='goal_list'),
    path('add/', views.goal_add, name='goal_add'),
    path('edit/<int:goal_id>/', views.goal_edit, name='goal_edit'),
    path('delete/<int:goal_id>/', views.goal_delete, name='goal_delete'),
    path('progress/<int:goal_id>/', views.progress_list, name='progress_list'),
]
