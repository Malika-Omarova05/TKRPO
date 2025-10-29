from django.db import models
from django.contrib.auth.models import AbstractUser

#  Кастомная модель пользователя
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('employer', 'Работодатель'),
        ('seeker', 'Соискатель'),
        ('admin', 'Администратор'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='seeker')

    def __str__(self):
        return f"{self.username} ({self.role})"


#  Профиль пользователя (личный кабинет)
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField("Телефон", max_length=20, blank=True)
    city = models.CharField("Город", max_length=100, blank=True)
    bio = models.TextField("О себе", blank=True)
    avatar = models.ImageField("Аватар", upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"Профиль {self.user.username}"


#  Резюме (для соискателя)
class Resume(models.Model):
    seeker = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'seeker'}, related_name='resumes')
    title = models.CharField("Название резюме", max_length=200)
    description = models.TextField("Описание", blank=True)
    experience = models.TextField("Опыт работы", blank=True)
    education = models.TextField("Образование", blank=True)
    skills = models.TextField("Навыки", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Резюме: {self.title} ({self.seeker.username})"


# Вакансия (для работодателя)
class JobPost(models.Model):
    employer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'employer'}, related_name='job_posts')
    title = models.CharField("Название вакансии", max_length=200)
    description = models.TextField("Описание вакансии")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Вакансия: {self.title} ({self.employer.username})"
