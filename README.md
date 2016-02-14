# Cryex

Clients for various cryptocurrency exchanges.

[![Build Status](https://travis-ci.org/walkr/cryex.svg?branch=master)](https://travis-ci.org/walkr/cryex)

### Exchanges supported:

* Kraken
* Poloniex


### Features supported:

* Get ticker
* ... more to come ...


### Usage:
```python
from cryex import Poloniex, Kraken

client = Poloniex()
ticker_data = client.ticker('eth_btc')
print(ticker_data['last'])
```