"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),

    # URL path for authorization and authentication
    path('', include('authentication.urls')),
    
    # # URL path for dashboard activities and authentication
    # path('user/', include('users.urls')),

    # URL path for accounts activities and authentication
    path('user/', include('accounts.urls')),

    # Explicitly serve favicon.ico at the root
    path('favicon.ico', RedirectView.as_view(url='/static/img/logo.png', permanent=True)),
]
