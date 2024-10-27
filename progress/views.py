
from django.shortcuts import render, redirect, get_object_or_404
from .models import Progress
from goals.models import Goal
from django.views import View
from django.contrib.auth.decorators import login_required

@login_required
def progress_list(request):
    progresses = Progress.objects.all()
    return render(request, 'progress/list.html', {'progresses': progresses})

@login_required
def progress_add(request):
    if request.method == 'POST':
        user = request.user  
        goal_id = request.POST['goal_id']
        progress_date = request.POST['progress_date']
        value = request.POST['value']

        goal = get_object_or_404(Goal, id=goal_id)  

        Progress.objects.create(
            user=user,
            goal=goal,
            progress_date=progress_date,
            value=value
        )
        return redirect('progress_list')

    goals = Goal.objects.all()  
    return render(request, 'progress/add.html', {'goals': goals})

@login_required
def progress_edit(request, progress_id):
    progress = get_object_or_404(Progress, id=progress_id)
    
    if request.method == 'POST':
        progress.goal = get_object_or_404(Goal, id=request.POST['goal'])
        progress.progress_date = request.POST['progress_date']
        progress.value = request.POST['value']
        progress.save()
        return redirect('progress_list')  

    goals = Goal.objects.all()
    return render(request, 'progress/edit.html', {'progress': progress, 'goals': goals})

@login_required
def progress_delete(request, progress_id):
    progress = get_object_or_404(Progress, id=progress_id)
    if request.method == 'POST':
        progress.delete()
        return redirect('progress_list')
    return render(request, 'progress/delete.html', {'progress': progress})


