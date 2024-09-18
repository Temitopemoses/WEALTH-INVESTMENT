# Import necessary modules and classes from Django
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from django.utils import timezone

# Import custom user manager and JWT token generation
from .managers import CustomUserManager

# Define the User model with custom fields and methods
class User(AbstractBaseUser, PermissionsMixin):
    # Email field is required and must be unique, it serves as the username field
    email = models.EmailField(max_length=255, unique=True, verbose_name=_("Email Address"))
    username = models.CharField(max_length=15, unique=True, verbose_name=_("Username"))
    # First, last name and phone number fields
    first_name = models.CharField(max_length=20, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=20, verbose_name=_("Last Name"))
    secret_question = models.CharField(max_length=25)
    secret_question_answer = models.CharField(max_length=25)
    # Boolean flags to indicate account activity and verification status
    is_active = models.BooleanField(default=False)
    # Flags to determine staff and superuser roles
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # Timestamps for when the user joined and last logged in
    date_joined = models.DateTimeField(auto_now_add=True)
    last_logged_in = models.DateTimeField(auto_now=True)
    
    # Specify the authentication field and required fields during registration
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email', "first_name", "last_name"]

    # Custom manager for handling user queries
    objects = CustomUserManager()

    # String representation of the user
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    # Property to get the full name of the user
    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"