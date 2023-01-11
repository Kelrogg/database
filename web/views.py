import os
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import generic
from django.urls import reverse_lazy
from .models import Admin
from .models import User
from .forms import TreatmentForm

from .LabelDecoder import decode_label_detail

from .forms import SignUpForm, PersonalData


LOGIN_URL = 'login'

class SignUpUser(generic.edit.CreateView):
    form_class = SignUpForm
    template_name = 'registration/sign_up.html'
    def get_success_url(self):
        return reverse_lazy('login')

@login_required(login_url=LOGIN_URL)
def cabinet_view(request):
    if request.method == "POST":
        form = PersonalData(request.POST, request.FILES)
        if form.is_valid():
            doctor = request.user.doctor
            doctor.full_name = form.cleaned_data['full_name']
            doctor.qualification = form.cleaned_data['qualification']
            doctor.experience = form.cleaned_data['experience']
            doctor.work_place = form.cleaned_data['work_place']
            doctor.education = form.cleaned_data['education']
            doctor.contacts = form.cleaned_data['contacts']
            if form.cleaned_data['image']:
                doctor.photo = form.cleaned_data['image']
            doctor.save()

    doctor = request.user.doctor
    data = {
        'full_name': doctor.full_name,
        'qualification': doctor.qualification,
        'work_place': doctor.work_place,
        'education': doctor.education,
        'experience': doctor.experience,
        'contacts': doctor.contacts,
        'photo': doctor.photo,
    }
    form = PersonalData(data)

    def get_queryset():
        search_query = request.GET.get('q')
        search_query = search_query if search_query else ''
        return reversed(Treatment.objects.filter(
            Q(doctor=doctor) & Q(user__full_name__icontains=search_query)
        ).all())

    return render(request, 'cabinet.html',
                  context={'header': 'Личный кабинет',
                           'doctor': request.user.doctor,
                           'form': form,
                           'history': get_queryset,
                           })

def treatment_form_view(request):
    if request.method == 'POST':
        form = TreatmentForm(request.POST, request.FILES)

        if form.is_valid():
            user = User()
            
            user.full_name = form.cleaned_data['full_name']
            user.age = form.cleaned_data['age']
            user.save()
    else:
        form = TreatmentForm()

    return render(request, 'treatment_form.html', {'form': form})



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