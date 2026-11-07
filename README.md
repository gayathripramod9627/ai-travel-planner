# ✈️ AI Travel Planner for Students

A Flask web app that builds a day-wise, budget-aware travel itinerary for students.
Built as a project after a 3-month Data Science course.

## Features
- Data-driven planning using **pandas** and a CSV dataset of Indian destinations
- Daily budget split (stay, food, transport, entry fees) shown in a **Chart.js** doughnut chart
- Budget check: Comfortable / Feasible / Tight / Not enough
- Recommends other destinations that fit your budget
- Input validation and responsive, dark-mode-friendly UI

## Tech stack
Python, Flask, pandas, HTML/CSS, Chart.js

## Run locally
```bash
git clone https://github.com/<your-username>/ai-travel-planner.git
cd ai-travel-planner
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## Project structure
```
app.py                  Flask routes and validation
planner.py              Planning and recommendation logic (pandas)
data/destinations.csv   Destination dataset (approximate costs in ₹/day)
templates/              Jinja2 HTML templates
static/style.css        Styles
```

## How the budget logic works
1. Daily budget = total budget / days
2. The destination's typical daily cost is the sum of stay, food, transport and entry fees
3. Your daily budget is scaled across those categories in the same proportion
4. Ratio of budget to typical cost decides the status (>=1.3 Comfortable, >=1.0 Feasible, >=0.75 Tight)

## Future improvements
- Add more destinations and real price data
- Add an LLM API to write personalised itinerary text
- Add a cost-prediction model (scikit-learn) trained on travel data
- Deploy on Render or PythonAnywhere

## Note
Costs are rough estimates for learning purposes, not live prices.
