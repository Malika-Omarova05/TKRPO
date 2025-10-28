from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


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
        # убираем роль admin из списка, чтобы нельзя было выбрать при регистрации
        if 'role' in self.fields:
            self.fields['role'].choices = [
                choice for choice in self.fields['role'].choices if choice[0] != 'admin'
            ]


# Форма входа (можно использовать стандартную, но для удобства оставим класс)
class CustomAuthenticationForm(AuthenticationForm):
    pass
