import os
import requests

API_URL = 'https://free.currconv.com/api/v7/convert?q={}_{}' \
          '&compact=ultra&apiKey={}'


def currency_converter(currency_from: str, currency_to: str) -> dict:
    """Function used to calculate current exchange rates for currency pairs"""
    return requests.get(API_URL.format(currency_from, currency_to, os.getenv(
        "CURRENCY_KEY"))).json()
