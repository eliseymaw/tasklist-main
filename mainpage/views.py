import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .models import Task, Profile, Geoposition
from .forms import TaskForm, RegisterForm, LoginForm, ProfileForm, GeopositionForm
from django.http import JsonResponse

# Регистрация пользователя
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("base")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

# Вход пользователя
def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("base")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})

# Выход пользователя
def logout_view(request):
    logout(request)
    return redirect("login")

# Стартовая страница
@login_required
def base(request):
    tasks = Task.objects.filter(owner=request.user)
    return render(request, 'base.html', {'tasks': tasks, 'today': now().date()})

# Создание новой задачи
@login_required
def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        date_start = request.POST.get('date_start')
        deadline = request.POST.get('deadline')
        repeat_type = request.POST.get('repeat_type')
        repeat_i = request.POST.get('repeat_i')

        task_form_data = {
            'title': title,
            'description': description,
            'date_start': date_start,
            'deadline': deadline,
            'repeat_type': repeat_type,
            'repeat_i': repeat_i,
        }

        form = TaskForm(task_form_data)

        lat = float(request.POST.get('lat'))
        lon = float(request.POST.get('lon'))
        geop_form = GeopositionForm({'lat': lat, 'lon': lon})

        print("POST данные:", request.POST)

        if form.is_valid() and geop_form.is_valid():
            geop = geop_form.save()
            task = form.save(commit=False)
            task.geop = geop
            task.owner = request.user
            task.save()

            print(f"Создана задача: {task.title}, ID: {task.id}, Владелец: {task.owner}")

            return redirect('task_list_main')

        else:
            print("Ошибки формы:", form.errors)
            print("Ошибки формы геопозиции:", geop_form.errors)

    else:
        form = TaskForm()
        geop_form = GeopositionForm()

    return render(request, 'create_task.html', {'form': form, 'geop_form': geop_form})


@login_required
def task_list(request):
    tasks = Task.objects.filter(owner=request.user)#.select_related("geop")
    print(tasks)
    tasks_json =[
        {
            "id": task.id,
            "title": task.title,
    #         "description": task.description,
    #         "date_start": str(task.date_start),
    #         "deadline": str(task.deadline),
    #         "repeat_type": task.repeat_type,
    #         "repeat_i": task.repeat_i,
            "geop": {
                "lat": float(task.geop.lat) if task.geop else None,
                "lon": float(task.geop.lon) if task.geop else None
            }
        }
        for task in tasks
    ] 
    print(tasks_json)
    

    return render(request, "tasks.html", 
                  {"tasks": tasks, 
                   "tasks_json":json.dumps(tasks_json)})

# Получение задач в JSON формате
@login_required
def task_list_json(request):
    tasks = Task.objects.filter(owner=request.user).select_related("geop")

    tasks_list = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "date_start": str(task.date_start),
            "deadline": str(task.deadline),
            "repeat_type": task.repeat_type,
            "repeat_i": task.repeat_i,
            "geop": {
                "lat": task.geop.lat if task.geop else None,
                "lon": task.geop.lon if task.geop else None
            }
        }
        for task in tasks
    ]

    return JsonResponse({"tasks": tasks_list})


@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'profile.html', {'user': user})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile', username=request.user.username)
    else:
        form = ProfileForm(instance=request.user.profile)

    return render(request, 'edit_profile.html', {'form': form})

# Детали задачи (JSON)
@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)

    data = {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'date_start': str(task.date_start),
        'deadline': str(task.deadline),
        'repeat_type': task.repeat_type,
        'repeat_i': task.repeat_i,
        'geop': {
            'lat': task.geop.lat if task.geop else None,
            'lon': task.geop.lon if task.geop else None
        }
    }
    return JsonResponse(data)


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list_main')
    else:
        form = TaskForm(instance=task)

    return render(request, 'edit_task.html', {'form': form, 'task': task})


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    task.delete()
    return redirect('task_list_main')