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

from cryex import Poloniex, Kraken


def load_ticker_data(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        with requests_mock.mock() as m:
            with open('tests/data/poloniex.ticker.json') as fh:
                m.register_uri(
                    'GET', 'https://poloniex.com/public?command=returnTicker', text=fh.read())

            with open('tests/data/kraken.ticker.json') as fh:
                pairs = {'XETHZUSD', 'XETHXXBT', 'XXBTZUSD'}
                json_data = fh.read()
                for pair in pairs:
                    m.register_uri(
                        'GET', 'https://api.kraken.com/0/public/Ticker?pair={}'.format(pair), text=json_data)
            f(*args, **kwargs)
    return wrapper


class TestCryex(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @load_ticker_data
    def test_tickers(self):
        for ex in [Poloniex(), Kraken()]:
            for pair in ['eth_usd', 'eth_btc', 'btc_usd']:
                ticker_data = ex.ticker(pair)
                self.assertIsNotNone(ticker_data['last'])


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
