# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import TrainingPlan, ExerciseSet, Exercise
from .forms import TrainingPlanForm, ExerciseSetForm
from django.http import HttpResponse
from datetime import timedelta
from groq import Groq
import requests
from os import environ
import io  # For handling byte streams
from PIL import Image  # For image processing
import os
import time
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render
# Initialize Groq client
client = Groq(api_key='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') 

# Hugging Face API URL and headers for sentiment analysis
API_URL = "https://api-inference.huggingface.co/models/SamLowe/roberta-base-go_emotions"
headers = {"Authorization": "Bearer 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"}  # Replace with your actual token

# Function to query the Hugging Face model
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Exercise views
def exercise_list(request):
    exercise_list = Exercise.objects.all()  # Get all exercises
    paginator = Paginator(exercise_list, 6)  # Show 6 exercises per page

    page_number = request.GET.get('page')
    exercises = paginator.get_page(page_number)  # Get the exercises for the current page

    return render(request, 'exercise/list.html', {
        'exercises': exercises,
    })

def exercise_add(request):
    if request.method == 'POST':
        Exercise.objects.create(
            name=request.POST['name'],
            description=request.POST['description'],
            category=request.POST['category'],
            muscles_targeted=request.POST['muscles_targeted']
        )
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

# Training Plan views
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
            form.save()
            for exercise_set in plan.exercise_sets.all():
                sets = request.POST.get(f'sets_{exercise_set.id}')
                repetitions = request.POST.get(f'repetitions_{exercise_set.id}')
                rest_time = request.POST.get(f'rest_time_{exercise_set.id}')

                # Validate and update exercise sets
                if sets and repetitions and rest_time:
                    try:
                        exercise_set.sets = int(sets)
                        exercise_set.repetitions = int(repetitions)
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

def training_plan_delete(request, id):
    plan = get_object_or_404(TrainingPlan, id=id)
    if request.method == 'POST':
        plan.delete()
        return redirect('training_plan_list')
    return render(request, 'training_plan/training_plan_delete.html', {'plan': plan})

import random

def training_plan_detail(request, plan_id):
    plan = get_object_or_404(TrainingPlan, id=plan_id)
    exercise_sets_with_recommendations = []

    # Define a list of random emotions
    emotions = [
        "exciting", 
        "challenging", 
        "uplifting", 
        "thrilling", 
        "joyful", 
        "inspiring", 
        "exhilarating", 
        "fun", 
        "intense"
    ]

    for exercise_set in plan.exercise_sets.all():
        exercise = exercise_set.exercise
        
        # Get a random emotion from the list
        random_emotion = random.choice(emotions)
        
        # Get AI-generated suggestion for the exercise with emotion
        prompt = f"Provide a brief, 1 very short sentence recommendation or improvement tips for '{exercise.name}' with a focus on how it feels {random_emotion}."
        
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )
        
        recommendations = chat_completion.choices[0].message.content
        sentiment_output = query({"inputs": recommendations})
        
        # Extract sentiment label and score
        sentiment_label, sentiment_score = None, None
        
        if sentiment_output and isinstance(sentiment_output, list) and len(sentiment_output) > 0:
            first_sentiment_list = sentiment_output[0]
            if isinstance(first_sentiment_list, list) and len(first_sentiment_list) > 0:
                first_sentiment = first_sentiment_list[0]
                if isinstance(first_sentiment, dict):
                    sentiment_label = first_sentiment.get('label')
                    sentiment_score = first_sentiment.get('score')

        exercise_sets_with_recommendations.append({
            'exercise_set': exercise_set,
            'recommendations': recommendations,
            'sentiment_label': sentiment_label,
            'sentiment_score': sentiment_score,
        })

    return render(request, 'training_plan/training_plan_detail.html', {
        'plan': plan,
        'exercise_sets_with_recommendations': exercise_sets_with_recommendations
    })

# Exercise Set views
def exercise_set_add(request, training_plan_id):
    training_plan = get_object_or_404(TrainingPlan, id=training_plan_id)
    if request.method == 'POST':
        form = ExerciseSetForm(request.POST)
        if form.is_valid():
            exercise_set = form.save(commit=False)
            exercise_set.training_plan = training_plan
            exercise_set.save()
            return redirect('training_plan_edit', plan_id=training_plan.id)
    else:
        form = ExerciseSetForm()
    return render(request, 'exercise_set/exercise_set_add.html', {'form': form, 'training_plan': training_plan})

def exercise_set_edit(request, id):
    exercise_set = get_object_or_404(ExerciseSet, id=id)
    if request.method == 'POST':
        form = ExerciseSetForm(request.POST, instance=exercise_set)
        if form.is_valid():
            form.save()
            return redirect('training_plan_edit', id=exercise_set.training_plan.id)
    else:
        form = ExerciseSetForm(instance=exercise_set)
    return render(request, 'exercise_set/exercise_set_edit.html', {'form': form, 'set': exercise_set})

def exercise_set_delete(request, id):
    exercise_set = get_object_or_404(ExerciseSet, id=id)
    training_plan_id = exercise_set.training_plan.id
    if request.method == 'POST':
        exercise_set.delete()
        return redirect('training_plan_edit', id=training_plan_id)
    return render(request, 'exercise_set/exercise_set_confirm_delete.html', {'exercise_set': exercise_set})


import logging

# Set up logging
logger = logging.getLogger(__name__)

# Define the image querying function
def query_image(prompt):
    IMAGE_API_URL = "https://api-inference.huggingface.co/models/stable-diffusion-v1-5/stable-diffusion-v1-5"
    MAX_RETRIES = 3  # Number of retries for 503 errors

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(IMAGE_API_URL, headers=headers, json={"inputs": prompt})
            response.raise_for_status()  # Raise an error for HTTP errors

            # If the API returns JSON instead of binary image data, handle that
            if response.headers.get("Content-Type") == "application/json":
                logger.error(f"Received JSON response: {response.json()}")
                return None  # Or handle the error accordingly

            return response.content  # Return raw bytes for images
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 503 and attempt < MAX_RETRIES - 1:
                logger.warning(f"503 error, retrying in 2 seconds... (Attempt {attempt + 1})")
                time.sleep(2)  # Wait before retrying
                continue  # Retry the request
            else:
                logger.error(f"HTTP error occurred: {http_err}")
                return None  # Handle other errors gracefully
        except requests.exceptions.RequestException as e:
            logger.error(f"Error during image query: {e}")
            return None  # Handle errors gracefully

def exercise_detail(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)

    # Generate recommendations for the exercise
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": f"Provide a brief, 3 short sentence recommendations or tips for improving on '{exercise.name}'."}],
        model="gemma-7b-it",
    )
    recommendations = chat_completion.choices[0].message.content

    # Define the media directory and ensure it exists
    media_root = getattr(settings, 'MEDIA_ROOT', 'media')
    image_dir = os.path.join(media_root, 'exercise_images')
    os.makedirs(image_dir, exist_ok=True)

    # Define the image path on disk and URL path
    image_filename = f"{exercise_id}_{exercise.name.replace(' ', '_')}.png"
    image_save_path = os.path.join(image_dir, image_filename)  # Save path in the file system
    image_url_path = settings.MEDIA_URL + 'exercise_images/' + image_filename  # URL path for template rendering

    # Check if the image already exists
    image_url = None

    if os.path.exists(image_save_path):
        image_url = image_url_path
    else:
        # Generate an image using the new image query function
        prompt = f"An illustration of a {exercise.name} being performed."
        image_bytes = query_image(prompt)

        if image_bytes:
            try:
                # Convert the image bytes to a displayable format
                image = Image.open(io.BytesIO(image_bytes))
                image.save(image_save_path)  # Save the image to a file
                image_url = image_url_path  # URL to access the saved image
            except Exception as e:
                logger.error(f"Error opening image: {e}")
                image_url = None  # No image available if there was an error
        else:
            logger.error("No image bytes returned from the API.")
            image_url = None  # Fallback to no image if query failed

    return render(request, 'exercise/detail.html', {
        'exercise': exercise,
        'recommendations': recommendations,
        'image_url': image_url,
    })

def home(request):
    return render(request, 'base_template/home.html')