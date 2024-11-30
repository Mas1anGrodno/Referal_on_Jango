from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


# Form for entering a phone number
class PhoneNumberForm(forms.Form):
    phone_number = forms.CharField(
        max_length=15,
        label="Phone Number",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone Number"}),
    )


# Form for entering the confirmation code
class AuthCodeForm(forms.Form):
    auth_code = forms.CharField(
        max_length=4,
        label="Authentication Code",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Authentication Code"}),
    )


class InviteCodeForm(forms.Form):
    invite_code = forms.CharField(
        max_length=6,
        label="Invite Code",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Invite Code"}),
    )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}),
        }
