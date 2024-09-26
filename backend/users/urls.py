from django.urls import path

from .views import dashboard, deposit, transaction, withdraw

urlpatterns = [
  path('dashboard/', name='dashboard', view=dashboard),
  path('deposit/', name='deposit', view=deposit),
  path('transactions/', name='transaction', view=transaction),
  path('withdraw/', name='withdraw', view=withdraw),
]