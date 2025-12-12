from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class PlotType(Enum):
    HISTOGRAM = "histogram"
    LINE = "line"
    AREA = "area"
    CANDLESTICK = "candlestick"


class ActionType(Enum):
    LONG = "Long"
    HOLD = "Hold"
    SHORT = "Short"


class Period(Enum):
    MINUTELY = "1m"
    QUINTLY = "5m"
    HALFHOURLY = "30m"
    HOURLY = "60m"
    DAILY = "D"
    WEEKLY = "W"
    MONTHLY = "M"


class Provider(Enum):
    YFinance = "YFinance"
    Binance = "Binance"


@dataclass
class Quote:
    timestamp: datetime
    high: float
    low: float
    open: float
    close: float
    volume: float


@dataclass
class MarketData:
    ticker: str
    period: Period
    provider: Provider
    quotes: list[Quote]


@dataclass
class FloatSeries:
    timestamp: datetime
    value: float

    def to_dict(self):
        return {"timestamp": self.timestamp.isoformat(), "value": self.value}


@dataclass
class ActionSeries:
    timestamp: datetime
    action: ActionType
    amount: float = 0.0

    def to_dict(self):
        return {
            "timestamp": self.timestamp.isoformat(),
            "action": self.action.value,
            "amount": self.amount,
        }


@dataclass
class LabeledSeries:
    label: str
    data: list

    def to_dict(self):
        return {"label": self.label, "data": [item.to_dict() for item in self.data]}


@dataclass
class Output:
    histogram: list[LabeledSeries]
    line: list[LabeledSeries]
    area: list[LabeledSeries]
    strategy: list[LabeledSeries]

    def to_dict(self):
        return {
            "histogram": [series.to_dict() for series in self.histogram]
            if self.histogram
            else None,
            "line": [series.to_dict() for series in self.line],
            "area": [series.to_dict() for series in self.area] if self.area else None,
            "strategy": [series.to_dict() for series in self.strategy]
            if self.strategy
            else None,
        }
