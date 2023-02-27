import os
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
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
from django.shortcuts import resolve_url, get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from .models import Admin, User, Prisoner
from .forms import PrisonerSignUpForm
from .decorators import admin_required
from .LabelDecoder import decode_label_detail

from .forms import SignUpForm, LoginUserForm

from calendarapp.models import Event

LOGIN_URL = 'login'

class SignUpAdmin(generic.edit.CreateView):
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
        login(self.request, user)
        return redirect('admin_cabinet')

class LoginUser(LoginView):
    model = User
    form_class = LoginUserForm
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy('user_cabinet')
    
    def form_valid(self, form):
        login(self.request, form.get_user())
        user = form.get_user()
        if user.is_staff:
             return redirect('admin_cabinet')
        else:
             return redirect('user_cabinet')

#@admin_required
class SignUpPrisoner(generic.edit.CreateView):
    model = User
    form_class = PrisonerSignUpForm
    template_name = 'registration/sign_up_prisoner.html'
    
    def get_succes_url(self):
        return reverse_lazy('user_cabinet')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
         'user': self.request.user,
        })
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'prisoner'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.save()
        return redirect('admin_cabinet')

# class EditPrisoner(generic.edit.UpdateView):
#     model = Prisoner
#     form_class = 

def get_absolute_path_to_project():
    return os.path.dirname(os.path.abspath(__file__)).replace('\\web', '').replace('\\', '/')

def logout_user(request):
    logout(request)
    return redirect('home')

class admin_info_cabinet(generic.list.ListView):
    model = Admin
    template_name = 'admin_cabinet.html'
    context_object_name = 'context'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user=self.request.user
        admin = Admin.objects.get(user=user)
        context['rank'] = admin.rank
        context['gender'] = admin.gender
        context['birthday'] = admin.birthday
        context['image'] = user.image
        return context
    
    def get_queryset(self):
        admin = Admin.objects.get(user=self.request.user)
        return Prisoner.objects.filter(admin=admin)

class prisoner_info_cabinet(generic.list.ListView):
    model = Prisoner
    template_name = 'user_cabinet.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user=self.request.user
        prisoner = Prisoner.objects.get(user=user)
        context['gender'] = prisoner.gender
        context['birthday'] = prisoner.birthday
        context['image'] = user.image
        return context

class DashboardView(LoginRequiredMixin, View):
    template_name = "calendarapp/dashboard.html"

    def get(self, request, *args, **kwargs):
        events = Event.objects.get_all_events(user=request.user)
        running_events = Event.objects.get_running_events(user=request.user)
        latest_events = Event.objects.filter(user=request.user).order_by("-id")[:10]
        context = {
            "total_event": events.count(),
            "running_events": running_events,
            "latest_events": latest_events,
        }
        return render(request, self.template_name, context)