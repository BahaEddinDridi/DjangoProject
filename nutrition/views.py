from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.shortcuts import get_object_or_404, render

def create_Meal(request):
    if request.method == 'POST':
        form = MealForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)  # Ne pas enregistrer tout de suite
            meal.user = request.user  # Associer l'utilisateur connecté
            meal.save()  # Maintenant, sauvegarde l'objet
            return redirect('list_meal')  # Rediriger vers une autre vue après la création
    else:
        form = MealForm()
    
    return render(request, 'meals/create.html', {'form': form})
# READ
def list_Meal(request):
    # Récupère tous les niveaux hormonaux, sans filtrer par utilisateur
    meals = Meal.objects.all()
    return render(request, 'meals/list.html', {'meals': meals})

# UPDATE
def update_meal(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id)

    if request.method == 'POST':
        form = MealForm(request.POST, instance=meal)
        if form.is_valid():
            form.save()
            return redirect('list_meal')  # Redirige vers la liste des niveaux hormonaux
    else:
        form = MealForm(instance=meal)

    return render(request, 'meals/update.html', {'form': form,'meal': meal})
# DELETE

def delete_meal(request, meal_id):
    # Récupérer le niveau hormonal à supprimer
    meal = get_object_or_404(Meal, id=meal_id)
    
    # Supprimer le niveau hormonal
    meal.delete()
    
    # Rediriger vers la liste des niveaux hormonaux après suppression
    return redirect('list_meal')