from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import RegisterForm, AuthenticationForm, TaskForm
from .models import Task
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tasks:home')
    else:
        form = RegisterForm()
    return render(request, 'tasks/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('tasks:home') 
    else:
        form = AuthenticationForm()
    return render(request, 'tasks/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('tasks:login') 

@login_required
@csrf_exempt
def home(request):
    tasks = Task.objects.filter(created_by=request.user)
    return render(request, 'tasks/home.html', {'tasks': tasks})

@csrf_exempt
def add_task(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        if title and due_date:
            new_task = Task(title=title, description=description, due_date=due_date, created_by=request.user)
            new_task.save()
            return redirect('tasks:home')
        else:
            return HttpResponse("Title and Due Date are required fields.")
    return redirect('tasks:home')

@login_required
def edit_task(request, task_id):
    task_instance = get_object_or_404(Task, id=task_id)
    if request.method == 'POST' and task_instance.created_by == request.user:
        
        form = TaskForm(request.POST, instance=task_instance)
        if form.is_valid():
            form.save()
            return redirect('tasks:home')
    else:
        form = TaskForm(instance=task_instance)
    return render(request, 'tasks/edit_task.html', {'form': form, 'task': task_instance})

@login_required
def delete_task(request, task_id):
    task_instance = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task_instance.delete()
        return redirect('tasks:home')
    return render(request, 'tasks/confirm_delete.html', {'task': task_instance})