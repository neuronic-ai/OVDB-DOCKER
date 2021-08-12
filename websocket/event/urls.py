from django.urls import path
from .views import *

urlpatterns = [
    path('notify_event', notify_event, name='notify_event'),
]
