from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

from django import forms


from django import forms
from django.core.exceptions import ValidationError


class PhoneNumberForm(forms.Form):
    COUNTRY_CHOICES = [
        ("+7", "Russia (+7)"),
        ("+375", "Belarus (+375)"),
    ]

    country_code = forms.ChoiceField(
        choices=COUNTRY_CHOICES,
        label="Country Code",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    phone_number = forms.CharField(
        max_length=15,
        label="Phone Number",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone Number"}),
    )

    # checking if phone number contains only digits and length from 7 to 15
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if not phone_number.isdigit():
            raise ValidationError("Phone number must contain only digits.")
        if len(phone_number) < 7 or len(phone_number) > 15:
            raise ValidationError("Phone number must be between 7 and 15 digits.")
        return phone_number


# Form for entering the confirmation code
class AuthCodeForm(forms.Form):
    auth_code = forms.CharField(
        max_length=4,
        label="Authentication Code",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Authentication Code"}),
    )


# Form for entering the Invite code
class InviteCodeForm(forms.Form):
    invite_code = forms.CharField(
        max_length=6,
        label="Invite Code",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Invite Code"}),
    )


# Form for editing user-email and username
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}),
        }
