from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Project, Task
from .forms import ProjectForm, TaskForm
def is_manager(user):
    return user.groups.filter(name='Manager').exists()

@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'tasks/project_list.html', {'projects': projects})




@login_required
def task_list(request):
    tasks = Task.objects.all()

    search_query = request.GET.get('search', '')
    if search_query:
        tasks = tasks.filter(title__icontains=search_query)

    status_filter = request.GET.get('status','')
    if status_filter:
        tasks = tasks.filter(status=status_filter)

    sort_by = request.GET.get('sort','')
    ALLOWED_SORT_FIELDS = {'title', 'status', 'due_date'}
    if sort_by in ALLOWED_SORT_FIELDS:
        tasks = tasks.order_by(sort_by)

    context = {
        'tasks': tasks,
        'search_query': search_query,
        'status_filter': status_filter,
        'sort_by': sort_by,
    }
    return render(request, 'tasks/task_list.html', context)

@login_required
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

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()  
    return render(request, 'tasks/register.html', {'form': form})


@login_required
def create_project(request):
    if not is_manager(request.user):
        return redirect('dashboard')

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()

    return render(request, 'tasks/create_project.html', {'form': form})

@login_required
def create_task(request):
    if not is_manager(request.user):
        return redirect('dashboard')

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()

    return render(request, 'tasks/create_task.html', {'form': form})