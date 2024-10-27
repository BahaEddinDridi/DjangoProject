from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.core.paginator import Paginator
import os
from groq import Groq
import requests  # Import requests for API calls
# Initialize the Groq client with your API key
client = Groq(api_key="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")
API_URL = "https://api-inference.huggingface.co/models/SamLowe/roberta-base-go_emotions"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    """Function to query the Hugging Face sentiment analysis API."""
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def analyze_sentiment(request):
    """Function to analyze sentiment using the API."""
    output = None
    if request.method == 'POST':
        text = request.POST.get('text')  # Get text input from the request
        if text:
            output = query({"inputs": text})  # Query the sentiment analysis API
    
    return render(request, 'events/analyze_sentiment.html', {'output': output})

def create_Event(request):
    if request.method == 'POST':
        form = EvenementSportifForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organisateur = request.user  # Associate the logged-in user as the organizer
            event.save()
            return redirect('list_event')  # Redirect to the event list
    else:
        form = EvenementSportifForm()
    
    return render(request, 'events/create.html', {'form': form})

# READ
def list_Event(request):
    events = EvenementSportif.objects.all()  # Retrieve events from the database
    paginator = Paginator(events, 2)  # Pagination: 2 events per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'events/list.html', {'page_obj': page_obj})

# UPDATE
def update_event(request, event_id):
    # Retrieve the event instance
    event = get_object_or_404(EvenementSportif, id=event_id)

    if request.method == 'POST':
        # Pass POST data and the instance for updates
        form = EvenementSportifForm(request.POST, instance=event)
        if form.is_valid():
            form.save()  # Save the changes
            return redirect('list_event')  # Redirect to the event list
    else:
        form = EvenementSportifForm(instance=event)  # Pre-fill the form with the instance

    # Pass the event and the form to the template
    return render(request, 'events/update.html', {'form': form, 'event': event})

# DELETE
def delete_event(request, event_id):
    # Retrieve the event to delete
    event = get_object_or_404(EvenementSportif, id=event_id)
    
    # Delete the event
    event.delete()
    
    # Redirect to the event list after deletion
    return redirect('list_event')

import random

def detail_event(request, event_id):
    event = get_object_or_404(EvenementSportif, id=event_id)

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

    # Randomly select an emotion and append it to the event description
    random_emotion = random.choice(emotions)
    modified_description = f"{event.description} This event is very {random_emotion}!"

    # Fetch recommendations from the Groq API
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Provide a brief, 3 short sentences of recommended similar events or tips related to '{modified_description}'."  # Use the modified description
            }
        ],
        model="llama-3.1-70b-versatile",
    )

    # Get the recommendation text from the response
    recommendations = chat_completion.choices[0].message.content

    # Analyze sentiment of the modified event description
    sentiment_output = query({"inputs": modified_description})  # Call the sentiment analysis API

    # Extract the first sentiment label and its score
    if sentiment_output and isinstance(sentiment_output, list) and sentiment_output:
        first_sentiment = sentiment_output[0][0]  # Accessing the first result
        sentiment_label = first_sentiment['label']  # Extracting the label
        sentiment_score = first_sentiment['score']  # Extracting the score
    else:
        sentiment_label = None
        sentiment_score = None

    return render(request, 'events/detail.html', {
        'event': event,
        'recommendations': recommendations,
        'sentiment_label': sentiment_label,  # Pass the sentiment label to the template
        'sentiment_score': sentiment_score,  # Pass the sentiment score to the template
    })

# Event List View
def list_event(request):
    events = EvenementSportif.objects.all()  # Fetch all events
    paginator = Paginator(events, 2)  # Pagination
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'events/list.html', {'page_obj': page_obj})