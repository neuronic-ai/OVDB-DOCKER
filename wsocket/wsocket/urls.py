from django.urls import path
from .views import *

urlpatterns = [
    path('send_command', send_command, name='send_command')
]
