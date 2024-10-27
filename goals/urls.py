from django.urls import path
from .views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.goal_list, name='goal_list'),
    path('add/', views.goal_add, name='goal_add'),
    path('edit/<int:goal_id>/', views.goal_edit, name='goal_edit'),
    path('delete/<int:goal_id>/', views.goal_delete, name='goal_delete'),
    path('progress/<int:goal_id>/', views.progress_list, name='progress_list'),
    path('image/<int:goal_id>/', goal_image, name='goal_image'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
