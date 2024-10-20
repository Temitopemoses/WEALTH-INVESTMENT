from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from django.conf import settings

from .models import Cryptocurrency, Wallet, Transaction
# Create your views here.

User = get_user_model()
# Wallet = Wallet.objects.get()

@login_required(redirect_field_name='next', login_url='/auth/login/')
def dashboard(request):
  user = request.user
  wallet = Wallet.objects.get(user=user)
  print(f"User acct balance ${wallet.balance}")
  context = {wallet: "wallet"}
  return render(request, 'dashboard.html', context)

# @login_required(redirect_field_name='next', login_url='/auth/login/')
def deposit(request):
  if not request.user.is_authenticated:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
  return render(request, 'deposit.html')


def transaction(request):
  return render(request, 'transaction.html')


def withdraw(request):
  return render(request, 'withdraw.html')