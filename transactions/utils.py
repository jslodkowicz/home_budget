import os
import requests

API_URL = 'https://free.currconv.com/api/v7/convert?q={}_{}' \
          '&compact=ultra&apiKey={}'


def currency_converter(cur_1: str, cur_2: str) -> dict:
    """Function used to calculate current exchange rates for currency pairs"""
    return requests.get(API_URL.format(cur_1, cur_2, os.getenv("CURRENCY_KEY"))).json()
