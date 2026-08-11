from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login_func, authenticate, logout as auth_logout_func
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm, UserRegisterForm

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login_func(request, user)
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'tasks/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login_func(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'tasks/login.html', {'form': form})

def logout_view(request):
    auth_logout_func(request)
    return redirect('login')

@login_required
def dashboard(request):
    tasks_query = Task.objects.filter(user=request.user)
    
    # Simple search
    search_query = request.GET.get('search', '')
    if search_query:
        tasks_query = tasks_query.filter(title__icontains=search_query)
        
    # Group tasks by status for visual layout (Kanban style or columns)
    todo_tasks = tasks_query.filter(status='todo')
    in_progress_tasks = tasks_query.filter(status='in_progress')
    completed_tasks = tasks_query.filter(status='completed')
    
    context = {
        'todo_tasks': todo_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completed_tasks': completed_tasks,
        'search_query': search_query,
        'total_tasks': tasks_query.count()
    }
    return render(request, 'tasks/dashboard.html', context)

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('dashboard')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Create Task'})

@login_required
def task_update(request):
    pass # Wait, let's implement the actual logic:

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Edit Task', 'task': task})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('dashboard')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})
