from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import timedelta, datetime, date
import calendar
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse

from calendarapp.models import EventMember, Event
from calendarapp.utils import Calendar
from calendarapp.forms import MeetingForm, AddMemberForm
from web.models import Admin, Meeting, Prisoner, Record, CorrectionalWork


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month


class CalendarView(LoginRequiredMixin, generic.ListView):
    login_url = "home"
    model = Meeting
    template_name = "calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)
        return context


@login_required(login_url="home")
def create_event(request):
    form = MeetingForm(request.POST or None)
    if request.POST and form.is_valid():
        meetingcol = form.cleaned_data["meetingcol"]
        theme = form.cleaned_data["theme"]
        start_time = form.cleaned_data["start_time"]
        end_time = form.cleaned_data["end_time"]
        admin = Admin.objects.get(user=request.user)
        Meeting.objects.get_or_create(
            admin=admin,
            theme=theme,
            meetingcol=meetingcol,
            start_time=start_time,
            end_time=end_time,
        )
        return HttpResponseRedirect(reverse("calendarapp:calendars"))
    return render(request, "event.html", {"form": form})


class EventEdit(generic.UpdateView):
    model = Meeting
    fields = ["meetingcol", "theme", "start_time", "end_time"]
    template_name = "event.html"

    def get_success_url(self):
        return reverse("calendarapp:calendars")


@login_required(login_url="home")
def event_details(request, event_id):
    meeting = Meeting.objects.get(id=event_id)
    prisoners = Prisoner.objects.filter(meeting=meeting)
    context = {"meeting": meeting, "prisoners": prisoners}
    return render(request, "event-details.html", context)


def add_eventmember(request, event_id):
    meeting = Meeting.objects.get(id=event_id)
    forms = AddMemberForm()
    if request.method == "POST":
        forms = AddMemberForm(request.POST, instance=meeting)
        if forms.is_valid():
            prisoners = Prisoner.objects.filter(meeting=meeting)
            if prisoners.count() <= 9:
                user = forms.cleaned_data["user"]
                prisoner = Prisoner.objects.get(user=user)
                prisoner.meeting.add(meeting)
                return redirect("calendarapp:calendars")
            else:
                print("--------------User limit exceed!-----------------")
    context = {"form": forms}
    return render(request, "add_member.html", context)


class EventMemberDeleteView(generic.DeleteView):
    model = Prisoner
    template_name = "event_delete.html"
    success_url = reverse_lazy("calendarapp:calendars")


class CalendarViewNew(LoginRequiredMixin, generic.View):
    login_url = "login"
    template_name = "calendarapp/calendar.html"
    form_class = MeetingForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        events = Event.objects.get_all_events(user=request.user)
        events_month = Event.objects.get_running_events(user=request.user)
        event_list = []
        # start: '2020-09-16T16:00:00'
        for event in events:
            event_list.append(
                {
                    "title": event.title,
                    "start": event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),

                }
            )
        context = {"form": forms, "events": event_list,
                   "events_month": events_month}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            form = forms.save(commit=False)
            form.user = request.user
            form.save()
            return redirect("calendarapp:calendar")
        context = {"form": forms}
        return render(request, self.template_name, context)
