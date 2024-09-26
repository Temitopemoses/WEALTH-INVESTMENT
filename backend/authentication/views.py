from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib import messages

User = get_user_model()

# Create your views here.

def login(request):

  if request.method == 'POST':
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    print(username, password)
    user = auth.authenticate(username=username, password=password)
        
    if user is not None:
        print(username, password)
        auth.login(request, user)
        print('logged in')
        return redirect('dashboard')
    
    else:
        print('not logged in')
        print(username, password)
        messages.error(request, 'Incorrect Username or Password')
        type = 'danger'
        context = {"type": type}
        return render(request, 'auth/login.html', context)
    
  return render(request, 'auth/login.html')

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
        user.save()
        return redirect("dashboard")
    
    else:
      messages.error(request, 'Password Does Not Match!')
      type = 'danger'
      context = {"type": type}
      return render(request, "auth/signup.html", context=context)
    
  return render(request, 'auth/signup.html')



def logout(request):
    auth.logout(request)
    return redirect("login")