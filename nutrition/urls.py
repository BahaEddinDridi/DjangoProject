from django.urls import path

from .views import *
urlpatterns = [
    path('create/', create_Meal, name='create_meal'),
    path('list/', list_Meal, name='list_meal'),
    path('<int:meal_id>/update/', update_meal, name='update_meal'),
    path('delete/<int:meal_id>/', delete_meal, name='delete_meal'),
]