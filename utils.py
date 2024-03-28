import requests
import json
from config import values


class ConvertException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def convert(quote, base, amount):
        if quote == base:
            raise ConvertException("Cant convert the same curr")

        try:
            quote_ticker = values[quote]
        except KeyError:
            raise ConvertException(f"Fail to process currency {quote}")

        try:
            base_ticker = values[base]
        except KeyError:
            raise ConvertException(f"Fail to process currency {base}")

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertException(f"Fail to convert amount {amount} to float")

        r = requests.get(f"https://open.er-api.com/v6/latest/{quote_ticker}")
        text = json.loads(r.content)
        result = (text["rates"][f"{base_ticker}"]) * int(amount)
        return result
