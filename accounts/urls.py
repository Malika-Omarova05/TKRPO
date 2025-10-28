from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),  # ✅ добавили
    path('employer_home/', views.employer_home, name='employer_home'),
    path('seeker_home/', views.seeker_home, name='seeker_home'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('delete_resume/<int:resume_id>/', views.delete_resume, name='delete_resume'),
    path('delete_job/<int:job_id>/', views.delete_job, name='delete_job'),

]
