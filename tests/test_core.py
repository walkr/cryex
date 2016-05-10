#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_core
----------------------------------

Tests for `core` module.
"""

import unittest
import functools
import requests_mock

from cryex import Poloniex, Kraken, ClientError
from cryex.model import Ask, Bid, Trade


def load_ticker_data(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        with requests_mock.mock() as m:
            with open('tests/data/poloniex.ticker.json') as fh:
                m.register_uri(
                    'GET', 'https://poloniex.com/public?command=returnTicker', text=fh.read())

            with open('tests/data/poloniex.trades.json') as fh:
                m.register_uri(
                    'GET', 'https://poloniex.com/public?returnTradeHistory&currencyPair=BTC_ETH', text=fh.read())

            with open('tests/data/poloniex.depth.json') as fh:
                m.register_uri(
                    'GET', 'https://poloniex.com/public?command=returnOrderBook&currencyPair=BTC_ETH&depth=1000', text=fh.read())

            with open('tests/data/kraken.ticker.json') as fh:
                pairs = Kraken.REPAIRS.values()
                json_data = fh.read()
                for pair in pairs:
                    url = 'https://api.kraken.com/0/public/Ticker?pair={}'.format(
                        pair)
                    m.register_uri('GET', url, text=json_data)
            f(*args, **kwargs)
    return wrapper


class TestCryex(unittest.TestCase):

    def setUp(self):
        self.clients = [Poloniex(), Kraken()]

    def tearDown(self):
        pass

    @load_ticker_data
    def test_tickers(self):
        keys = ['last', 'pair', 'exchange', 'volume24h', 'low24h', 'high24h']
        for client in self.clients:
            pairs = [p for p in client.REPAIRS.keys() if '_' in p]
            for pair in pairs:
                ticker_data = client.public.ticker(pair)
                for key in keys:
                    self.assertIsNotNone(ticker_data[key])

    def test_validate_pair(self):
        c = self.clients[0]
        self.assertRaisesRegexp(
            ClientError, 'Invalid pair', c.validate_pair, 'xyz')

    def test_public_trades(self):
        c = self.clients[0]
        trades = c.public.trades('eth_btc')
        self.assertIsInstance(trades[0], Trade)

    def test_public_depth(self):
        c = self.clients[0]
        (asks, bids) = c.public.depth('eth_btc')
        self.assertIsInstance(asks[0], Ask)
        self.assertIsInstance(bids[0], Bid)

    def test_currencies(self):
        for c in self.clients:
            self.assertTrue('eth' in c.public.currencies())
            self.assertTrue('eth' in c.public.currencies())


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
