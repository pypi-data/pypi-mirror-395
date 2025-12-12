import unittest
import matplotlib.dates as mdates
from unittest.mock import patch, ANY
from datetime import datetime

from openstoxlify.models import PlotType, ActionType, Quote
from openstoxlify.draw import draw
from openstoxlify.plotter import PLOT_DATA
from openstoxlify.fetch import MARKET_DATA
from openstoxlify.strategy import STRATEGY_DATA


class TestDrawFunction(unittest.TestCase):
    @patch("matplotlib.pyplot.show")
    @patch("matplotlib.axes.Axes.annotate")
    @patch("matplotlib.axes.Axes.vlines")
    @patch("matplotlib.axes.Axes.plot")
    @patch("matplotlib.axes.Axes.bar")
    @patch("matplotlib.axes.Axes.fill_between")
    def test_draw(
        self,
        mock_fill_between,
        mock_bar,
        mock_plot,
        mock_vlines,
        mock_annotate,
        mock_show,
    ):
        """Test the draw function to ensure all plotting and annotations are triggered."""

        timestamp = datetime(2025, 3, 26)
        expected_ts_num = mdates.date2num(timestamp)

        # Reset data
        PLOT_DATA.clear()
        STRATEGY_DATA.clear()
        MARKET_DATA.quotes.clear()

        # Plot types
        PLOT_DATA[PlotType.HISTOGRAM] = [
            {
                "label": "histogram",
                "data": [{"timestamp": timestamp, "value": 100}],
                "screen_index": 0,
            }
        ]
        PLOT_DATA[PlotType.LINE] = [
            {
                "label": "line",
                "data": [{"timestamp": timestamp, "value": 200}],
                "screen_index": 0,
            }
        ]
        PLOT_DATA[PlotType.AREA] = [
            {
                "label": "area",
                "data": [{"timestamp": timestamp, "value": 300}],
                "screen_index": 0,
            }
        ]

        # Candlestick quote
        MARKET_DATA.quotes.append(
            Quote(
                timestamp=timestamp,
                open=100,
                close=200,
                low=50,
                high=250,
                volume=1000,
            )
        )

        # Strategy data (with amount)
        STRATEGY_DATA["strategy"] = [
            {
                "label": "strategy",
                "data": [
                    {
                        "timestamp": timestamp,
                        "action": ActionType.LONG.value,
                        "amount": 42.0,
                    }
                ],
            }
        ]

        draw()

        # Histogram
        mock_bar.assert_called_with(
            [expected_ts_num],
            [100],
            label="histogram",
            color=ANY,
            width=0.5,
            alpha=0.6,
        )

        # Line
        mock_plot.assert_any_call(
            [expected_ts_num], [200], label="line", color=ANY, lw=2
        )

        # Area
        mock_fill_between.assert_called_with(
            [expected_ts_num], [300], label="area", color=ANY, alpha=0.3
        )

        # Arrow marker
        offset_price = 200 - (200 * 0.05)
        mock_plot.assert_any_call(
            expected_ts_num, offset_price, marker="^", color="blue", markersize=8
        )

        # Inline annotation
        mock_annotate.assert_any_call(
            "LONG 42.0",
            xy=(expected_ts_num, offset_price),
            xytext=(0, -15),
            textcoords="offset points",
            ha="center",
            fontsize=9,
            color="blue",
        )


if __name__ == "__main__":
    unittest.main()
