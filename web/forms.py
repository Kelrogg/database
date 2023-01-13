from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


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

    article = forms.CharField(max_length= 45, required=True, label='Действующая статья АК РФ:',
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
                                    

class SignUpForm(UserCreationForm): 
     admin_birthday = forms.DateField(label='Дата рождения', input_formats=[
        '%Y-%m-%d',  # '2006-10-25'
    ], 
     widget=forms.TextInput(attrs={'placeholder': ''}))
     rank = forms.CharField(max_length=45, required=False, label='Должность/Звание')
     admin_gender = forms.ChoiceField(
        choices=[(True, 'Муж'), (True, 'Жен')],
        initial=None,
        label='Пол',
        required=True,
        widget=forms.RadioSelect,   
    )
     admin_login = forms.CharField(max_length=45, required=True, label='Логин',
                                widget=forms.TextInput(attrs={'placeholder': ''}))
     admin_image = forms.ImageField(required=True, allow_empty_file=True) 

class LoginUserForm(AuthenticationForm):
    username = forms.EmailField(label='Почта', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'почта', 'autocomplete': 'email'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'пароль'}))