from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect
from coinbase_commerce.client import Client
from .models import Transaction, Wallet, Cryptocurrency, User
from django.utils import timezone
from decimal import Decimal
from requests.exceptions import ConnectionError

# Create your views here.

User = get_user_model()
client = Client(api_key=settings.COINBASE_API_KEY)
print(settings.COINBASE_API_KEY)

@login_required
def dashboard(request):

  user = request.user
  wallet = Wallet.objects.get(user=user)
  print(f"User acct balance ${wallet.balance}")
  context = {wallet: "wallet"}
  return render(request, 'account/dashboard.html', context)


@login_required
def userProfile(request):
   
   if request.method == "POST":
      username = request.POST.get("username", None)
      secret_question = request.POST.get("secret_question", None)
      secret_question_answer = request.POST.get('secret_question_answer', None)
      bitcoin_address = request.POST.get('bitcoin_address', None)
      usdtc_address = request.POST.get('usdtc_address', None)
      ethereum_address = request.POST.get('ethereum_address', None)

      user = request.user
      if username:
         user.username = username.capitalize()

      if secret_question:
         user.secret_question = secret_question.capitalize()

      if secret_question_answer:
         user.secret_question_answer = secret_question_answer

      if bitcoin_address:
         user.bitcoin_address = bitcoin_address

      if usdtc_address:
         user.usdtc_address = usdtc_address

      if ethereum_address:
         user.ethereum_address = ethereum_address

      
      user.save()

      type = 'success'
      context = {"type": type}
      messages.error(request, 'Your profile has been updated successfully!')
      return render(request, "account/profile.html", context=context)

   user = request.user
   context = {"user": user}
   return render(request, 'account/profile.html', context)


@login_required
def deposit(request):

  if request.method == 'POST':
   amount = float(request.POST.get('amount'))
   plan = request.POST.get('plan', None)
   crypto = request.POST.get('crypto', None)

   print(amount)

   company_name = "Wealth Wise Investments"
   
   crypto_instance = Cryptocurrency.objects.get(symbol=crypto)  # Replace with the actual crypto selected by user
   try:

      charge_data = {
         'name': f"Investment Deposit for {plan}",
         'description': f"Crypto investment deposit for your {plan} on {request.META['REMOTE_ADDR']}",
         'local_price': {
               'amount': str(amount),  # Convert Decimal to string
               'currency': 'USD'  # Assuming payment in USD; update if dynamic currency needed
         },
         'pricing_type': 'fixed_price'
      }
      charge = client.charge.create(**charge_data)

      # Create Transaction with charge_id
      transaction = Transaction.objects.create(
         user=request.user,
         crypto=crypto_instance,
         transaction_type=Transaction.DEPOSIT,
         amount=amount,
         status=Transaction.PENDING,
         charge_id=charge['id'],  # Store Coinbase charge ID
         payment_id=charge['id']
      )

      return redirect(charge['hosted_url'])
   
   except Exception as e:
      print(f"Error creating charge: {e}")
      messages.error(request, 'Failed to initiate deposit. Please try again later.')
      type = 'danger'
      context = {"type": type}
      return render(request, 'account/deposit.html', context)

  return render(request, 'account/deposit.html')

@login_required
def transaction(request):
  transactions = Transaction.objects.filter(user=request.user)  # Using filter instead of get

  # Handle filter form submission
  if request.method == 'POST':
   transaction_type = request.POST.get('type')
   currency_type = request.POST.get('currency')
   date_from = request.POST.get('date_from')
   date_to = request.POST.get('date_to')

    # Apply filters based on form input
   if transaction_type:
      transactions = transactions.filter(transaction_type=transaction_type)
   if currency_type and currency_type != '-1':
      transactions = transactions.filter(crypto__symbol=currency_type)
   if date_from:
      transactions = transactions.filter(timestamp__gte=date_from)
   if date_to:
      transactions = transactions.filter(timestamp__lte=date_to)

  return render(request, 'account/transaction.html', {"transactions": transactions})


def withdraw(request):
  return render(request, 'account/withdraw.html')


def transfer(request):
   return render(request, "account/transfer.html")