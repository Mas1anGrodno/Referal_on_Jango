from django.db import models
from django.contrib.auth.models import User
import random
import string


# Function to generate 6 random symbols
def generate_unique_code():
    return "".join(random.choices(string.ascii_letters + string.digits, k=6))


# Create new model for phone verification
class PhoneNumberVerification(models.Model):
    # Creating OneToOne connection to standard model User
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    # Making phone unique - 15 digits length
    phone_number = models.CharField(max_length=15, unique=True)
    # Empty field for 4 digith auth code
    auth_code = models.CharField(max_length=4, blank=True)
    # unique referal number 6 symbols long
    referal_number = models.CharField(max_length=6, unique=True, default=generate_unique_code)

    def __str__(self):
        return self.phone_number
