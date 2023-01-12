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

class TreatmentForm(forms.Form):
    first_name = forms.CharField(max_length=45, required=True, label='Имя',
                                widget=forms.TextInput(attrs={'placeholder': ''}))
    last_name = forms.CharField(max_length=45, required=True, label='Фамилия',
                                widget=forms.TextInput(attrs={'placeholder': ''}))
    birthday = forms.DateField(label='Дата рождения', input_formats=[
    '%Y-%m-%d',  # '2006-10-25'
    ], 
    widget=forms.TextInput(attrs={'placeholder': ''}))

    article = forms.CharField(max_length= 45, required=True, label='Действующая статья АК РФ:',
                               widget=forms.TextInput(attrs={'placeholder': ''}))
    gender = forms.ChoiceField(
        choices=[(True, 'Муж'), (True, 'Жен')],
        initial=None,
        label='Пол',
        required=True,
        widget=forms.RadioSelect,
    )
    login = forms.CharField(max_length=45, required=True, label='Логин',
                                widget=forms.TextInput(attrs={'placeholder': ''}))
    password = forms.CharField(max_length=45, required=True, label='Пароль',
                                widget=forms.TextInput(attrs={'placeholder': ''}))
                                    

# 
class PersonalData(forms.Form):
     admin_first_name = forms.CharField(max_length=45, required=True, label='Имя',
                                         widget=forms.TextInput(attrs={'placeholder': ''}))
     admin_last_name = forms.CharField(max_length=45, required=True, label='Фамилия',
                                         widget=forms.TextInput(attrs={'placeholder': ''}))
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
     admin_password = forms.CharField(max_length=45, required=True, label='Пароль',
                                widget=forms.TextInput(attrs={'placeholder': ''}))
     admin_image = forms.ImageField(required=True, allow_empty_file=False) 


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