from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.conf import settings

from .models import Cryptocurrency, Wallet, Transaction, User
# Create your views here.

User = get_user_model()
# Wallet = Wallet.objects.get()

@login_required(redirect_field_name='next', login_url='/auth/login/')
def dashboard(request):

  user = request.user
  wallet = Wallet.objects.get(user=user)
  print(f"User acct balance ${wallet.balance}")
  context = {wallet: "wallet"}
  return render(request, 'account/dashboard.html', context)

# @login_required(redirect_field_name='next', login_url='/auth/login/')
@login_required(redirect_field_name='next', login_url='/accounts/auth/login/')
def userProfile(request):
   
   if request.method == "POST":
      username = request.POST.get("username", None)
      secret_question = request.POST.get("secret_question", None)
      secret_question_answer = request.POST.get('secret_question_answer', None)

      user = request.user
      if username:
         user.username = username

      if secret_question:
         user.secret_question = secret_question

      if secret_question_answer:
         user.secret_question_answer = secret_question_answer
      
      user.save()

      type = 'success'
      context = {"type": type}
      messages.error(request, 'Your profile has been updated successfully!')
      return render(request, "account/profile.html", context=context)

   user = request.user
   context = {"user": user}
   return render(request, 'account/profile.html', context)

def deposit(request):
  if not request.user.is_authenticated:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
  return render(request, 'account/deposit.html')


def transaction(request):
  return render(request, 'account/transaction.html')


def withdraw(request):
  return render(request, 'account/withdraw.html')