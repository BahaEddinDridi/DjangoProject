# fitness/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Goal
from django.views import View

# Liste des objectifs
def goal_list(request):
    goals = Goal.objects.all()
    return render(request, 'goals/list.html', {'goals': goals})


# Ajouter un nouvel objectif
def goal_add(request):
    if request.method == 'POST':
        goal_type = request.POST['goal_type']
        target_value = request.POST['target_value']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        Goal.objects.create(
            goal_type=goal_type,
            target_value=target_value,
            start_date=start_date,
            end_date=end_date
        )
        return redirect('goal_list')

    return render(request, 'goals/add.html')

# Modifier un objectif existant
def goal_edit(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id)
    if request.method == 'POST':
        goal.goal_type = request.POST['goal_type']
        goal.target_value = request.POST['target_value']
        goal.start_date = request.POST['start_date']
        goal.end_date = request.POST['end_date']
        goal.save()
        return redirect('goal_list')
    return render(request, 'goals/edit.html', {'goal': goal})

# Supprimer un objectif
def goal_delete(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id)
    if request.method == 'POST':
        goal.delete()
        return redirect('goal_list')
    return render(request, 'goals/delete.html', {'goal': goal})


