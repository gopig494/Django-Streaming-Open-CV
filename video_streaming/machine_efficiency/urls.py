from django.urls import path
from machine_efficiency.api import *


urlpatterns = [
    path("api/get_machine_efficiency/",get_machine_efficiency, name="get_machine_efficiency")
]
