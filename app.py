import os

from flask import Flask, render_template, request

from planner import all_destinations, build_plan, get_destination, recommend

app = Flask(__name__)

MAX_DAYS = 30


def render_home(error=None, suggestions=None, status=200):
    return (
        render_template(
            "index.html",
            error=error,
            suggestions=suggestions,
            destinations=all_destinations(),
        ),
        status,
    )


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_home()

    destination = request.form.get("destination", "").strip()
    try:
        days = int(request.form.get("days", ""))
        budget = int(request.form.get("budget", ""))
    except ValueError:
        return render_home("Please enter valid numbers for days and budget.", status=400)

    if not destination or not 1 <= days <= MAX_DAYS or budget < 1:
        return render_home(f"Days must be 1-{MAX_DAYS} and budget must be positive.", status=400)

    row = get_destination(destination)
    if row is None:
        suggestions = recommend(budget, days)
        return render_home(
            f"Sorry, '{destination}' is not in our dataset yet. Try one of these instead:",
            suggestions=suggestions,
            status=404,
        )

    plan = build_plan(row, days, budget)
    alternatives = recommend(budget, days, exclude=destination)
    return render_template(
        "result.html", plan=plan, days=days, budget=budget, alternatives=alternatives
    )


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
