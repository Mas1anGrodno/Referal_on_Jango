from django.urls import path
from . import views
from users.swagger import schema_view

urlpatterns = [
    path("enter/", views.phone_number_view, name="phone_number"),
    path("verify-code/", views.auth_code_view, name="verify_code"),
    path("profile/", views.profile_view, name="profile"),
    path("api/profile/", views.ProfileAPIView.as_view(), name="api_profile"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]
