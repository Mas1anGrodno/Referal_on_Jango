from django.urls import path
from . import views

urlpatterns = [
    path("enter/", views.phone_number_view, name="enter"),
    path("verify-code/", views.auth_code_view, name="verify_code"),
]
