from django.urls import path
from . import views

urlpatterns = [
    # ---------------------------
    # Базовые страницы
    # ---------------------------
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ---------------------------
    # Домашние страницы по ролям
    # ---------------------------
    path('employer_home/', views.employer_home, name='employer_home'),
    path('seeker_home/', views.seeker_home, name='seeker_home'),
    path('admin_home/', views.admin_home, name='admin_home'),

    # ---------------------------
    # Админ-панель
    # ---------------------------
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('delete_resume/<int:resume_id>/', views.delete_resume, name='delete_resume'),
    path('delete_job/<int:job_id>/', views.delete_job, name='delete_job'),

    # ---------------------------
    # Профиль (личный кабинет)
    # ---------------------------
    path('profile/', views.profile_view, name='profile'),

    # ---------------------------
    # Работа с резюме
    # ---------------------------
    path('resume/create/', views.create_resume, name='create_resume'),
    path('resume/<int:resume_id>/edit/', views.edit_resume, name='edit_resume'),

    # ---------------------------
    # Вакансии
    # ---------------------------
    path('vacancies/', views.vacancy_list, name='vacancy_list'),  # список всех вакансий
    path('vacancy/<int:vacancy_id>/respond/', views.respond_to_vacancy, name='respond_to_vacancy'),

    # ---------------------------
    # Чат
    # ---------------------------
    path('chat/<int:chat_id>/', views.chat_view, name='chat_view'),
]
