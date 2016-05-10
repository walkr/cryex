import time
import hmac
import base64
import hashlib
import requests
from decimal import Decimal

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

from cryex import core


class Kraken(core.Client):
    """ Implementation for exchange: Kraken """

    PUBLIC = 'https://api.kraken.com/0/public/Ticker?pair={}'
    PRIVATE = 'https://api.kraken.com/0/private/{}'
    REPAIRS = {
        'eth_usd': 'XETHZUSD',
        'eth_btc': 'XETHXXBT',
        'btc_usd': 'XXBTZUSD',
        'eth': 'XETH',
        'btc': 'XXBT',
    }

    def __init__(self, key=None, secret=None):
        super(Kraken, self).__init__()

        self.public = self.Public()
        self.private = self.Private(key, secret)

    ##################################################

    class Public(core.Public):
        """ Public API """

        def ticker(self, pair):
            """ Fetch public ticker """

            new_pair = Kraken.repair(pair)
            url = Kraken.PUBLIC.format(new_pair)
            data = requests.get(url).json()['result'][new_pair]
            return {
                'exchange': 'kraken',
                'last': Decimal(data['c'][0]),
                'pair': pair,
                'volume24h': Decimal(data['v'][1]),
                'high24h': Decimal(data['h'][1]),
                'low24h': Decimal(data['l'][1]),
            }

        def currencies(self):
            return [c for c in Kraken.REPAIRS.keys() if '_' not in c]

    ##################################################

    class Private(core.Private):
        """ Private API """

        def __init__(self, key, secret):
            self.key = key
            self.secret = secret

        # ############## HELPERS ###################################

        def sign(self, digest):
            secret = base64.b64decode(self.secret)
            return hmac.new(
                secret,
                digest,
                hashlib.sha512
            ).digest()

        def post(self, url, params=None):
            """ Make a post request to Kraken """

            params = params or {}

            # Add nonce
            nonce = int(time.time() * 1000)
            params['nonce'] = nonce

            # Create message to sign
            encoded = urlencode(params)
            message = (str(nonce) + encoded).encode()
            digest = hashlib.sha256(message).digest()

            path = url.replace('https://api.kraken.com', '').encode()
            to_sign = path + digest

            # Create signature and headers
            signature = self.sign(to_sign)
            headers = {'API-Key': self.key,
                       'API-Sign': base64.b64encode(signature).decode()}

            # Fetch and return json
            res = requests.post(url, data=params, headers=headers)
            return res.json()

        # ############## COMMANDS ###################################

        def balances(self, symbol=None):
            url = Kraken.PRIVATE.format('Balance')
            response = self.post(url)['result']
            return response[Kraken.repair(symbol)] if symbol else response

        def buy(self, pair, price, amount):
            """ Launch a new buy order """

            new_pair = Kraken.repair(pair)
            params = {'type': 'buy', 'pair': new_pair,
                      'ordertype': 'limit', 'price': str(price), 'volume': str(amount)}

            url = Kraken.PRIVATE.format('AddOrder')
            return self.post(url, params)

        def sell(self, pair, price, amount):
            """ Launch a new sell order """

            new_pair = Kraken.repair(pair)
            params = {'type': 'sell', 'pair': new_pair,
                      'ordertype': 'limit', 'price': str(price), 'volume': str(amount)}

            url = Kraken.PRIVATE.format('AddOrder')
            return self.post(url, params)

        def stop(self, order_id):
            """ Cancel order """
            params = {'txid': order_id}
            url = Kraken.PRIVATE.format('CancelOrder')
            return self.post(url, params)
