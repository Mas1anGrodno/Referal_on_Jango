from django.urls import path
from . import views
from .views.api_views import *
from .views.regular_views import *
from users.swagger import schema_view

urlpatterns = [
    path("enter/", views.phone_number_view, name="phone_number"),
    path("verify-code/", views.auth_code_view, name="verify_code"),
    path("profile/", views.profile_view, name="profile"),
    # ----------------------------------API----------------------------------
    path("api/profile-referals/", views.ProfileReferralsAPIView.as_view(), name="api_profile"),
    path("api/profile-referals/<int:id>/", views.ProfileReferralsAPIView.as_view(), name="api_profile_referals_by_id"),
    path("api/user/", views.UserDetailAPIView.as_view(), name="api_user_detail"),
    path("api/user/<int:id>/", views.UserDetailByIdAPIView.as_view(), name="api_user_detail_by_id"),
    path("api/phone-number/create/", views.PhoneNumberVerificationCreateAPIView.as_view(), name="phone_number_create"),
    path("api/phone-number/update/<str:phone_number>/", views.PhoneNumberVerificationUpdateAPIView.as_view(), name="phone_number_update"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]
