from celery import shared_task
from .crypto_price_tracker import update_crypto_prices

@shared_task
def fetch_crypto_prices_task():
    update_crypto_prices()
