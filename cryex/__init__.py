# -*- coding: utf-8 -*-

from .poloniex import Poloniex
from .kraken import Kraken
from .core import ClientError

__author__ = 'Tony Walker'
__email__ = 'walkr.walkr@gmail.com'
__version__ = '0.1.6'

__all__ = ['Poloniex', 'Kraken', 'ClientError']
