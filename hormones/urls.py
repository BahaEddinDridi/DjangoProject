from django.urls import path

from .views import *
urlpatterns = [
    #hormones
    path('create/', create_hormone_level, name='create_hormone_level'),
    path('list/', list_hormone_levels, name='list_hormone_levels'),
    path('<int:id>/update/', update_hormone_level, name='update_hormone_level'),
    path('<int:id>/delete/', delete_hormone_level, name='delete_hormone_level'),
]