from django.urls import reverse, path
from .views import login, signup

urlpatterns = [
    path('login/', view=login, name='login'),
    path('signup/', view=signup, name='signup'),
]