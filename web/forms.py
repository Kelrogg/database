from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from .models import Diagnosis, TemporaryContraindications


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
    first_name = forms.CharField(max_length=45, required=False, label='Имя',
                                widget=forms.TextInput(attrs={'placeholder': ''}))
    last_name = forms.CharField(max_length=45, required=False, label='Фамилия',
                                widget=forms.TextInput(attrs={'placeholder': ''}))
    birthday = forms.DateField(label='Дата рождения', input_formats=[
    '%Y-%m-%d',  # '2006-10-25'
    '%m/%d/%Y',  # '10/25/2006'
    '%m/%d/%y',  # '10/25/06'
    '%b %d %Y',  # 'Oct 25 2006'
    '%b %d, %Y',  # 'Oct 25, 2006'
    '%d %b %Y',  # '25 Oct 2006'
    '%d %b, %Y',  # '25 Oct, 2006'
    '%B %d %Y',  # 'October 25 2006'
    '%B %d, %Y',  # 'October 25, 2006'
    '%d %B %Y',  # '25 October 2006'
    '%d %B, %Y',  # '25 October, 2006'
    ], 
    widget=forms.TextInput(attrs={'placeholder': ''}))

    article = forms.CharField(max_length= 45, required=False, label='Действующая статья АК РФ:',
                               widget=forms.TextInput(attrs={'placeholder': ''}))
    gender = forms.ChoiceField(
        choices=[(True, 'Муж'), (True, 'Жен')],
        initial=None,
        label='Пол',
        required=False,
        widget=forms.RadioSelect,
    )
    login = forms.CharField(max_length=45, required=False, label='Логин',
                                widget=forms.TextInput(attrs={'placeholder': ''}))
    password = forms.CharField(max_length=45, required=False, label='Пароль',
                                widget=forms.TextInput(attrs={'placeholder': ''}))
                                    






# 

class PersonalData(forms.Form):
     full_name = forms.CharField(max_length=100, required=True, label='ФИО')
     qualification = forms.CharField(max_length=100, required=False, label='Квалификация')
     experience = forms.IntegerField(min_value=0, max_value=70, required=False, label='Стаж')
     work_place = forms.CharField(max_length=100, required=False, label='Место работы')
     education = forms.CharField(max_length=100, required=False, label='Образование')
     contacts = forms.CharField(max_length=100, required=False, label='Контакты')
     image = forms.ImageField(required=False, allow_empty_file=False)


class SignUpForm(UserCreationForm):
     full_name = forms.CharField(max_length=100, required=True)
     email = forms.EmailField(max_length=254, required=True)
     password1 = forms.CharField(widget=forms.PasswordInput())
     qualification = forms.CharField(max_length=40, required=False)
     work_place = forms.CharField(max_length=60, required=False)
     education = forms.CharField(max_length=30, required=False)
     experience = forms.IntegerField(min_value=0, required=False)
     contacts = forms.CharField(max_length=150, required=False)
     photo = forms.ImageField(required=True)

     class Meta:
         model = User
         fields = ('full_name', 'email', 'password1', 'qualification', 'work_place',
                   'education', 'experience', 'contacts', 'photo')

