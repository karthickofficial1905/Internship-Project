import requests
from django.core.cache import cache
from .models import Currency

def get_currency_by_country(country_code):
    """Get currency object by country code"""
    try:
        from .models import Country
        country = Country.objects.get(code=country_code, is_active=True)
        return country.currencies.filter(is_active=True).first()
    except:
        # Fallback to INR if currency not found
        try:
            from .models import Country
            country = Country.objects.get(code='IN', is_active=True)
            return country.currencies.filter(is_active=True).first()
        except:
            return None

def get_live_exchange_rates():
    """Fetch live exchange rates from API with caching"""
    cache_key = 'exchange_rates'
    rates = cache.get(cache_key)
    if rates is None:
        try:
            response = requests.get('https://api.exchangerate-api.com/v4/latest/INR', timeout=5)
            if response.status_code == 200:
                data = response.json()
                rates = data.get('rates', {})
                cache.set(cache_key, rates, 3600)  # Cache for 1 hour
            else:
                rates = get_fallback_rates()
        except:
            rates = get_fallback_rates()
    
    return rates

def get_fallback_rates():
    """Fallback rates if API fails"""
    return {
        'INR': 1.0,
    }

def convert_currency(amount, from_country='IN', to_country='IN'):
    """Convert amount from one country currency to another using live rates"""
    if from_country == to_country:
        return amount
    
    from_currency = get_currency_by_country(from_country)
    to_currency = get_currency_by_country(to_country)
    
    rates = get_live_exchange_rates()
    
    # Convert from INR base to target currency
    if from_currency.code == 'INR':
        converted_amount = amount * rates.get(to_currency.code, 1.0)
    elif to_currency.code == 'INR':
        converted_amount = amount / rates.get(from_currency.code, 1.0)
    else:
        # Convert via INR
        inr_amount = amount / rates.get(from_currency.code, 1.0)
        converted_amount = inr_amount * rates.get(to_currency.code, 1.0)
    
    return round(converted_amount, 2)

def get_currency_info(country_code):
    """Get currency info for a country"""
    currency = get_currency_by_country(country_code)
    return {
        'symbol': currency.symbol,
        'code': currency.code,
        'name': currency.name
    }

# Legacy mapping for backward compatibility
COUNTRY_CURRENCY_MAP = {
    'IN': {'symbol': '₹', 'code': 'INR'},
    'US': {'symbol': '$', 'code': 'USD'},
    'GB': {'symbol': '£', 'code': 'GBP'},
    'EU': {'symbol': '€', 'code': 'EUR'},
    'JP': {'symbol': '¥', 'code': 'JPY'},
    'AU': {'symbol': 'A$', 'code': 'AUD'},
    'CA': {'symbol': 'C$', 'code': 'CAD'},
}