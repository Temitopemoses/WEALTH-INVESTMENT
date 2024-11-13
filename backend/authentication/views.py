from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import update_last_login
from django.contrib import auth
from django.contrib import messages
from django.views import View

from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
import random
import string

from django.contrib.auth.hashers import make_password

from accounts.models import Wallet

User = get_user_model()

# Create your views here.

class Homepage(View):
  def get(self, request):
    return render(request, 'index.html')
  

class About(View):
  def get(self, request):
    return render(request, 'about.html')
  
class Investment(View):
  def get(self, request):
    return render(request, 'investment.html')
  
class Policy(View):
  def get(self, request):
    return render(request, 'policy.html')
  
class Support(View):
  def get(self, request):
    return render(request, 'support.html')

class LoginView(View):

  def get(self, request):
    return render(request, 'auth/login.html')
  
  def post(self, request):
      
      username = request.POST.get('username', '')
      password = request.POST.get('password', '')
      # print(username, password)
      user = authenticate(request, username=username.capitalize(), password=password)
      
      print(user)
      if user is not None:
          # print(username, password)
          login(request, user)
          
          # Use the backend parameter when logging in
          # login(request, user, backend='authentication.CustomAuthenticationBackend')  # Replace with your actual backend
          # login(request, user)  # Replace with your actual backend
          update_last_login(None, user)
          print('logged in')
          return redirect('dashboard')
      
      else:
          print('not logged in')
          print(username, password)
          messages.error(request, 'Incorrect Username or Password')
          type = 'danger'
          context = {"type": type}
          return render(request, 'auth/login.html', context)
      

def signup(request):

  if request.method == "POST":
    first_name = request.POST.get('first_name', '')
    last_name = request.POST.get('last_name', '')
    email = request.POST.get('email', '')
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    password_confirmation = request.POST.get('password2', '')
    secret_question = request.POST.get('secret_question', '')
    secret_question_answer = request.POST.get('secret_answer', '')
    bitcoin_address = request.POST.get('bitcoin_address', )
    usdtc_address = request.POST.get('usdtc_address', )
    ethereum_address = request.POST.get('ethereum_address', )


    if password == password_confirmation:

      if User.objects.filter(email=email).exists():
        messages.error(request,  'Email already exists')
        type = 'danger'
        context = {"type": type}
        return render(request, "auth/signup.html", context=context)
      
      elif User.objects.filter(username=username).exists():
        messages.error(request, 'Username is Taken!')
        type = 'danger'
        context = {"type": type}
        return render(request, "auth/signup.html", context=context)
      
      else:
        user = User.objects.create_user(
          username=username.capitalize(), email=email, 
          password=password, first_name=first_name.capitalize(), 
          last_name=last_name.capitalize(), bitcoin_address = bitcoin_address,
          usdtc_address = usdtc_address, ethereum_address = ethereum_address,
          secret_question=secret_question.capitalize(), secret_question_answer=secret_question_answer
        )
        
        user.is_active = True
        user.save()

        user_wallet = Wallet.objects.create(user=user)
        user_wallet.save();
        
        return redirect('login')
    
    else:
      messages.error(request, 'Password Does Not Match!')
      type = 'danger'
      context = {"type": type}
      return render(request, "auth/signup.html", context=context)
    
  return render(request, 'auth/signup.html')



def Logout(request):
  logout(request)
  return redirect('login')  # Redirect after logout




def generate_token():
    """Generate a random 6-digit token"""
    return ''.join(random.choices(string.digits, k=6))

def password_reset_request(request):

  if request.method == 'POST':

    email = request.POST.get('email', None)
    print(email)

    try:
      user = User.objects.get(email=email)
      print(user)

      if user:
        # Generate the token
        token = generate_token()

        # Store the token and user ID in session (with expiration)
        request.session['reset_token'] = token
        request.session['user_id'] = user.id
        
        # Set session expiry to 10 minutes (600 seconds)
        request.session.set_expiry(600)  # Session expires in 10 minutes

        # Send the token via email
        send_mail(
            subject='Your Password Reset Token',
            message=f'Your password reset token is: {token}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

        messages.success(request, 'A password reset token has been sent to your email.')
        return redirect('password_reset_confirm')

    except User.DoesNotExist as e:
      messages.error(request, 'No account found with the provided email or username.')
      return render(request, 'auth/password_reset_request.html')
        
  else:
     return render(request, 'auth/password_reset_request.html')



from django.contrib.auth.hashers import make_password

def password_reset_confirm(request):
    
  if request.method == 'POST':
      
    token = request.POST.get('token')
    new_password = request.POST.get('new_password')
    confirm_password = request.POST.get('confirm_password')

    # Retrieve the token and user ID from session
    session_token = request.session.get('reset_token')
    print(session_token)
    user_id = request.session.get('user_id')

    if not session_token or not user_id:
        messages.error(request, 'Session expired or invalid token.')
        return redirect('password_reset_request')

    if token == session_token:
        return redirect('setNewPassword')
    else:
        messages.error(request, 'Invalid token.')
      
    
  return render(request, 'auth/password_reset_confirm.html')


def setNewPassword(request):
   if request.method == "POST":
      
      # Retrieve the token and user ID from session
      session_token = request.session.get('reset_token')
      print(session_token)
      user_id = request.session.get('user_id')

      if not session_token or not user_id:
          messages.error(request, 'Session expired or invalid token.')
          return redirect('password_reset_request')
      
      new_password = request.POST.get('password')
      confirm_password = request.POST.get('confirm_password')

      # Check if passwords match
      if new_password == confirm_password:
          # Update the user's password
          user = User.objects.get(id=user_id)
          user.password = make_password(new_password)
          user.save()

          # Clear session data
          request.session.pop('reset_token')
          request.session.pop('user_id')

          messages.success(request, 'Your password has been reset successfully.')
          return redirect('login')
      else:
          messages.error(request, 'Passwords do not match.')

   return render(request, 'auth/reset_password.html')
