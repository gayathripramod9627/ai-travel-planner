"""Core logic for the AI Travel Planner for Students (data-driven with pandas)."""
from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).parent / "data" / "destinations.csv"
COST_COLS = ["stay", "food", "transport", "entry_fees"]
LABELS = {"stay": "Stay", "food": "Food", "transport": "Transport", "entry_fees": "Entry fees"}


def load_data() -> pd.DataFrame:
    """Load destination data and compute the minimum comfortable daily cost."""
    df = pd.read_csv(DATA_PATH)
    df["daily_min"] = df[COST_COLS].sum(axis=1)
    return df


DF = load_data()


def get_destination(name: str):
    """Case-insensitive lookup. Returns a row (Series) or None."""
    match = DF[DF["destination"].str.lower() == name.strip().lower()]
    return None if match.empty else match.iloc[0]


def budget_status(daily_budget: float, daily_min: float):
    """Compare the student's daily budget with the typical daily cost."""
    ratio = daily_budget / daily_min
    if ratio >= 1.3:
        return "Comfortable", "good", ratio
    if ratio >= 1.0:
        return "Feasible", "ok", ratio
    if ratio >= 0.75:
        return "Tight", "warn", ratio
    return "Not enough", "bad", ratio


def build_plan(row, days: int, budget: int) -> dict:
    """Create a day-wise itinerary and a budget split for one destination."""
    daily_budget = budget / days
    base = {c: float(row[c]) for c in COST_COLS}
    scale = daily_budget / sum(base.values())
    split = {c: round(v * scale) for c, v in base.items()}

    activities = row["activities"].split(";")
    itinerary = [
        {
            "day": d,
            "activity": activities[(d - 1) % len(activities)],
            "food": row["food_tip"],
            "transport": row["transport_tip"],
            "cost": round(daily_budget),
        }
        for d in range(1, days + 1)
    ]

    label, css, ratio = budget_status(daily_budget, row["daily_min"])
    return {
        "destination": row["destination"],
        "state": row["state"],
        "type": row["type"],
        "best_season": row["best_season"],
        "student_tip": row["student_tip"],
        "daily_budget": round(daily_budget),
        "daily_min": int(row["daily_min"]),
        "status": label,
        "status_css": css,
        "ratio": round(ratio, 2),
        "split": {LABELS[k]: v for k, v in split.items()},
        "itinerary": itinerary,
    }


def recommend(budget: int, days: int, exclude: str = "", limit: int = 3) -> list:
    """Suggest destinations whose typical cost fits inside the budget."""
    daily_budget = budget / days
    data = DF[DF["destination"].str.lower() != exclude.strip().lower()].copy()
    data = data[data["daily_min"] <= daily_budget]
    # Closest to the budget first = best use of money
    data["gap"] = daily_budget - data["daily_min"]
    data = data.sort_values("gap").head(limit)
    return data[["destination", "state", "type", "daily_min"]].to_dict("records")


def all_destinations() -> list:
    return sorted(DF["destination"].tolist())
