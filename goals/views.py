import os
import io
import requests
import logging
import time
from django.shortcuts import render, redirect, get_object_or_404
from .models import Goal
from django.contrib.auth.decorators import login_required
from groq import Groq
from PIL import Image
from django.conf import settings

# Initialize logging
logger = logging.getLogger(__name__)

# Initialize Groq client
client = Groq(api_key="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")

# Hugging Face API URL and headers
API_URL = "https://api-inference.huggingface.co/models/stable-diffusion-v1-5/stable-diffusion-v1-5"
headers = {"Authorization": "Bearer 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"}

# Function to send request to the Hugging Face API with retry logic
def query(payload):
    max_retries = 5  # Maximum number of retries
    for attempt in range(max_retries):
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.content
        elif response.status_code == 503:
            # Log the error and wait before retrying
            logger.error(f"API request failed with status code {response.status_code}: {response.text}")
            estimated_time = response.json().get("estimated_time", 5)  # Default to 5 seconds if not provided
            logger.info(f"Retrying in {estimated_time} seconds... (Attempt {attempt + 1}/{max_retries})")
            time.sleep(estimated_time)  # Wait for the estimated time before retrying
        else:
            logger.error(f"API request failed with status code {response.status_code}: {response.text}")
            break  # Break out of the loop for other errors
    return None  # Return None if all attempts fail

# Generate image using the description
def generate_image(description):
    image_bytes = query({"inputs": description})
    if image_bytes is None:
        return None  # Return None if the query failed after retries
    try:
        # Try opening the image
        return Image.open(io.BytesIO(image_bytes))
    except Exception as e:
        logger.error(f"Error while opening image: {e}")
        return None  # Return None if the image cannot be opened

@login_required
def goal_image(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id)
    description = f"Visual representation of goal: {goal.title} ({goal.goal_type})"
    
    # Generate the image
    image = generate_image(description)
    if image is None:
        return render(request, 'goals/goal_image.html', {
            'goal': goal,
            'error': "Could not generate an image for this goal. Please try again."
        })
    
    # Define the media directory and ensure it exists
    media_root = getattr(settings, 'MEDIA_ROOT', 'media')
    image_dir = os.path.join(media_root, 'images')
    os.makedirs(image_dir, exist_ok=True)

    # Define the image path on disk and URL path
    image_filename = f"{goal.id}_{goal.title.replace(' ', '_')}.png"
    image_save_path = os.path.join(image_dir, image_filename)  # Save path in the file system
    image_url_path = settings.MEDIA_URL + 'images/' + image_filename  # URL path for template rendering

    try:
        image.save(image_save_path)  # Save image to the media directory
    except Exception as e:
        logger.error(f"Failed to save image: {e}")
        return render(request, 'goals/goal_image.html', {
            'goal': goal,
            'error': "Failed to save the generated image. Please try again."
        })

    return render(request, 'goals/goal_image.html', {
        'goal': goal,
        'image_path': image_url_path
    })

# Add a new goal
def goal_add(request):
    if request.method == 'POST':
        title = request.POST['title']
        goal_type = request.POST['goal_type']
        target_value = request.POST['target_value']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        Goal.objects.create(
            title=title,
            goal_type=goal_type,
            target_value=target_value,
            start_date=start_date,
            end_date=end_date
        )
        return redirect('goal_list')

    return render(request, 'goals/add.html')

# Edit an existing goal
def goal_edit(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id)
    if request.method == 'POST':
        goal.title = request.POST['title']
        goal.goal_type = request.POST['goal_type']
        goal.target_value = request.POST['target_value']
        goal.start_date = request.POST['start_date']
        goal.end_date = request.POST['end_date']
        goal.save()
        return redirect('goal_list')
    return render(request, 'goals/edit.html', {'goal': goal})

# Delete a goal
def goal_delete(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id)
    if request.method == 'POST':
        goal.delete()
        return redirect('goal_list')
    return render(request, 'goals/delete.html', {'goal': goal})

# List progress for a specific goal
@login_required
def progress_list(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id)
    progress = goal.progress.all()  # Ensure 'progress' is the related_name in the Progress model

    # Fetch recommendations from the Groq API based on the goal's title
    chat_completion = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": f"Provide a brief, 1 short sentence recommendations for achieving the goal: {goal.title}.",
        }],
        model="llama3-8b-8192",
    )

    recommendations = chat_completion.choices[0].message.content

    return render(request, 'goals/progress_list.html', {
        'goal': goal,
        'progress': progress,
        'recommendations': recommendations,  # Pass recommendations to the template
    })
# goals/views.py
def goal_list(request):
    goals = Goal.objects.all()
    return render(request, 'goals/list.html', {'goals': goals})
