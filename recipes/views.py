import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Recipe, Ingredient, RecipeIngredient
from .forms import IngredientForm
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage


NUTRITIONIX_APP_ID = 'cbb2dc89'
NUTRITIONIX_APP_KEY = '18a70d582a76cf3a6489927f68a32c9e'


@login_required
def add_ingredient(request):
    if request.method == "POST":
        image = request.FILES.get('image')
        name = request.POST.get('name')
        calories = request.POST.get('calories')
        protein = request.POST.get('protein')
        carbs = request.POST.get('carbs')
        fat = request.POST.get('fat')
        print(f"Received image: {image}")
        ingredient = Ingredient(
            name=name,
            calories=calories,
            protein=protein,
            carbs=carbs,
            fat=fat,
            image=image
        )
        ingredient.save()

        return redirect('/recipes/ingredients/') 

    return render(request, 'recipes/create_ingredient.html')

def ingredient_list(request):
    ingredients = Ingredient.objects.all()
    return render(request, 'recipes/ingredients_list.html', {'ingredients': ingredients})

def ingredient_detail(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)
    return render(request, 'recipes/ingredient_detail.html', {'ingredient': ingredient})

@login_required
def update_ingredient(request, id):
    ingredient = get_object_or_404(Ingredient, id=id)  

    if request.method == 'POST':
        ingredient.name = request.POST.get('name')
        ingredient.calories = request.POST.get('calories')
        ingredient.protein = request.POST.get('protein')
        ingredient.carbs = request.POST.get('carbs')
        ingredient.fat = request.POST.get('fat')
        if 'image' in request.FILES:
            ingredient.image = request.FILES['image']
        
        ingredient.save()  

        return redirect('ingredient-list')  

    return render(request, 'recipes/update_ingredient.html', {'ingredient': ingredient})

def ingredient_delete(request, id):
    ingredient = get_object_or_404(Ingredient, id=id)
    if request.method == 'POST':
        ingredient.delete()
        return redirect('ingredient-list')  
    return render(request, 'recipes/ingredients_list.html', {'ingredient': ingredient})


@login_required
def add_recipe(request):
    if request.method == "POST":
        image = request.FILES.get('image_url')
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        steps = request.POST.get('steps', '')
        prep_time = request.POST.get('prep_time', 0)
        cook_time = request.POST.get('cook_time', 0) 
        servings = request.POST.get('servings', 1)  
        recipe_type = request.POST.get('type', 'main_course')  
        ingredient_ids = request.POST.getlist('ingredient') 
        quantities = request.POST.getlist('quantity')  
        units = request.POST.getlist('unit')
        recipe = Recipe.objects.create(
            user=request.user,
            name=name,
            description=description,
            steps=steps,
            prep_time=prep_time,
            cook_time=cook_time,
            servings=servings,
            type=recipe_type,
            image=image
        )
        for ingredient_id, quantity, unit in zip(ingredient_ids, quantities, units):
            ingredient = Ingredient.objects.get(id=ingredient_id)
            quantity = float(quantity)
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                quantity=quantity,
                unit=unit
            )
        return redirect('recipe_list')
    ingredients = Ingredient.objects.all()
    return render(request, 'recipes/create_recipe.html', {'ingredients': ingredients})

@login_required
def update_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    
    if request.method == "POST":
        image = request.FILES.get('image_url', recipe.image)  
        
        name = request.POST.get('name', recipe.name)
        description = request.POST.get('description', recipe.description)
        steps = request.POST.get('steps', recipe.steps)
        prep_time = request.POST.get('prep_time', recipe.prep_time)
        cook_time = request.POST.get('cook_time', recipe.cook_time) 
        servings = request.POST.get('servings', recipe.servings)  
        recipe_type = request.POST.get('type', recipe.type)  
        ingredient_ids = request.POST.getlist('ingredient') 
        quantities = request.POST.getlist('quantity')  
        units = request.POST.getlist('unit')

        recipe.name = name
        recipe.description = description
        recipe.steps = steps
        recipe.prep_time = prep_time
        recipe.cook_time = cook_time
        recipe.servings = servings
        recipe.type = recipe_type
        recipe.image = image
        recipe.save()

       
        recipe.recipeingredient_set.all().delete()  
        for ingredient_id, quantity, unit in zip(ingredient_ids, quantities, units):
            ingredient = Ingredient.objects.get(id=ingredient_id)
            quantity = float(quantity)
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                quantity=quantity,
                unit=unit
            )

        return redirect('recipe_detail', id=recipe.id) 

    ingredients = Ingredient.objects.all()
    return render(request, 'recipes/update_recipe.html', {'recipe': recipe, 'ingredients': ingredients})

def recipe_detail(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

def recipe_list(request):
    recipes = Recipe.objects.all().order_by('-created_at')
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})

def recipe_delete(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    if request.method == 'POST':
        recipe.delete()
        return redirect('recipe_list')  
    return render(request, 'recipes/recipe_list.html', {'recipe': recipe})

@login_required
def user_recipe_list(request):
    current_user = request.user
    recipes = Recipe.objects.filter(user=current_user).order_by('-created_at')
    return render(request, 'recipes/my_recipe.html', {'recipes': recipes})

def add_ingredient_from_image(request):
    if request.method == 'POST' and request.FILES['image']:
        image_file = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        uploaded_file_url = fs.url(filename)

        url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
        headers = {
            'x-app-id': NUTRITIONIX_APP_ID,
            'x-app-key': NUTRITIONIX_APP_KEY,
            'Content-Type': 'application/json'
        }
        data = {
            "query": uploaded_file_url,  
            "timezone": "US/Eastern"
        }

        
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            nutrition_data = response.json().get('foods', [])
            if nutrition_data:
                food_item = nutrition_data[0]
                name = food_item.get('food_name')
                calories = food_item.get('nf_calories')
                protein = food_item.get('nf_protein')
                carbs = food_item.get('nf_total_carbohydrate')
                fat = food_item.get('nf_total_fat')

                ingredient = Ingredient(
                    name=name,
                    calories=calories,
                    protein=protein,
                    carbs=carbs,
                    fat=fat,
                    image=image_file                
                    )
                ingredient.save()

                return redirect('/recipes/ingredients/')  
            else:
                return render(request, 'recipes/errors.html', {'error': 'No food item found in the image.'})

        else:
            error_message = response.json().get('message', 'Unknown error occurred.')
            return render(request, 'recipes/errors.html', {'error': f'Error calling Nutritionix API: {error_message}'})

    return render(request, 'recipes/create_ingredient.html')