from datetime import datetime
from .models import ActionType, ActionSeries

STRATEGY_DATA = {}


def act(action: ActionType, timestamp: datetime, amount: float = 0.0):
    """Record an action taken at a specific timestamp."""
    if "strategy" not in STRATEGY_DATA:
        STRATEGY_DATA["strategy"] = [{"label": "strategy", "data": []}]

    amt = 0.0 if action == ActionType.HOLD else amount

    STRATEGY_DATA["strategy"][0]["data"].append(
        ActionSeries(timestamp, action, amt).to_dict()
    )
