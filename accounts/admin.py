from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import CustomUser, Profile, Resume, JobPost, Chat, Message

# Регистрируем кастомного пользователя
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser')

# Остальные модели
admin.site.register(Profile)
admin.site.register(Resume)
admin.site.register(JobPost)
admin.site.register(Chat)
admin.site.register(Message)

