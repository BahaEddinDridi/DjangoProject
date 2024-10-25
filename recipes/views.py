from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Recipe, Ingredient, RecipeIngredient
from .forms import IngredientForm
from django.contrib.auth.decorators import login_required

# List ingredients
class IngredientListView(ListView):
    model = Ingredient
    template_name = 'recipes/ingredients_list.html'
    context_object_name = 'ingredients'

# Create new ingredient
class IngredientCreateView(CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'recipes/ingredient_form.html'
    success_url = '/recipes/ingredients/'

# Update ingredient
class IngredientUpdateView(UpdateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'recipes/ingredient_form.html'
    success_url = '/recipes/ingredients/'

# Delete ingredient
class IngredientDeleteView(DeleteView):
    model = Ingredient
    template_name = 'recipes/ingredient_confirm_delete.html'
    success_url = '/recipes/ingredients/'

@login_required
def add_recipe(request):
    if request.method == "POST":
        # Retrieve the data from the form submission
        name = request.POST.get('name')
        description = request.POST.get('description', '')  # Optional description
        steps = request.POST.get('steps', '')  # Instructions for the recipe
        prep_time = request.POST.get('prep_time', 0)  # Preparation time
        cook_time = request.POST.get('cook_time', 0)  # Cooking time
        servings = request.POST.get('servings', 1)  # Number of servings
        recipe_type = request.POST.get('type', 'main_course')  # Type of recipe
        
        # Retrieve ingredient data
        ingredient_ids = request.POST.getlist('ingredient')  # Multiple ingredients
        quantities = request.POST.getlist('quantity')  # Corresponding quantities
        units = request.POST.getlist('unit')

        # Create the Recipe instance
        recipe = Recipe.objects.create(
            user=request.user,
            name=name,
            description=description,
            steps=steps,
            prep_time=prep_time,
            cook_time=cook_time,
            servings=servings,
            type=recipe_type
        )

        # Create RecipeIngredient instances
        for ingredient_id, quantity, unit in zip(ingredient_ids, quantities, units):
            ingredient = Ingredient.objects.get(id=ingredient_id)
            quantity = float(quantity)
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                quantity=quantity,
                unit=unit
            )

        return redirect('recipe_list')  # Redirect to the list of recipes

    ingredients = Ingredient.objects.all()
    return render(request, 'recipes/create_recipe.html', {'ingredients': ingredients})


def recipe_list(request):
    recipes = Recipe.objects.all().order_by('-created_at')
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})