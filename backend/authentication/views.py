from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import update_last_login
from django.contrib import auth
from django.contrib import messages
from django.views import View

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
      user = authenticate(request, username=username, password=password)
      
      print(user)
      if user is not None:
          # print(username, password)
          login(request, user)
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
          username=username, email=email, 
          password=password, first_name=first_name, 
          last_name=last_name, secret_question=secret_question, 
          secret_question_answer=secret_question_answer)
        
        user.is_active = True
        user.save()
      
        # Use the backend parameter when logging in
        login(request, user, backend='authentication.CustomAuthenticationBackend')  # Replace with your actual backend

        update_last_login(None, user)
        return redirect("dashboard")
    
    else:
      messages.error(request, 'Password Does Not Match!')
      type = 'danger'
      context = {"type": type}
      return render(request, "auth/signup.html", context=context)
    
  return render(request, 'auth/signup.html')



def Logout(request):
  logout(request)
  return redirect('login')  # Redirect after logout