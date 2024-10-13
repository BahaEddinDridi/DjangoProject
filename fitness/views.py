# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Exercise
from django.views import View

# List all exercises
def exercise_list(request):
    exercises = Exercise.objects.all()
    print("exercises") # This will print the exercises in the console
    return render(request, 'exercise/list.html', {'exercises': exercises})

# Add new exercise
def exercise_add(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        category = request.POST['category']
        muscles_targeted = request.POST['muscles_targeted']
        Exercise.objects.create(name=name, description=description, category=category, muscles_targeted=muscles_targeted)
        return redirect('exercise_list')
    return render(request, 'exercise/add.html')

# Edit existing exercise
def exercise_edit(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    if request.method == 'POST':
        exercise.name = request.POST['name']
        exercise.description = request.POST['description']
        exercise.category = request.POST['category']
        exercise.muscles_targeted = request.POST['muscles_targeted']
        exercise.save()
        return redirect('exercise_list')
    return render(request, 'exercise/edit.html', {'exercise': exercise})

# Delete exercise
def exercise_delete(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    if request.method == 'POST':
        exercise.delete()
        return redirect('exercise_list')
    return render(request, 'exercise/delete.html', {'exercise': exercise})

def home(request):
    return render(request, 'base/home.html')