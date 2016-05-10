import time
import hmac
import hashlib
from decimal import Decimal
from datetime import datetime

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

import requests

from cryex import core
from cryex.model import Ask, Bid, Trade
from cryex.coins.poloniex import POLONIEX_REPAIRS


class Poloniex(core.Client):
    """ Implementation for exchange: Poloniex """

    PUBLIC = 'https://poloniex.com/public'
    PRIVATE = 'https://poloniex.com/tradingApi'
    REPAIRS = POLONIEX_REPAIRS

    def __init__(self, key=None, secret=None):
        super(Poloniex, self).__init__()

        self.public = self.Public()
        self.private = self.Private(key, secret)

    ##################################################

    class Public(core.Public):
        """ Public API """

        def ticker(self, pair):
            """ Return ticker """

            new_pair = Poloniex.repair(pair)
            args = urlencode({'command': 'returnTicker'})
            url = Poloniex.PUBLIC + '?' + args
            data = requests.get(url).json()[new_pair]

            return {
                'exchange': 'poloniex',
                'last': Decimal(data['last']),
                'pair': pair,
                'volume24h': Decimal(data['quoteVolume']),
                'high24h': Decimal(data['high24hr']),
                'low24h': Decimal(data['low24hr']),
            }

        def depth(self, pair, depth=1000):
            """ Return order book """

            new_pair = Poloniex.repair(pair)
            args = urlencode({
                'command': 'returnOrderBook',
                'currencyPair': new_pair,
                'depth': depth
            })

            url = Poloniex.PUBLIC + '?' + args
            data = requests.get(url).json()

            asks = [Ask(i[0], i[1]) for i in data['asks']]
            bids = [Bid(i[0], i[1]) for i in data['bids']]
            return (asks, bids)

        def trades(self, pair, start=None, end=None):
            """ Return public trade history

            Arguments:

            pair        - cryptocurrency pair

            (optional)
            start       - start timestamp
            end         - end timestamp """

            new_pair = Poloniex.repair(pair)
            args = urlencode({
                'command': 'returnTradeHistory',
                'currencyPair': new_pair,
            })

            url = Poloniex.PUBLIC + '?' + args
            data = requests.get(url).json()

            def new_trade(i):
                """ Parse UTC Date and create a new Trade object """
                dateformat = '%Y-%m-%d %H:%M:%S'
                rate = Decimal(i['rate'])
                amount = Decimal(i['amount'])
                date = datetime.strptime(i['date'], dateformat)
                return Trade(i['globalTradeID'], rate, amount, i['type'], date)

            # ---
            return [new_trade(i) for i in data]

        def currencies(self):
            return [c for c in Poloniex.REPAIRS.keys() if '_' not in c]

    ##################################################

    class Private(core.Private):
        """ Private API """

        def __init__(self, key, secret):
            self.key = key
            self.secret = secret

        # ############## HELPERS ###################################

        def sign(self, data):
            encoded = urlencode(data).encode('utf-8')
            return hmac.new(
                self.secret.encode('utf-8'),
                encoded, hashlib.sha512).hexdigest()

        def post(self, params):
            """ Make a post request to Poloniex """

            # Add nonce
            params['nonce'] = int(time.time() * 1000)

            # Sign params and create headers
            sig = self.sign(params)
            headers = {'Key': self.key, 'Sign': sig}

            # Fetch and return json
            res = requests.post(Poloniex.PRIVATE, params, headers=headers)
            return res.json()

        # ############## COMMANDS ###################################

        def balances(self, symbol=None):
            """ Return account balances.

            Arguments:

            (optional)
            symbol    - return balance for that symbol (currency) """

            response = self.post({'command': 'returnBalances'})
            return response[Poloniex.REPAIRS[symbol]] if symbol else response

        def buy(self, pair, price, amount):
            """ Launch a new buy order

            Arguments:

            pair        - currency pair, e.g. eth_btc
            price       - the price to pay
            amount      - the amount to trade """

            new_pair = Poloniex.REPAIRS[pair]
            return self.post({
                'command': 'buy', 'currencyPair': new_pair,
                'rate': price, 'amount': amount
            })

        def sell(self, pair, price, amount):
            """ Launch a new sell order

            Arguments:

            pair        - currency pair, e.g. eth_btc
            price       - the price to pay
            amount      - the amount to trade """

            new_pair = Poloniex.REPAIRS[pair]
            return self.post({
                'command': 'sell', 'currencyPair': new_pair,
                'rate': price, 'amount': amount
            })

        def stop(self, order_id):
            """ Cancel order """
            return self.post({
                'command': 'cancelOrder',
                'orderNumber': order_id,
            })
