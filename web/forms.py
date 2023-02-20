from django import forms
from django.contrib.auth import get_user
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.db import transaction
from django.core.files import File

from GosNadzor.settings import MEDIA_ROOT

from .models import *

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

class ArticleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, article):
        return str(article.number)

class CorrectionalWorkChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, article):
        return str(article.type)

class PrisonerSignUpForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', max_length=104)
    last_name = forms.CharField(label='Фамилия', max_length=104, required=False)
    prisoner_birthday = forms.DateField(label='Дата рождения', input_formats=[
        '%Y-%m-%d',  # '2006-10-25'
    ], widget=forms.TextInput(attrs={'placeholder': ''}))

    email = forms.EmailField(max_length=45, required=True, label='Почта',
                                widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Miha@yandex.ru', 'autocomplete': 'email'})),
    prisoner_gender = forms.ChoiceField(
        choices=[(0, 'Муж'), (1, 'Жен')],
        initial=None,
        label='Пол',
        required=True,
        widget=forms.RadioSelect,
    )
    
    article = ArticleChoiceField(
        queryset=Article.objects.all(), #.values('id', 'number'),
        widget = forms.CheckboxSelectMultiple
    )

    correctional_works_type = CorrectionalWorkChoiceField(
        queryset=CorrectionalWork.objects.all(), #.values('id', 'type'),
        widget=forms.CheckboxSelectMultiple
    )

    correctional_works_address = forms.CharField(widget = forms.TextInput())

    prisoner_image = forms.ImageField(required=True, widget=forms.FileInput())
    
    def __init__(self, *args, **kwargs):
        self.logged_user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_prisoner = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.image = self.cleaned_data.get('prisoner_image')
        user.save()
        if commit:
            user.save()

        admin=Admin.objects.get(user=self.logged_user)
        prisoner = Prisoner.objects.create(user=user,
            admin=admin,
            gender = self.cleaned_data.get('prisoner_gender'),
            birthday = self.cleaned_data.get('prisoner_birthday')
        )
        
        for article in self.cleaned_data.get('article'):
            prisoner.articles.add(article)

        # prisoner.records.add(
        #     Record.objects.filter(date=self.cleaned_data.get('records'))
        # )

        for correctional_work in self.cleaned_data.get('correctional_works_type'):
            prisoner.correctional_works.add(
                correctional_work,
                through_defaults={'admin_id': admin}
            )

        #prisoner.correctional_works.add(
        #    CorrectionalWork.objects.get(type=self.cleaned_data.get('correctional_works_type')), 
        #    through_defaults={'admin_id': admin}
        #)

        prisoner.save()
        return user

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', max_length=104)
    last_name = forms.CharField(label='Фамилия', max_length=104, required=False)
    admin_birthday = forms.DateField(label='Дата рождения', input_formats=[
        '%Y-%m-%d',  # '2006-10-25'
    ], widget=forms.TextInput(attrs={'placeholder': ''}))

    email = forms.EmailField(max_length=45, required=True, label='Почта',
                                widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Miha@yandex.ru', 'autocomplete': 'email'})),
    rank = forms.CharField(max_length=45, required=False, label='Должность/Звание', widget=forms.TextInput())
    admin_gender = forms.ChoiceField(
       choices=[(0, 'Муж'), (1, 'Жен')],
       initial=None,
       label='Пол',
       required=True,
       widget=forms.RadioSelect,   
    )

    admin_image = forms.ImageField(required=True,
                                   widget=forms.FileInput())

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_admin = True
        user.is_staff = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.image = self.cleaned_data.get('admin_image')
        user.save()
        admin = Admin.objects.create(user=user,
            rank = self.cleaned_data.get('rank'),
            gender = self.cleaned_data.get('admin_gender'),
            birthday = self.cleaned_data.get('admin_birthday')
        )
        admin.save()
        return user

class LoginUserForm(AuthenticationForm):
    username = forms.EmailField(label='Почта', widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'почта', 'autocomplete': 'email'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'пароль'}))
    

