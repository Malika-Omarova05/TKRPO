from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    #  Админ-панель
    path('admin/', admin.site.urls),

    #  Приложение аккаунтов (регистрация, вход, профиль, резюме)
    path('accounts/', include('accounts.urls')),

    #  Можно добавить отдельное приложение для вакансий (jobs)
    # path('jobs/', include('jobs.urls')),

    #  Главная страница проекта
    path('', include('accounts.urls')),  # если хочешь, чтобы домашняя страница была из accounts
]
