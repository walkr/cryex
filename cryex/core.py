class ClientError(Exception):
    pass


class Client(object):
    """ The client object """

    PUBLIC = None   # Public API endpoint
    PRIVATE = None  # Private API endpoint

    # These are the normalized symbols.
    # To must be remapped in your subclass, and turned
    # into symbols specific to a particular exchange,
    # such as XXBT for Bitcoin on Kraken.
    NORMALIZED_SYMBOLS = {

        # PAIRS
        'eth_usd',
        'eth_btc',
        'btc_usd',
        'str_btc',
        'bts_btc',
        'fct_btc',
        'maid_btc',

        # SYMBOLS
        'maid',
        'bts',
        'fct',
        'str',
        'eth',
        'btc',
        'usd',
    }

    # Define this in your subclass
    REPAIRS = {}

    @classmethod
    def validate_pair(cls, pair_or_symbol):
        """ Validate a normalized pair/symbol """

        if pair_or_symbol not in cls.NORMALIZED_SYMBOLS:
            raise ClientError('Invalid pair/symbol')
        if pair_or_symbol not in cls.REPAIRS:
            raise ClientError(
                'There is no remapping available for this symbol/pair.')

    @classmethod
    def repair(cls, pair):
        cls.validate_pair(pair)
        return cls.REPAIRS[pair]


class Public(object):
    """ Public API methods """

    def ticker(self, pair):
        raise NotImplemented

    def depth(self, pair):
        raise NotImplemented

    def trades(self, pair):
        raise NotImplemented


class Private(object):
    """ Private API methods """

    def balances(self, symbol=None):
        raise NotImplemented

    def buy(self, pair, price, amount):
        raise NotImplemented

    def sell(self, pair, price, amount):
        raise NotImplemented

    def stop(self, order_number):
        raise NotImplemented
