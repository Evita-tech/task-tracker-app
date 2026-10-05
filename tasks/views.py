from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Project, Task, Comment
from .forms import ProjectForm, TaskForm, CommentForm,RegisterForm
from django.core.mail import send_mail
def is_manager(user):
    return user.groups.filter(name='Manager').exists()

@login_required
def project_list(request):
    projects = Project.objects.exclude(name="Task Tracking Application")
    paginator = Paginator(projects, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    tasks = Task.objects.exclude(project__name="Task Tracking Application").select_related('project', 'assigned_to')
    return render(request, 'tasks/project_list.html', {'projects': page_obj, 'page_obj': page_obj, 'tasks': tasks})
@login_required
def task_list(request):
    tasks = Task.objects.all()
    if not is_manager(request.user):
        tasks = tasks.filter(assigned_to=request.user)

    search_query = request.GET.get('search', '')
    if search_query:
        tasks = tasks.filter(title__icontains=search_query)

    status_filter = request.GET.get('status', '')
    if status_filter:
        tasks = tasks.filter(status=status_filter)

    sort_by = request.GET.get('sort', '')
    ALLOWED_SORT_FIELDS = {'title', 'status', 'due_date'}
    if sort_by in ALLOWED_SORT_FIELDS:
        tasks = tasks.order_by(sort_by)

    paginator = Paginator(tasks, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    querydict = request.GET.copy()
    if 'page' in querydict:
        del querydict['page']
    query_string = querydict.urlencode() + '&' if querydict else ''

    context = {
        'tasks': page_obj,
        'page_obj': page_obj,
        'query_string': query_string,
        'search_query': search_query,
        'status_filter': status_filter,
        'sort_by': sort_by,
    }
    return render(request, 'tasks/task_list.html', context)
    
@login_required
def dashboard(request):
    app_project = Project.objects.filter(name="Task Tracking Application").first()
    total_projects = Project.objects.exclude(name="Task Tracking Application").count()
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
        'app_project': app_project,
    }
    return render(request, 'tasks/dashboard.html', context)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()  
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
            task = form.save()
            if task.assigned_to and task.assigned_to.email:
                send_mail(
                    subject=f'New task assigned: {task.title}',
                    message=(
                        f'Hello {task.assigned_to.username},\n\n'
                        f'You have been assigned a new task.\n\n'
                        f'Task: {task.title}\n'
                        f'Project: {task.project.name}\n'
                        f'Due date: {task.due_date or "Not set"}\n\n'
                        f'Please log in to the Task Tracker to view it.'
                    ),
                    from_email=None,
                    recipient_list=[task.assigned_to.email],
                )
            return redirect('task_list')
    else:
        form = TaskForm()

    return render(request, 'tasks/create_task.html', {'form': form})

@login_required
def update_task_status(request, pk):
    task = Task.objects.get(pk=pk)
   
    if not (is_manager(request.user) or task.assigned_to == request.user):
        return redirect('dashboard')
    if not is_manager(request.user) and task.edited:
        task.edited = False
        task.save()

    error = None

    if request.method == 'POST':
        new_status = request.POST.get('status')
        comment_text = request.POST.get('text', '').strip()

        if not comment_text:
            error = "Please add a comment explaining this update."
        elif new_status in ['todo', 'in_progress', 'done']:
            task.status = new_status
            task.save()
            Comment.objects.create(task=task, author=request.user, text=comment_text)
            return redirect('task_list')

    comments = task.comments.all()
    return render(request, 'tasks/update_task.html', {'task': task, 'comments': comments, 'error': error})
@login_required
def delete_task(request, pk):
    if not is_manager(request.user):
        return redirect('dashboard')
    task = Task.objects.get(pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/confirm_delete.html', {'object': task, 'type': 'task'})


@login_required
def delete_project(request, pk):
    if not is_manager(request.user):
        return redirect('dashboard')
    project = Project.objects.get(pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')
    return render(request, 'tasks/confirm_delete.html', {'object': project, 'type': 'project'})

@login_required
def edit_task(request, pk):
    if not is_manager(request.user):
        return redirect('dashboard')
    task = Task.objects.get(pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            task.edited = True
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/create_task.html', {'form': form})

def hello_world (request):
    return render (request, 'tasks/hello.html')