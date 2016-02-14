# -*- coding: utf-8 -*-
import requests


class ExchangeError(Exception):
    pass


class Exchange(object):
    PAIRS = {
        'eth_usd', 'eth_btc', 'btc_usd'}

    def validate_pair(self, pair):
        if pair not in self.PAIRS:
            raise ExchangeError('Invalid pair')


class Poloniex(Exchange):
    """ Implementation for exchange: Poloniex """

    URL = 'https://poloniex.com/public?command=returnTicker'

    REPAIRS = {
        'eth_usd': 'USDT_ETH',
        'eth_btc': 'BTC_ETH',
        'btc_usd': 'USDT_BTC'}

    def __init__(self):
        super(Poloniex, self).__init__()

    def ticker(self, pair):
        self.validate_pair(pair)

        new_pair = self.REPAIRS[pair]
        data = requests.get(self.URL).json()[new_pair]

        return {
            'exchange': 'poloniex',
            'last': float(data['last']),
            'pair': pair,
            'volume24h': float(data['quoteVolume']),
            'high24h': float(data['high24hr']),
            'low24h': float(data['low24hr']),
        }


class Kraken(Exchange):
    """ Implementation for exchange: Kraken """

    URL = 'https://api.kraken.com/0/public/Ticker?pair={}'

    REPAIRS = {
        'eth_usd': 'XETHZUSD',
        'eth_btc': 'XETHXXBT',
        'btc_usd': 'XXBTZUSD'}

    def __init__(self):
        super(Kraken, self).__init__()

    def ticker(self, pair):
        self.validate_pair(pair)

        new_pair = self.REPAIRS[pair]
        url = self.URL.format(new_pair)
        data = requests.get(url).json()['result'][new_pair]
        return {
            'exchange': 'kraken',
            'last': float(data['c'][0]),
            'pair': pair,
            'volume24h': float(data['v'][1]),
            'high24h': float(data['h'][1]),
            'low24h': float(data['l'][1]),
        }
