from django.shortcuts import render
from .models import Project, Task

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'tasks/project_list.html', {'projects': projects})




def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def dashboard(request):
    total_projects = Project.objects.count()
    total_tasks = Task.objects.count()
    todo_count = Task.objects.filter(status='todo').count()
    in_progress_count = Task.objects.filter(status='in_progress').count()
    done_count = Task.objects.filter(status='done').count()

    context = {
        'total_projects': total_projects,
        'total_tasks': total_tasks,
        'todo_count': todo_count,
        'in_progress_count': in_progress_count,
        'done_count': done_count,
    }
    return render(request, 'tasks/dashboard.html', context)