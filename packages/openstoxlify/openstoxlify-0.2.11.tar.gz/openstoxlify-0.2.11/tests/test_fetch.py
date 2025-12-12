import pytest

from openstoxlify import fetch, MarketData
from openstoxlify.models import Period, Provider


def test_fetch():
    market_data = fetch("BTCUSDT", Provider.Binance, Period.MONTHLY)
    assert isinstance(market_data, MarketData)
