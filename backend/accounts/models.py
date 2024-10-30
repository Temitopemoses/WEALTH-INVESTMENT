# Import necessary modules and classes from Django
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth import get_user_model

from django.utils import timezone

# Import custom user manager and JWT token generation
from .managers import CustomUserManager

# User = get_user_model()

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
    is_verified = models.BooleanField(default=False)
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



class Cryptocurrency(models.Model):
    name = models.CharField(max_length=100)  # e.g., Bitcoin, Ethereum
    symbol = models.CharField(max_length=10)  # e.g., BTC, ETH
    price_usd = models.DecimalField(max_digits=20, decimal_places=8, default=0.0)  # Store real-time price in USD
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.symbol})"
    
    class Meta:
        ordering = ("-last_updated",)
        verbose_name = 'Cryptocurrency'
        verbose_name_plural = 'Cryptocurrencies'


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE, null=True)
    balance = models.DecimalField(max_digits=20, decimal_places=8, default=0.0)  # Balance in respective crypto
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username}'s Wallet"
    
    class Meta:
        ordering = ['last_updated']



class Transaction(models.Model):
    DEPOSIT = 'Deposit'
    WITHDRAWAL = 'Withdrawal'
    TRANSACTION_TYPES = [
        (DEPOSIT, 'Deposit'),
        (WITHDRAWAL, 'Withdrawal'),
    ]
    
    PENDING = 'pending'
    SUCCESS = 'success'
    FAILED = 'failed'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (SUCCESS, 'Success'),
        (FAILED, 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    charge_id = models.CharField(max_length=100, null=True, blank=True)  # Store Coinbase charge ID
    crypto = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)  # 'BTC' or 'USDT'
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=20, decimal_places=3)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    timestamp = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)  # Store payment provider's ID


    def __str__(self):
        return f"{self.payment_id}"
    
    class Meta:
        ordering = ('-timestamp',)
        verbose_name_plural = 'Transactions'