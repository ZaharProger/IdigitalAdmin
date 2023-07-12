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
import os

import dotenv
from django.contrib import admin
from django.urls import path

from ..controllers import EventController
from ..models.contexts import PyMySqlContext
from ..serializers import EventSerializer
from ..services import EventService, ImageService

dotenv.load_dotenv(dotenv.find_dotenv())

db_context = PyMySqlContext(
    db_name=os.environ['DB_NAME'],
    db_user=os.environ['DB_USER'],
    db_password=os.environ['DB_PASSWORD'],
    db_host=os.environ['DB_HOST']
)

image_service = ImageService()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/events/', EventController.as_view(
        db_context=db_context,
        event_service=EventService(),
        image_service=image_service,
        event_serializer=EventSerializer()
    ))
]
