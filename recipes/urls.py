from django.urls import path
from . import views
from .views import (
    IngredientListView, IngredientCreateView, IngredientUpdateView, IngredientDeleteView, recipe_list
)

urlpatterns = [
    # Recipe URLs
    path('ingredients/', IngredientListView.as_view(), name='ingredient-list'),
    path('ingredients/new/', IngredientCreateView.as_view(), name='ingredient-create'),
    path('ingredients/edit/<int:pk>/', IngredientUpdateView.as_view(), name='update_ingredient'),
    path('ingredients/delete/<int:pk>/', IngredientDeleteView.as_view(), name='delete_ingredient'),
    path('add-recipe/', views.add_recipe, name='add_recipe'),
    path('', recipe_list, name='recipe_list'),
]
