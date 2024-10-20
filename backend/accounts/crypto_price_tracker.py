import requests
from .models import Cryptocurrency

COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"

def update_crypto_prices():
    # Define the list of cryptocurrency symbols you want to track
    symbols = ['bitcoin', 'ethereum', 'litecoin', 'dogecoin']
    params = {
        'ids': ','.join(symbols),
        'vs_currencies': 'usd'
    }
    
    response = requests.get(COINGECKO_API_URL, params=params)
    if response.status_code == 200:
        prices = response.json()
        for symbol in symbols:
            crypto = Cryptocurrency.objects.get(symbol=symbol.upper())
            crypto.price_usd = prices[symbol]['usd']
            crypto.save()
    else:
        raise Exception(f"Error fetching crypto prices: {response.status_code}")
