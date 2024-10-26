from django.urls import path
from . import views
from .views import (
    update_ingredient, ingredient_delete,ingredient_detail, ingredient_list,
    recipe_list, add_ingredient, user_recipe_list, recipe_detail 
)

urlpatterns = [
    path('ingredients/', ingredient_list, name='ingredient-list'),
    path('ingredients/new/', add_ingredient, name='add_ingredient'),
    path('ingredients/update/<int:id>/', update_ingredient, name='update_ingredient'),
    path('ingredients/delete/<int:id>/', ingredient_delete, name='ingredient_delete'),
    path('ingredients/<int:pk>/', ingredient_detail, name='ingredient_detail'),
        # Recipe URLs
    path('add-recipe/', views.add_recipe, name='add_recipe'),
    path('', recipe_list, name='recipe_list'),
    path('my_recipes/', user_recipe_list, name='my_recipe'),
    path('recipes/<int:id>/', recipe_detail, name='recipe_detail'), 
     path('recipe/<int:id>/update/', views.update_recipe, name='recipe_update'),
    path('recipe/<int:id>/delete/', views.recipe_delete, name='recipe_delete'),
    path('add-ingredient-image/', views.add_ingredient_from_image, name='add_ingredient_from_image'),  

]
