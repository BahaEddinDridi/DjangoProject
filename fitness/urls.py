# fitness/urls.py

from django.urls import path
from .views import exercise_list, exercise_add, exercise_edit, exercise_delete
from . import views
urlpatterns = [
    path('', views.home, name='home'),  # Home page URL
    path('exercises/', exercise_list, name='exercise_list'),
    path('exercises/add/', exercise_add, name='exercise_add'),
    path('exercises/edit/<int:exercise_id>/', exercise_edit, name='exercise_edit'),
    path('exercises/delete/<int:exercise_id>/', exercise_delete, name='exercise_delete'),
]
