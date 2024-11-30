from django.shortcuts import render
from .forms import LoginUserForm
from django.contrib.auth.views import LoginView

# Create your views here.


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "users/login.html"
