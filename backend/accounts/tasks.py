from celery import shared_task
from .crypto_price_tracker import update_crypto_prices

@shared_task
def fetch_crypto_prices_task():
    update_crypto_prices()


from django.conf import settings
from coinbase_commerce.client import Client
from .models import Transaction, Wallet
from decimal import Decimal

client = Client(api_key=settings.COINBASE_API_KEY)

@shared_task
def update_pending_transactions():
    pending_transactions = Transaction.objects.filter(status=Transaction.PENDING)
    
    for transaction in pending_transactions:
        try:
            charge = client.charge.retrieve(transaction.charge_id)
            status = charge['timeline'][-1]['status']
            transaction.status = status
            transaction.save()
            
            if status == 'COMPLETED':
                wallet, _ = Wallet.objects.get_or_create(user=transaction.user, crypto=transaction.crypto)
                wallet.balance += transaction.amount
                wallet.save()
                
        except Exception as e:
            print(f"Error updating transaction {transaction.id}: {e}")
