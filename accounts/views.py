from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileForm, ResumeForm
from .models import CustomUser, Resume, JobPost, Profile

# ---------------------------
# Регистрация
# ---------------------------
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # сразу авторизуем
            # перенаправление по роли
            if user.role == 'employer':
                return redirect('employer_home')
            elif user.role == 'seeker':
                return redirect('profile')
            elif user.role == 'admin':
                return redirect('admin_home')
            return redirect('home')
        else:
            # если форма не валидна, ошибки будут отображены
            return render(request, 'accounts/register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

# ---------------------------
# Вход
# ---------------------------
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.role == 'employer':
                return redirect('employer_home')
            elif user.role == 'seeker':
                return redirect('profile')
            elif user.role == 'admin':
                return redirect('admin_home')
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'form': form})
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

# ---------------------------
# Главная страница
# ---------------------------
def home(request):
    if request.user.is_authenticated:
        if request.user.role == 'employer':
            return redirect('employer_home')
        elif request.user.role == 'seeker':
            return redirect('profile')
        elif request.user.role == 'admin':
            return redirect('admin_home')
    return render(request, 'accounts/home.html')

# ---------------------------
# Домашние страницы по ролям
# ---------------------------
@login_required
def employer_home(request):
    return render(request, 'accounts/employer_home.html')

@login_required
def seeker_home(request):
    return render(request, 'accounts/seeker_home.html')

@login_required
def admin_home(request):
    return render(request, 'accounts/admin_home.html')

# ---------------------------
# Выход
# ---------------------------
def logout_view(request):
    logout(request)
    return redirect('home')

# ---------------------------
# Проверка роли администратора
# ---------------------------
def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

# ---------------------------
# Панель администратора
# ---------------------------
@user_passes_test(is_admin)
def admin_dashboard(request):
    resumes = Resume.objects.all()
    jobs = JobPost.objects.all()
    return render(request, 'accounts/admin_dashboard.html', {
        'resumes': resumes,
        'jobs': jobs
    })

@user_passes_test(is_admin)
def delete_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    resume.delete()
    return redirect('admin_dashboard')

@user_passes_test(is_admin)
def delete_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    job.delete()
    return redirect('admin_dashboard')

# ---------------------------
# Личный кабинет (профиль)
# ---------------------------
@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # перенаправление после сохранения
    else:
        form = ProfileForm(instance=profile)

    resumes = Resume.objects.filter(seeker=request.user)

    return render(request, 'accounts/profile.html', {
        'form': form,
        'resumes': resumes
    })

# ---------------------------
# Создание резюме (для соискателя)
# ---------------------------
@login_required
def create_resume(request):
    if request.user.role != 'seeker':
        return redirect('profile')

    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.seeker = request.user
            resume.save()
            return redirect('profile')
    else:
        form = ResumeForm()

    return render(request, 'accounts/resume_form.html', {
        'form': form,
        'title': 'Создать резюме'
    })

# ---------------------------
# Редактирование резюме (для соискателя)
# ---------------------------
@login_required
def edit_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, seeker=request.user)

    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ResumeForm(instance=resume)

    return render(request, 'accounts/resume_form.html', {
        'form': form,
        'title': 'Редактировать резюме'
    })
