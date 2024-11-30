from django.urls import path
from . import views

urlpatterns = [
    path("enter/", views.phone_number_view, name="phone_number"),
    path("verify-code/", views.auth_code_view, name="verify_code"),
    path("profile/", views.profile_view, name="profile"),
]
