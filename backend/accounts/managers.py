from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User
# from authentication.views import Wallet

from django.apps import apps

class CustomUserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("Please enter a valid email address"))
        
    def create_user(self, email, username, first_name, last_name, password, **extra_fields):
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)  # This will raise a ValueError if the email is invalid
        else: 
            raise ValueError(_("An email address is required"))
        
        # Check if user already exists
        if get_user_model().objects.filter(username=username).exists():
            raise ValueError(_("A user with this username already exists."))

        if not first_name:
            raise ValueError(_("First name is required"))
        if not last_name:
            raise ValueError(_("Last name is required"))
        if not username:
            raise ValueError(_("Username is required"))
        if not email:
            raise ValueError(_("Email is required"))
        
        user = self.model(email=email, username=username, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, email, username, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        # extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("is staff must be for admin user"))
        
        if extra_fields.get("is_superuser") is not True: 
            raise ValueError(_("is superuser must be for admin user"))

        if extra_fields.get("is_active") is not True:
            raise ValueError(_("is active must be for admin user"))
        
        # Check if user already exists
        if get_user_model().objects.filter(username=username).exists():
            raise ValueError(_("A user with this username already exists."))
        # print(email)

        user = self.create_user(email=email, username=username, first_name=first_name, last_name=last_name, password=password, **extra_fields)
        user.save(using=self.db)
        Wallet = apps.get_model('accounts', 'Wallet')
        user_wallet = Wallet.objects.create(user=user)
        user_wallet.save()
        return user
