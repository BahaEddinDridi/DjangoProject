from django.urls import path
from .views import *

urlpatterns = [
    path('create/', create_Event, name='create_event'),
    path('list/', list_Event, name='list_event'),
    path('<int:event_id>/update/', update_event, name='update_event'),
    path('delete/<int:event_id>/', delete_event, name='delete_event'),
    path('events/<int:event_id>/detail/', detail_event, name='detail_event'),
]