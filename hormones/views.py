from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.shortcuts import get_object_or_404, render
# CREATE
def create_hormone_level(request):
    if request.method == "POST":
        form = HormoneLevelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_hormone_levels')
    else:
        form = HormoneLevelForm()
    return render(request, 'hormones/create.html', {'form': form})

# READ
def list_hormone_levels(request):
    # Récupère tous les niveaux hormonaux, sans filtrer par utilisateur
    levels = HormoneLevel.objects.all()
    return render(request, 'hormones/list.html', {'levels': levels})

# UPDATE
def update_hormone_level(request, id):
    level = get_object_or_404(HormoneLevel, id=id)
    if request.method == "POST":
        form = HormoneLevelForm(request.POST, instance=level)
        if form.is_valid():
            form.save()
            return redirect('list_hormone_levels')
    else:
        form = HormoneLevelForm(instance=level)
    return render(request, 'hormones/update_hormone_level.html', {'form': form})

# DELETE
def delete_hormone_level(request, id):
    level = get_object_or_404(HormoneLevel, id=id)
    if request.method == "POST":
        level.delete()
        return redirect('list_hormone_levels')
    return render(request, 'hormones/delete_hormone_level.html', {'level': level})
