from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator


def create_Event(request):
    if request.method == 'POST':
        form = EvenementSportifForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organisateur = request.user  # Associe l'utilisateur connecté comme organisateur
            event.save()
            return redirect('list_event')  # Rediriger vers la liste des événements
    else:
        form = EvenementSportifForm()
    
    return render(request, 'events/create.html', {'form': form})
# READ

def list_Event(request):
    events = EvenementSportif.objects.all()  # Récupération des événements depuis la base de données
    paginator = Paginator(events, 2)  # Pagination : 4 événements par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'events/list.html', {'page_obj': page_obj})

# UPDATE
def update_event(request, event_id):
    # Récupère l'instance de l'événement
    event = get_object_or_404(EvenementSportif, id=event_id)

    if request.method == 'POST':
        # Passe les données POST et l'instance pour les mises à jour
        form = EvenementSportifForm(request.POST, instance=event)
        if form.is_valid():
            form.save()  # Enregistre les modifications
            return redirect('list_event')  # Redirige vers la liste des événements
    else:
        form = EvenementSportifForm(instance=event)  # Passe l'instance pour pré-remplir le formulaire

    # Passe l'événement et le formulaire au template
    return render(request, 'events/update.html', {'form': form, 'event': event})


# DELETE

def delete_event(request, event_id):
    # Récupérer le niveau hormonal à supprimer
    event = get_object_or_404(EvenementSportif, id=event_id)
    
    # Supprimer le niveau hormonal
    event.delete()
    
    # Rediriger vers la liste des niveaux hormonaux après suppression
    return redirect('list_event')