from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Profile, Resume

# ---------------------------
# Форма регистрации
# ---------------------------
class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        min_length=4,
        help_text="Минимум 4 символа. Можно буквы и цифры."
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput,
        min_length=4,
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # убираем роль admin из списка при регистрации
        if 'role' in self.fields:
            self.fields['role'].choices = [
                choice for choice in self.fields['role'].choices if choice[0] != 'admin'
            ]


# ---------------------------
# Форма входа
# ---------------------------
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


# ---------------------------
# Форма профиля (личный кабинет)
# ---------------------------
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'city', 'bio', 'avatar']
        labels = {
            'phone': 'Телефон',
            'city': 'Город',
            'bio': 'О себе',
            'avatar': 'Аватар',
        }
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': '+7 (999) 123-45-67'}),
            'city': forms.TextInput(attrs={'placeholder': 'Ваш город'}),
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Кратко расскажите о себе'}),
        }


# ---------------------------
# Форма резюме (создание и редактирование)
# ---------------------------
class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title', 'description', 'experience', 'education', 'skills']
        labels = {
            'title': 'Название резюме',
            'description': 'Описание',
            'experience': 'Опыт работы',
            'education': 'Образование',
            'skills': 'Навыки',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Краткое описание'}),
            'experience': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ваш опыт работы'}),
            'education': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ваше образование'}),
            'skills': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Ваши ключевые навыки'}),
        }
