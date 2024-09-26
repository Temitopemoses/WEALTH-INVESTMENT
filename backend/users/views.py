from django.shortcuts import render
from django.contrib.auth import get_user_model
# Create your views here.

User = get_user_model()

def dashboard(request):
  return render(request, 'dashboard.html')


def deposit(request):
  return render(request, 'deposit.html')


def transaction(request):
  return render(request, 'transaction.html')


def withdraw(request):
  return render(request, 'withdraw.html')