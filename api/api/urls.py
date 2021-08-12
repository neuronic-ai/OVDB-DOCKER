from django.urls import path
from .views import *

urlpatterns = [
    path('<str:param1>/<str:param2>', process_api, name='webhook'),
]
