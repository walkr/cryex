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

print(ticker_data)
```

```
{
    'low24h': 0.0110211,
    'last': 0.0121899,
    'exchange': 'poloniex',
    'volume24h': 1350859.34589662,
    'high24h': 0.0140101,
    'pair': 'eth_btc'
}
```