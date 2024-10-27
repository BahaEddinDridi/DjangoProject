from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # Exercise URLs
    path('exercises/', views.exercise_list, name='exercise_list'),
    path('exercises/add/', views.exercise_add, name='exercise_add'),
    path('exercises/edit/<int:exercise_id>/', views.exercise_edit, name='exercise_edit'),
    path('exercises/delete/<int:exercise_id>/', views.exercise_delete, name='exercise_delete'),
     path('exercise/<int:exercise_id>/', views.exercise_detail, name='exercise_detail'),

    # Training Plan URLs
    path('training_plans/', views.training_plan_list, name='training_plan_list'),
    path('training_plans/add/', views.training_plan_add, name='training_plan_add'),
    path('training_plans/edit/<int:plan_id>/', views.training_plan_edit, name='training_plan_edit'),
    path('training_plans/delete/<int:id>/', views.training_plan_delete, name='training_plan_delete'),
    path('training_plans/detail/<int:plan_id>/', views.training_plan_detail, name='training_plan_detail'),
    # Exercise Set URLs
    path('exercise_sets/add/<int:training_plan_id>/', views.exercise_set_add, name='exercise_set_add'),
    path('exercise_sets/edit/<int:id>/', views.exercise_set_edit, name='exercise_set_edit'),
    path('exercise_sets/delete/<int:id>/', views.exercise_set_delete, name='exercise_set_delete'),

    # Home
    path('', views.home, name='home'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)