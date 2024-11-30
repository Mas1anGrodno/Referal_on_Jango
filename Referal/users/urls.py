from django.urls import path
from .views import *


urlpatterns = [
    path("", LoginUser.as_view(), name="login"),
]
