from django.urls import path

from .views import dashboard, deposit, transaction, withdraw, userProfile, transfer

urlpatterns = [
  path('dashboard/', name='dashboard', view=dashboard),
  path('profile/', name='profile', view=userProfile),
  path('deposit/', name='deposit', view=deposit),
  path('transactions/', name='transaction', view=transaction),
  path('withdraw/', name='withdraw', view=withdraw),
  path('transfer/', name='transfer', view=transfer),
]