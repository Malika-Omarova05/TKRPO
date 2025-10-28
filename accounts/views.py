from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import Resume, JobPost   # ✅ добавили импорт моделей


# Регистрация
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # сразу авторизуем
            # после регистрации сразу отправляем по роли
            if user.role == 'employer':
                return redirect('employer_home')
            elif user.role == 'seeker':
                return redirect('seeker_home')
            elif user.role == 'admin':
                return redirect('admin_home')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


# Вход
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # проверяем роль и перенаправляем
            if user.role == 'employer':
                return redirect('employer_home')
            elif user.role == 'seeker':
                return redirect('seeker_home')
            elif user.role == 'admin':
                return redirect('admin_home')
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


# Главная страница
def home(request):
    if request.user.is_authenticated:
        if request.user.role == 'employer':
            return redirect('employer_home')
        elif request.user.role == 'seeker':
            return redirect('seeker_home')
        elif request.user.role == 'admin':
            return redirect('admin_home')
    return render(request, 'accounts/home.html')


# Домашняя страница работодателя
def employer_home(request):
    return render(request, 'accounts/employer_home.html')


# Домашняя страница соискателя
def seeker_home(request):
    return render(request, 'accounts/seeker_home.html')


# Домашняя страница администратора (приветствие)
def admin_home(request):
    return render(request, 'accounts/admin_home.html')


# Выход
def logout_view(request):
    logout(request)
    return redirect('home')


# Проверка, что пользователь админ
def is_admin(user):
    return user.is_authenticated and user.role == 'admin'


# Панель администратора
@user_passes_test(is_admin)
def admin_dashboard(request):
    resumes = Resume.objects.all()
    jobs = JobPost.objects.all()
    return render(request, 'accounts/admin_dashboard.html', {
        'resumes': resumes,
        'jobs': jobs
    })


# Удаление резюме
@user_passes_test(is_admin)
def delete_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    resume.delete()
    return redirect('admin_dashboard')


# Удаление вакансии
@user_passes_test(is_admin)
def delete_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    job.delete()
    return redirect('admin_dashboard')
