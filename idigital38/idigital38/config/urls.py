"""
URL configuration for idigital38 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from django.conf import settings

from ..appointments.views import AppointmentView
from ..events.views import EventView
from ..forum_programme.views import ProgrammeDayView
from ..organizers.views import OrganizerView
from ..authorization.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/events/', EventView.as_view(), name='events'),
    path('api/organizers/', OrganizerView.as_view(), name='organizers'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/forum-programme/', ProgrammeDayView.as_view(), name='programme_days'),
    path('api/appointments/', AppointmentView.as_view(), name='appointments')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
