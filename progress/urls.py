from django.urls import path
from .views import *

urlpatterns = [
    path('', progress_list, name='progress_list'),
    path('add/', progress_add, name='progress_add'),
    path('edit/<int:progress_id>/', progress_edit, name='progress_edit'),
    path('delete/<int:progress_id>/', progress_delete, name='progress_delete'),
]
