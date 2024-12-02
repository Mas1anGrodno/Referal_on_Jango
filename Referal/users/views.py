from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from .models import PhoneNumberVerification
from .forms import PhoneNumberForm, AuthCodeForm, InviteCodeForm, ProfileForm
import random
from time import sleep

# ----------------------------------API----------------------------------
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated
from .serializers import PhoneNumberVerificationSerializer, UserSerializer


User = get_user_model()


def phone_number_view(request):
    if request.method == "POST":
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            country_code = form.cleaned_data["country_code"]
            phone_number = form.cleaned_data["phone_number"]
            code = str(random.randint(1000, 9999))
            # Сохранение кода в сессии
            request.session["auth_code"] = code
            # Printing code to console
            print(code)
            phone_verification, created = PhoneNumberVerification.objects.get_or_create(phone_number=phone_number, defaults={"country_code": country_code})
            if not created:
                phone_verification.country_code = country_code
            phone_verification.auth_code = code
            phone_verification.save()

            # Имитируем отправку кода с задержкой
            sleep(2)

            # Перенаправляем пользователя на ввод кода
            return redirect("verify_code")
    else:
        form = PhoneNumberForm()
    return render(request, "users/phone_number.html", {"form": form})


def auth_code_view(request):
    auth_code = request.session.get("auth_code", None)  # Получение кода из сессии
    if request.method == "POST":
        form = AuthCodeForm(request.POST)
        if form.is_valid():
            input_code = form.cleaned_data["auth_code"]
            try:
                phone_verification = PhoneNumberVerification.objects.get(auth_code=input_code)
                if phone_verification.user is None:
                    user = User.objects.create_user(username=phone_verification.phone_number)
                    phone_verification.user = user
                    phone_verification.save()
                    login(request, user)
                else:
                    user = phone_verification.user
                    login(request, user)

                # Получение данных пользователя
                user_data = {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "phone_number": phone_verification.phone_number,
                    "referal_number": phone_verification.referal_number,
                    "activated_referal_number": phone_verification.activated_referal_number,
                }
                return render(request, "users/user_data.html", user_data)
            except PhoneNumberVerification.DoesNotExist:
                form.add_error("auth_code", "Invalid code")
    else:
        form = AuthCodeForm()
    return render(request, "users/auth_code.html", {"form": form, "auth_code": auth_code})


def profile_view(request):
    user = request.user
    phone_verification = PhoneNumberVerification.objects.get(user=user)
    invite_form = InviteCodeForm(request.POST or None)
    profile_form = ProfileForm(request.POST or None, instance=user)

    if request.method == "POST":
        if invite_form.is_valid():
            invite_code = invite_form.cleaned_data["invite_code"]
            if PhoneNumberVerification.objects.filter(referal_number=invite_code).exists() and not phone_verification.activated_referal_number:
                phone_verification.activated_referal_number = invite_code
                phone_verification.save()
                return redirect("profile")
            else:
                invite_form.add_error("invite_code", "Invalid or already activated invite code")
        if profile_form.is_valid():
            profile_form.save()
            return redirect("profile")

    profile_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "phone_number": phone_verification.phone_number,
        "referal_number": phone_verification.referal_number,
        "activated_referal_number": phone_verification.activated_referal_number,
        "invite_form": invite_form,
        "profile_form": profile_form,
    }
    return render(request, "users/profile.html", profile_data)


# ----------------------------------API----------------------------------


class UserDetailAPIView(generics.RetrieveAPIView):
    # permission classes swiched to AllowAny for testing
    permission_classes = [permissions.AllowAny]
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ProfileReferralsAPIView(generics.GenericAPIView):
    # permission classes swiched to AllowAny for testing
    permission_classes = [permissions.AllowAny]
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = PhoneNumberVerificationSerializer

    def get(self, request, *args, **kwargs):
        if getattr(self, "swagger_fake_view", False):
            return Response()  # нужно для корректной генерации схемы

        user_id = kwargs.get("id")
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise NotFound(detail="User not found.")
        else:
            user = request.user
            if not user.is_authenticated:
                return Response({"detail": "You must use the endpoint with user ID: /api/profile-referals/<int:id>/"}, status=status.HTTP_403_FORBIDDEN)

        phone_verification = PhoneNumberVerification.objects.get(user=user)

        # Получаем список пользователей, которые использовали инвайт-код указанного пользователя
        invited_users = PhoneNumberVerification.objects.filter(activated_referal_number=phone_verification.referal_number)
        serializer = PhoneNumberVerificationSerializer(invited_users, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        user_id = self.kwargs.get("id")
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise NotFound(detail="User not found.")
        else:
            user = self.request.user
            if not user.is_authenticated:
                raise NotAuthenticated(detail="Authentication credentials were not provided.")

        phone_verification = PhoneNumberVerification.objects.get(user=user)
        return PhoneNumberVerification.objects.filter(activated_referal_number=phone_verification.referal_number)


class PhoneNumberVerificationCreateAPIView(generics.CreateAPIView):
    # permission classes swiched to AllowAny for testing
    permission_classes = [permissions.AllowAny]
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = PhoneNumberVerificationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PhoneNumberVerificationUpdateAPIView(generics.UpdateAPIView):
    # permission classes swiched to AllowAny for testing
    permission_classes = [permissions.AllowAny]
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = PhoneNumberVerificationSerializer
    lookup_field = "phone_number"

    def get_queryset(self):
        return PhoneNumberVerification.objects.all()
