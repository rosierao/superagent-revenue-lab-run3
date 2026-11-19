"""Daily revenue report built from payment events."""
import pandas as pd


def load_events(path):
    """Read payment events; amounts are integer cents."""
    return pd.read_csv(path, parse_dates=["occurred_at", "received_at"])


def daily_revenue(events):
    """Return one row per UTC day with total revenue in cents.

    Payment webhooks are at-least-once, so the same payment event can be
    delivered more than once with the same ``event_id``. Count each event once,
    keeping its first delivery.
    """
    events = (
        events.sort_values("received_at", kind="stable")
        .drop_duplicates(subset="event_id", keep="first")
    )
    days = events["occurred_at"].dt.strftime("%Y-%m-%d")
    report = (
        events.assign(day=days)
        .groupby("day", as_index=False)["amount_cents"]
        .sum()
        .rename(columns={"amount_cents": "revenue_cents"})
    )
    return report
