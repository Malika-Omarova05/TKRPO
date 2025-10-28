from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm

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

# Домашняя страница администратора
def admin_home(request):
    return render(request, 'accounts/admin_home.html')

def logout_view(request):
    logout(request)
    return redirect('home')