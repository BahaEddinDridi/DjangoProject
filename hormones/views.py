from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.shortcuts import get_object_or_404, render

def create_hormone_level(request):
    if request.method == 'POST':
        form = HormoneLevelForm(request.POST)
        if form.is_valid():
            hormone_level = form.save(commit=False)  # Ne pas enregistrer tout de suite
            hormone_level.user = request.user  # Associer l'utilisateur connecté
            hormone_level.save()  # Maintenant, sauvegarde l'objet
            return redirect('list_hormone_levels')  # Rediriger vers une autre vue après la création
    else:
        form = HormoneLevelForm()
    
    return render(request, 'hormones/create.html', {'form': form})
# READ
def list_hormone_levels(request):
    # Récupère tous les niveaux hormonaux, sans filtrer par utilisateur
    levels = HormoneLevel.objects.all()
    return render(request, 'hormones/list.html', {'levels': levels})

# UPDATE
def update_hormone_level(request, level_id):
    hormone_level = get_object_or_404(HormoneLevel, id=level_id)

    if request.method == 'POST':
        form = HormoneLevelForm(request.POST, instance=hormone_level)
        if form.is_valid():
            form.save()
            return redirect('list_hormone_levels')  # Redirige vers la liste des niveaux hormonaux
    else:
        form = HormoneLevelForm(instance=hormone_level)

    return render(request, 'hormones/update.html', {'form': form,'hormone_level': hormone_level})
# DELETE

def delete_hormone_level(request, level_id):
    # Récupérer le niveau hormonal à supprimer
    level = get_object_or_404(HormoneLevel, id=level_id)
    
    # Supprimer le niveau hormonal
    level.delete()
    
    # Rediriger vers la liste des niveaux hormonaux après suppression
    return redirect('list_hormone_levels') 