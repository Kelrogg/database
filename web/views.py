import os
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import generic, View
from django.urls import reverse_lazy
from .models import Admin, User
from .forms import PrisonerSignUpForm

from .LabelDecoder import decode_label_detail

from .forms import SignUpForm, LoginUserForm


LOGIN_URL = 'login'

class SignUpUser(generic.edit.CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'registration/sign_up.html'

    def get_success_url(self):
        return reverse_lazy('login')

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'admin'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        admin = Admin.objects.create(user=user)
        admin.rank = form.fields['rank'] # ['rank'].value()
        #admin.gender = self.cleaned_data['admin_gender']
        #admin.birthday = self.cleaned_data['admin_birthday']
        #admin.user.first_name = self.cleaned_data['first_name']
        #admin.user.last_name = self.cleaned_data['last_name']
        #admin.user.email = self.cleaned_data['email']
        login(self.request, user)
        return redirect('login')

class LoginUser(LoginView):
    model = User
    form_class = LoginUserForm
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy('user_cabinet')


class SignUpPrisoner(generic.edit.CreateView):
    model = User
    form_class = PrisonerSignUpForm
    template_name = 'registration/treatment_form.html'

    def get_succes_url(self):
        return reverse_lazy('user_cabinet')

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'prisoner'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return reverse_lazy('home')


def treatment_form_view(request):
    if request.method == 'POST':
        form = PrisonerSignUpForm(request.POST, request.FILES)

        if form.is_valid():
            user = User()
            
            user.username = form.cleaned_data['prisoner_login']
            user.save()
    else:
        form = PrisonerSignUpForm()

    return render(request, 'userf', {'form': form})

@login_required(login_url=LOGIN_URL)
def cabinet_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            doctor = request.user.username
            doctor.full_name = form.cleaned_data['full_name']
            doctor.qualification = form.cleaned_data['qualification']
            doctor.experience = form.cleaned_data['experience']
            doctor.work_place = form.cleaned_data['work_place']
            doctor.education = form.cleaned_data['education']
            doctor.contacts = form.cleaned_data['contacts']
            if form.cleaned_data['image']:
                doctor.photo = form.cleaned_data['image']
            doctor.save()

    doctor = request.user
    data = {
        'full_name': doctor.username,
        'qualification': doctor.username,
        'work_place': doctor.username,
        'education': doctor.username,
        'experience': doctor.username,
        'contacts': doctor.username,
        'photo': doctor.username,
    }
    form = SignUpForm(data)

    def get_queryset():
        search_query = request.GET.get('q')
        search_query = search_query if search_query else ''
        return reversed({})

    return render(request, 'cabinet.html',
                  context={'header': 'Личный кабинет',
                           'doctor': request.user.username,
                           'form': form,
                           'history': get_queryset,
                           })

def get_absolute_path_to_project():
    return os.path.dirname(os.path.abspath(__file__)).replace('\\web', '').replace('\\', '/')

def api_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        stay_logged_in = request.POST.get('stayloggedIn')

        if stay_logged_in != "true":
            request.session.set_expiry(0)

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse('Success')
            else:
                return HttpResponse('inactive user')
        else:
            return HttpResponse('Bad request')

def user_cabinet(request):
    return render(request, 'user_cabinet.html') 