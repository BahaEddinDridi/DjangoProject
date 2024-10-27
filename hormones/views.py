from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
import requests
import os
import time
import re
from groq import Groq
           
def get_hormone_recommendation(hormone_name, level, unit):
    prompt = (
        f"Recommandations d'entraînement et de nutrition pour réguler un niveau de {hormone_name} de {level} {unit}. "
        f"Si le niveau est élevé, conseillez un entraînement et une alimentation pour le réduire de manière saine. "
        f"Si le niveau est faible, donnez des recommandations pour l'augmenter. "
        f"Écrivez uniquement en français, en organisant les conseils par Entraînement et Nutrition. "
        f"Veuillez fournir une réponse concise de maximum 10 lignes."
    )
    
    client = Groq(
        api_key="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"
    )  
    
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-8b-8192"
            )
            
            generated_text = response.choices[0].message.content.strip()
            
            clean_text = re.sub(r'^\s*Écris.*\n', '', generated_text)
            
            lines = clean_text.split('\n')
            short_text = '\n'.join(lines[:5]) 
            return short_text

        except Exception as e:
            print(f"Erreur lors de l'appel à l'API Groq : {e}")
            if attempt < max_retries - 1:
                time.sleep(5)  
            else:
                return "Une erreur est survenue lors de la génération de la recommandation."

    
def generate_and_save_recommendation(hormone_level):

    recommendation_text = get_hormone_recommendation(hormone_level.hormone_name, hormone_level.level, hormone_level.unit)
    
  
    recommendation = HormoneRecommendation(
        hormone_level=hormone_level,
        recommendation=recommendation_text
    )
    

    recommendation.save()
def create_hormone_level(request):
    if request.method == 'POST':
        form = HormoneLevelForm(request.POST)
        if form.is_valid():
            hormone_level = form.save(commit=False)
            hormone_level.user = request.user
            hormone_level.save()  
            generate_and_save_recommendation(hormone_level)
            return redirect('list_hormone_levels')  
    else:
        form = HormoneLevelForm()
    
    return render(request, 'hormones/create.html', {'form': form})
def list_hormone_levels(request):
    levels = HormoneLevel.objects.all().prefetch_related('hormonerecommendation_set')

    paginator = Paginator(levels, 2)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  

    return render(request, 'hormones/list.html', {'page_obj': page_obj, 'levels': page_obj})
def update_hormone_level(request, level_id):
    hormone_level = get_object_or_404(HormoneLevel, id=level_id)

    if request.method == 'POST':
        form = HormoneLevelForm(request.POST, instance=hormone_level)
        if form.is_valid():
            form.save()
            generate_and_save_recommendation(hormone_level)
            return redirect('list_hormone_levels')  
    else:
        form = HormoneLevelForm(instance=hormone_level)

    return render(request, 'hormones/update.html', {'form': form,'hormone_level': hormone_level})

def delete_hormone_level(request, level_id):
    level = get_object_or_404(HormoneLevel, id=level_id)
    level.delete()
    return redirect('list_hormone_levels') 


