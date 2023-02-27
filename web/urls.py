from django.conf.urls import url
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import logout_user, DashboardView

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name= 'home'),
    path('signup/', views.SignUpAdmin.as_view(), name='sign_up'),
    path('signup-prisoner/', views.SignUpPrisoner.as_view(), name='sign_up_prisoner'),
    path('user-cabinet/', views.prisoner_info_cabinet.as_view(), name='user_cabinet'),
    path('admin-cabinet/', views.admin_info_cabinet.as_view(), name='admin_cabinet'),
    # path('edit-prisoner/', views.EditPrisoner(), name='edit_prisoner'),
    path('', include('django.contrib.auth.urls')),
    path('', include('calendarapp.urls')),
    path("calendar", DashboardView.as_view(), name="dashboard"),

    url(r'^logout/$', logout_user, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
