from django.urls import reverse, path
from .views import login, signup, logout
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.Homepage.as_view(), name='homepage'),
    path('about-us/', views.About.as_view(), name="about"),
    path('support/', views.Support.as_view(), name="support"),
    path('investment-plans/', views.Investment.as_view(), name="investment"),
    path('policy/', views.Policy.as_view(), name="policy"),
    path('accounts/auth/login/', views.LoginView.as_view(), name='login'),
    path('accounts/auth/signup/', view=signup, name='signup'),
    path('accounts/auth/logout/', views.Logout, name='logout'),
]