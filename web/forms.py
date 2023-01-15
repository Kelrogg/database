from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.db import transaction

from .models import User, Admin, Prisoner

class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email',)

class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',)


def get_placeholder_widget(name, css_class=None):
    return forms.TextInput(attrs={'placeholder': name,
                                  'class': css_class})


def choice_to_bool(string: str) -> bool:
    choice_to_bool_dict = {
        'yes': True,
        'no': False,
        'unknown': None
    }

    return choice_to_bool_dict[string.lower()]

class PrisonerSignUpForm(UserCreationForm):
    prisoner_birthday = forms.DateField(label='Дата рождения', input_formats=[
    '%Y-%m-%d',  # '2006-10-25'
    ], 
    widget=forms.TextInput(attrs={'placeholder': ''}))

    article = forms.CharField(max_length= 45, required=True, label='Действующая статья УК РФ:',
                               widget=forms.TextInput(attrs={'placeholder': ''}))
    prisoner_gender = forms.ChoiceField(
        choices=[(True, 'Муж'), (True, 'Жен')],
        initial=None,
        label='Пол',
        required=True,
        widget=forms.RadioSelect,
    )
    prisoner_login = forms.CharField(max_length=45, required=True, label='Логин',
                                widget=forms.TextInput(attrs={'placeholder': ''}))
    prisoner_image = forms.ImageField(required=True, allow_empty_file=True)
    
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_prisoner = True
        if commit:
            user.save()
        return user

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', max_length=104)
    last_name = forms.CharField(label='Фамилия', max_length=104, required=False)
    admin_birthday = forms.DateField(label='Дата рождения', input_formats=[
        '%Y-%m-%d',  # '2006-10-25'
    ],
    widget=forms.TextInput(attrs={'placeholder': ''}))
    email = forms.EmailField(max_length=45, required=True, label='Почта',
                                widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Miha@yandex.ru', 'autocomplete': 'email'})),
    rank = forms.CharField(max_length=45, required=False, label='Должность/Звание')
    admin_gender = forms.ChoiceField(
       choices=[(True, 'Муж'), (True, 'Жен')],
       initial=None,
       label='Пол',
       required=True,
       widget=forms.RadioSelect,   
    )
    admin_image = forms.ImageField(required=True, allow_empty_file=True)
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_admin = True
        user.save()
        return user

class LoginUserForm(AuthenticationForm):
    username = forms.EmailField(label='Почта', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'почта', 'autocomplete': 'email'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'пароль'}))