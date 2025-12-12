from .models import FloatSeries, PlotType
from datetime import datetime

PLOT_DATA = {}


def plot(
    graph_type: PlotType,
    label: str,
    timestamp: datetime,
    value: float,
    screen_index: int = 0,
):
    """Store data for plotting, organizing by label."""
    if graph_type not in PlotType:
        raise ValueError(f"Invalid graph type: {graph_type}")

    if graph_type not in PLOT_DATA:
        PLOT_DATA[graph_type] = []

    for plot_entry in PLOT_DATA[graph_type]:
        if plot_entry["label"] == label:
            plot_entry["data"].append(FloatSeries(timestamp, value).to_dict())
            return

    PLOT_DATA[graph_type].append(
        {
            "label": label or graph_type.value,
            "data": [FloatSeries(timestamp, value).to_dict()],
            "screen_index": screen_index,
        }
    )
