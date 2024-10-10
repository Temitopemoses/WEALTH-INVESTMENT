from django.urls import reverse, path
from .views import login, signup, logout
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', view=signup, name='signup'),
    path('logout/', views.Logout, name='logout'),
]