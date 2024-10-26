# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import TrainingPlan, ExerciseSet, Exercise
from .forms import TrainingPlanForm, ExerciseSetForm
from django.views import View
from django.http import HttpResponse
from datetime import timedelta
from groq import Groq
from os import environ

####" AI/ML Model"
client = Groq(api_key='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') 
# Exercises
def exercise_list(request):
    exercises = Exercise.objects.all()
    print("exercises") # This will print the exercises in the console
    return render(request, 'exercise/list.html', {'exercises': exercises})


def exercise_add(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        category = request.POST['category']
        muscles_targeted = request.POST['muscles_targeted']
        Exercise.objects.create(name=name, description=description, category=category, muscles_targeted=muscles_targeted)
        return redirect('exercise_list')
    return render(request, 'exercise/add.html')


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


def exercise_delete(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    if request.method == 'POST':
        exercise.delete()
        return redirect('exercise_list')
    return render(request, 'exercise/delete.html', {'exercise': exercise})


# Training Plan 
def training_plan_list(request):
    plans = TrainingPlan.objects.filter(user=request.user)
    return render(request, 'training_plan/training_plan_list.html', {'plans': plans})


def training_plan_add(request):
    if request.method == 'POST':
        form = TrainingPlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.user = request.user
            plan.save()
            return redirect('training_plan_list')
    else:
        form = TrainingPlanForm()
    return render(request, 'training_plan/training_plan_add.html', {'form': form})


def training_plan_edit(request, plan_id):
    plan = get_object_or_404(TrainingPlan, id=plan_id)
    
    if request.method == "POST":
        form = TrainingPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()  # Save the main form instance
            
            # Process exercise sets
            for exercise_set in plan.exercise_sets.all():
                sets = request.POST.get(f'sets_{exercise_set.id}')
                repetitions = request.POST.get(f'repetitions_{exercise_set.id}')
                rest_time = request.POST.get(f'rest_time_{exercise_set.id}')

                # Debug output to see received values
                print(f"ID: {exercise_set.id}, Sets: {sets}, Repetitions: {repetitions}, Rest Time: {rest_time}")

                if sets and repetitions and rest_time:  # Ensure all fields are present
                    try:
                        exercise_set.sets = int(sets)
                        exercise_set.repetitions = int(repetitions)
                        # Convert rest_time from seconds to timedelta
                        exercise_set.rest_time = timedelta(seconds=int(rest_time))
                        exercise_set.save()
                    except ValueError as ve:
                        print(f"Value error for ExerciseSet ID {exercise_set.id}: {ve}")
                else:
                    print(f"Error: Missing data for ExerciseSet ID {exercise_set.id}")

            return redirect('training_plan_detail', plan_id=plan.id)

    else:
        form = TrainingPlanForm(instance=plan)

    return render(request, 'training_plan/training_plan_edit.html', {'form': form, 'plan': plan})


def training_plan_delete(request, id):  # Changed 'plan_id' to 'id'
    plan = get_object_or_404(TrainingPlan, id=id)
    if request.method == 'POST':
        plan.delete()
        return redirect('training_plan_list')
    return render(request, 'training_plan/training_plan_delete.html', {'plan': plan})




def training_plan_detail(request, plan_id):
    # Get the training plan by ID
    plan = get_object_or_404(TrainingPlan, id=plan_id)
    exercise_sets_with_recommendations = []

    # Fetch AI recommendations for each exercise in the plan
    for exercise_set in plan.exercise_sets.all():
        exercise = exercise_set.exercise
        
        # Get a brief AI-generated suggestion for each exercise
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Provide a brief, 1 short sentence recommendation or improvement tips for '{exercise.name}'."
                }
            ],
            model="llama3-8b-8192",
        )
        
        # Extract the recommendation text from the response
        recommendations = chat_completion.choices[0].message.content
        exercise_sets_with_recommendations.append({
            'exercise_set': exercise_set,
            'recommendations': recommendations
        })

    return render(request, 'training_plan/training_plan_detail.html', {
        'plan': plan,
        'exercise_sets_with_recommendations': exercise_sets_with_recommendations
    })

# Exercise Set
def exercise_set_add(request, training_plan_id):
    training_plan = get_object_or_404(TrainingPlan, id=training_plan_id)
    if request.method == 'POST':
        form = ExerciseSetForm(request.POST)
        if form.is_valid():
            exercise_set = form.save(commit=False)
            exercise_set.training_plan = training_plan  # Link to the training plan
            exercise_set.save()  # Save the exercise set
            return redirect('training_plan_edit', plan_id=training_plan.id)  # Correct redirection
    else:
        form = ExerciseSetForm()
    return render(request, 'exercise_set/exercise_set_add.html', {'form': form, 'training_plan': training_plan})


def exercise_set_edit(request, id):
    exercise_set = get_object_or_404(ExerciseSet, id=id)
    if request.method == 'POST':
        form = ExerciseSetForm(request.POST, instance=exercise_set)
        if form.is_valid():
            form.save()
            return redirect('training_plan/training_plan_edit', id=exercise_set.training_plan.id)
    else:
        form = ExerciseSetForm(instance=exercise_set)
    return render(request, 'exercise_set/exercise_set_edit.html', {'form': form, 'set': exercise_set})


def exercise_set_delete(request, id):
    exercise_set = get_object_or_404(ExerciseSet, id=id)
    training_plan_id = exercise_set.training_plan.id
    if request.method == 'POST':
        exercise_set.delete()
        return redirect('training_plan/training_plan_edit', id=training_plan_id)
    return render(request, 'exercise_set/exercise_set_confirm_delete.html', {'exercise_set': exercise_set})



# Exercise detail view with recommendations
def exercise_detail(request, exercise_id):
    # Fetch the exercise from the database
    exercise = get_object_or_404(Exercise, id=exercise_id)
    
    # Fetch recommendations from the Groq API
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Provide a brief, 3 short sentence Recommended similar exercises or tips for improving on '{exercise.name}'."
            }
        ],
        model="gemma-7b-it",
    )
    
    # Get the recommendation text from the response
    recommendations = chat_completion.choices[0].message.content

    # Pass exercise and recommendations to the template
    return render(request, 'exercise/detail.html', {'exercise': exercise, 'recommendations': recommendations})

def home(request):
    return render(request, 'base_template/home.html')