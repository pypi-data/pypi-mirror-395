import unittest
import json

from datetime import datetime
from unittest.mock import patch
from openstoxlify import (
    PlotType,
    ActionType,
    act,
    plot,
    STRATEGY_DATA,
    PLOT_DATA,
    output,
)
from openstoxlify.fetch import MARKET_DATA
from openstoxlify.models import Period, Provider


class TestStrategy(unittest.TestCase):
    def setUp(self):
        PLOT_DATA.clear()
        STRATEGY_DATA.clear()
        MARKET_DATA.ticker = ""
        MARKET_DATA.period = Period.DAILY
        MARKET_DATA.provider = Provider.YFinance
        MARKET_DATA.quotes = []

    def test_plot(self):
        timestamp = datetime(2025, 3, 26, 0, 0, 0)
        value = 90000.0

        plot(PlotType.HISTOGRAM, "test_plot", timestamp, value)

        self.assertEqual(len(PLOT_DATA[PlotType.HISTOGRAM][0]["data"]), 1)
        self.assertEqual(
            PLOT_DATA[PlotType.HISTOGRAM][0]["data"][0]["timestamp"],
            timestamp.isoformat(),
        )
        self.assertEqual(PLOT_DATA[PlotType.HISTOGRAM][0]["data"][0]["value"], value)

    def test_act(self):
        timestamp = datetime(2025, 3, 26, 0, 0, 0)

        act(ActionType.LONG, timestamp, 1)

        self.assertEqual(len(STRATEGY_DATA["strategy"][0]["data"]), 1.0)
        self.assertEqual(
            STRATEGY_DATA["strategy"][0]["data"][0]["action"], ActionType.LONG.value
        )
        self.assertEqual(
            STRATEGY_DATA["strategy"][0]["data"][0]["timestamp"], timestamp.isoformat()
        )
        self.assertEqual(STRATEGY_DATA["strategy"][0]["data"][0]["amount"], 1.0)

        act(ActionType.HOLD, timestamp)

        self.assertEqual(len(STRATEGY_DATA["strategy"][0]["data"]), 2)
        self.assertEqual(
            STRATEGY_DATA["strategy"][0]["data"][1]["action"], ActionType.HOLD.value
        )
        self.assertEqual(
            STRATEGY_DATA["strategy"][0]["data"][1]["timestamp"], timestamp.isoformat()
        )
        self.assertEqual(STRATEGY_DATA["strategy"][0]["data"][1]["amount"], 0.0)

    @patch("builtins.print")
    def test_output(self, mock_print):
        self.maxDiff = None
        plot(PlotType.HISTOGRAM, "test_output", datetime(2025, 3, 26), 90000)
        act(ActionType.LONG, datetime(2025, 3, 26), 1.0)

        output()

        actual_output = mock_print.call_args[0][0].strip()

        expected_output = json.dumps(
            {
                "histogram": [
                    {
                        "label": "test_output",
                        "data": [{"timestamp": "2025-03-26T00:00:00", "value": 90000}],
                        "screen_index": 0,
                    }
                ],
                "line": [],
                "area": [],
                "strategy": [
                    {
                        "label": "strategy",
                        "data": [
                            {
                                "timestamp": "2025-03-26T00:00:00",
                                "action": "Long",
                                "amount": 1.0,
                            }
                        ],
                    }
                ],
                "quotes": {
                    "ticker": "",
                    "interval": "1d",
                    "provider": "YFinance",
                    "data": [],
                },
            }
        )

        self.assertEqual(expected_output, actual_output)


if __name__ == "__main__":
    unittest.main()
