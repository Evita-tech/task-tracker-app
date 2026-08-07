from django.shortcuts import render
from .models import Project, Task

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'tasks/project_list.html', {'projects': projects})




def task_list(request):
    tasks = Task.objects.all()

    search_query = request.GET.get('search', '')
    if search_query:
        tasks = tasks.filter(title__icontains=search_query)

    status_filter = request.GET.get('status','')
    if status_filter:
        tasks = tasks.filter(status=status_filter)

    sort_by = request.GET.get('sort','')
    if sort_by:
        tasks = tasks.order_by(sort_by)

    context = {
        'tasks': tasks,
        'search_query': search_query,
        'status_filter': status_filter,
        'sort_by': sort_by,
    }
    return render(request, 'tasks/task_list.html', context)

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