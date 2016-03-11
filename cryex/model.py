from collections import namedtuple

Ask = namedtuple('Ask', ('price', 'amount'))
Bid = namedtuple('Bid', ('price', 'amount'))
Trade = namedtuple('Trade', ('txid', 'price', 'amount', 'type', 'date'))
