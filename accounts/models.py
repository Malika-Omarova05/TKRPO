from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('employer', 'Работодатель'),
        ('seeker', 'Соискатель'),
        ('admin', 'Администратор'),  # админ есть, но через регистрацию его выбрать нельзя
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='seeker')

    def __str__(self):
        return f"{self.username} ({self.role})"
