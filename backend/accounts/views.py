from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect
from coinbase_commerce.client import Client
from coinbase.wallet.client import Client as WalletClient
from .models import Transaction, Wallet, Cryptocurrency, User
from django.utils import timezone
from decimal import Decimal
from requests.exceptions import ConnectionError
from django.core.mail import send_mail

# Create your views here.

User = get_user_model()
client = Client(api_key=settings.COINBASE_API_KEY)
wallet_client = WalletClient(api_secret=settings.COINBASE_API_KEY, api_key=settings.COINBASE_API_KEY)
print(settings.COINBASE_API_KEY)

@login_required
def dashboard(request):

  user = request.user
  wallet = Wallet.objects.get(user=user)
  print(f"User acct balance ${wallet.balance}")
  balance = str(wallet.balance)
  print(balance)
  context = {wallet: "wallet", balance: "balance"}
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
      messages.success(request, 'Your profile has been updated successfully!')
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
   transaction_id = request.POST.get('transaction_id', None)

   if transaction_id == None:
      type = 'danger'
      context = {"type": type}
      messages.error(request, 'Please enter Transaction ID.')
      return redirect('deposit')

   if plan == None:
      type = 'danger'
      context = {"type": type}
      messages.error(request, 'Please select a Plan.')
      return redirect('deposit')
   
   if transaction_id is not None and Transaction.objects.filter(transaction_id=transaction_id).exists():
      type = 'danger'
      context = {"type": type}
      messages.error(request, 'Oops!. A transaction with the transaction ID provided already exists. Please check again or try again later after 1 hour')
      return redirect('deposit')


   company_name = "Wealth Wise Investments"
   
   try:
      crypto_instance = Cryptocurrency.objects.get(symbol=crypto)  # Replace with the actual crypto selected by user
      # Create Transaction with charge_id
      transaction = Transaction.objects.create(
         user=request.user,
         crypto=crypto_instance,
         transaction_type=Transaction.DEPOSIT,
         amount=amount,
         plan=plan,
         status=Transaction.PENDING,
         transaction_id=transaction_id
      )

      # Send email to admin for manual verification
      admin_email = settings.ADMIN_EMAIL 
      print(admin_email)
      subject = f"New Deposit Request for Manual Verification - {company_name}"
      message = (f"User: {request.user.username}\n"
                  f"Email: {request.user.email}\n"
                  f"Plan: {plan}\n"
                  f"Amount: ${amount}\n"
                  f"Transaction ID: {transaction_id}\n\n"
                  f"Please verify the transaction ID and update the status here http://127.0.0.1:8000/admin/accounts/transaction/.")

      send_mail(
         subject,
         message,
         settings.DEFAULT_FROM_EMAIL,
         admin_email,
         fail_silently=False,
      )

      type = 'info'
      context = {"type": type}
      messages.success(request, 'Your deposit request has been submitted for verification. You will be notified once it is confirmed.')
      return render(request, 'account/deposit.html')
   
   except Exception as e:
      print(f"Error creating charge: {e}")
      messages.error(request, f'Failed to initiate deposit. {e} Please try again later.')
      type = 'danger'
      context = {"type": type}
      return render(request, 'account/deposit.html', context)


   # try:

   #    charge_data = {
   #       'name': f"Investment Deposit for {plan}",
   #       'description': f"Crypto investment deposit for your {plan} on {request.META['REMOTE_ADDR']}",
   #       'local_price': {
   #             'amount': str(amount),  # Convert Decimal to string
   #             'currency': 'USD'  # Assuming payment in USD; update if dynamic currency needed
   #       },
   #       'pricing_type': 'fixed_price'
   #    }
   #    charge = client.charge.create(**charge_data)

   #    # Create Transaction with charge_id
   #    transaction = Transaction.objects.create(
   #       user=request.user,
   #       crypto=crypto_instance,
   #       transaction_type=Transaction.DEPOSIT,
   #       amount=amount,
   #       status=Transaction.PENDING,
   #       charge_id=charge['id'],  # Store Coinbase charge ID
   #       payment_id=charge['id']
   #    )

   #    return redirect(charge['hosted_url'])
   
   # except Exception as e:
   #    print(f"Error creating charge: {e}")
   #    messages.error(request, 'Failed to initiate deposit. Please try again later.')
   #    type = 'danger'
   #    context = {"type": type}
   #    return render(request, 'account/deposit.html', context)

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



@login_required
def withdraw(request):
    if request.method == 'POST':
        amount = float(request.POST.get('amount'))
        wallet_address = request.POST.get('wallet_address')
        
        try:
            # user_wallet = Wallet.objects.get(user=request.user)
            # if user_wallet.balance < amount:
            #     messages.error(request, "Insufficient balance.")
            #     return redirect('withdraw')

            # Deduct balance first for immediate feedback; set transaction as pending
            # user_wallet.balance -= decimal.Decimal(amount)
            # user_wallet.save()

            # Record the withdrawal transaction
            transaction = Transaction.objects.create(
                user=request.user,
                transaction_type=Transaction.WITHDRAWAL,
                amount=amount,
                status="PENDING",
               #  crypto=user_wallet.currency
            )

            # Initiate withdrawal via Coinbase API
            withdrawal = wallet_client.send_money(
               #  user_wallet.currency,
                to=wallet_address,
                amount=str(amount),
                currency="BTC",  # Assuming BTC; adjust based on user's wallet currency
                description="User withdrawal"
            )

            # Update transaction status based on API response
            transaction.status = "COMPLETED" if withdrawal['status'] == 'completed' else "FAILED"
            transaction.save()

            messages.success(request, "Withdrawal initiated successfully.")
            return redirect('withdraw')

        except Exception as e:
            # Rollback user balance if withdrawal fails
            # user_wallet.balance += decimal.Decimal(amount)
            # user_wallet.save()
            print(f"Withdrawal error: {e}")
            messages.error(request, "Failed to process withdrawal. Please try again later.")

    return render(request, 'account/withdraw.html')



def transfer(request):
   return render(request, "account/transfer.html")