from django.urls import path

from . import views
from .views.other_views import MeetingDeleteView

app_name = 'calendarapp'


urlpatterns = [
    path('calender/', views.CalendarViewNew.as_view(), name='calendar'),
    path('calenders/', views.CalendarView.as_view(), name='calendars'),
    path('event/new/', views.create_event, name='event_new'),
    path('event/edit/<int:pk>/', views.EventEdit.as_view(), name='event_edit'),
    path('event/<int:event_id>/details/', views.event_details, name='event-detail'),
    path(
        'add_eventmember/<int:event_id>', views.add_eventmember, name='add_eventmember'
    ),
    path(
        'event/<int:pk>/remove_member',
        views.EventMemberDeleteView.as_view(),
        name='remove_prisoner',
    ),
    path(
        'event/<int:pk>/remove_event',
        MeetingDeleteView.as_view(),
        name='remove_meeting',
    ),
    path('all-event-list/', views.AllEventsListView.as_view(), name='all_events'),
    path(
        'running-event-list/',
        views.RunningEventsListView.as_view(),
        name='running_events',
    ),
]
