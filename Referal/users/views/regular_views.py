# users/views/regular_views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from users.models import PhoneNumberVerification
from users.forms import PhoneNumberForm, AuthCodeForm, InviteCodeForm, ProfileForm
import random
from time import sleep


User = get_user_model()


def phone_number_view(request):
    if request.method == "POST":
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            country_code = form.cleaned_data["country_code"]
            phone_number = form.cleaned_data["phone_number"]
            code = str(random.randint(1000, 9999))
            # Saving code in session
            request.session["auth_code"] = code
            # Printing code to console
            print(code)
            phone_verification, created = PhoneNumberVerification.objects.get_or_create(phone_number=phone_number, defaults={"country_code": country_code})
            if not created:
                phone_verification.country_code = country_code
            phone_verification.auth_code = code
            phone_verification.save()

            # Simulate sending code with a delay 2 sec
            sleep(2)

            # Redirect the user to enter the code
            return redirect("verify_code")
    else:
        form = PhoneNumberForm()
    return render(request, "users/phone_number.html", {"form": form})


def auth_code_view(request):
    auth_code = request.session.get("auth_code", None)  # Getting code from session
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

                # Getting user data
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
