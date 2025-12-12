import requests
import json
from datetime import datetime
from .models import Period, Provider, Quote, MarketData

MARKET_DATA: MarketData = MarketData(
    ticker="", period=Period.DAILY, provider=Provider.YFinance, quotes=[]
)

PERIOD_MAPPING = {
    Period.MINUTELY: {"interval": "1m", "range": "1wk"},
    Period.QUINTLY: {"interval": "5m", "range": "1wk"},
    Period.HALFHOURLY: {"interval": "30m", "range": "1wk"},
    Period.HOURLY: {"interval": "60m", "range": "1wk"},
    Period.DAILY: {"interval": "1d", "range": "1y"},
    Period.WEEKLY: {"interval": "1wk", "range": "10y"},
    Period.MONTHLY: {"interval": "1mo", "range": "max"},
}


def fetch(ticker: str, provider: Provider, period: Period) -> MarketData:
    global MARKET_DATA

    if period not in PERIOD_MAPPING:
        raise ValueError(
            f"Invalid period '{period}'. Expected one of {list(PERIOD_MAPPING.keys())}."
        )

    interval = PERIOD_MAPPING[period]["interval"]
    time_range = PERIOD_MAPPING[period]["range"]

    url = "https://api.app.stoxlify.com/v1/market/info"
    headers = {"Content-Type": "application/json"}
    payload = {
        "ticker": ticker,
        "range": time_range,
        "source": provider.value,
        "interval": interval,
        "indicator": "quote",
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
    except requests.RequestException as req_err:
        raise RuntimeError(f"Request failed: {req_err}") from req_err

    if not response.ok:
        try:
            error_info = response.json()
            raise RuntimeError(
                f"HTTP {response.status_code} - {error_info.get('message', 'Unknown error')}"
            )
        except ValueError:
            raise RuntimeError(f"HTTP {response.status_code} - {response.text}")

    try:
        data = response.json()
    except ValueError as json_err:
        raise RuntimeError(f"JSON parsing error: {json_err}") from json_err

    quotes = []
    for q in data.get("quote", []):
        try:
            ts = datetime.fromisoformat(q["timestamp"].replace("Z", "+00:00"))
            price = q["product_info"]["price"]

            if not all(k in price for k in ("open", "high", "low", "close")):
                continue

            quote = Quote(
                timestamp=ts,
                high=price["high"],
                low=price["low"],
                open=price["open"],
                close=price["close"],
                volume=price["volume"],
            )
            quotes.append(quote)

        except (KeyError, TypeError, ValueError):
            continue

    MARKET_DATA.ticker = ticker
    MARKET_DATA.period = period
    MARKET_DATA.provider = provider
    MARKET_DATA.quotes = quotes

    return MARKET_DATA
