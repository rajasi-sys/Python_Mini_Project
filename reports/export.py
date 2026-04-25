import json
import csv
import os
from datetime import datetime


# Load data from JSON
def load_data():
    try:
        with open("data/expenses.json", "r") as f:
            return json.load(f)
    except:
        return []


# Export all expenses to CSV
def export_to_csv():
    data = load_data()

    if not data:
        print("No data to export.")
        return

    os.makedirs("reports", exist_ok=True)

    filename = f"reports/expenses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["amount", "category", "date", "note"]
        )
        writer.writeheader()
        writer.writerows(data)

    print(f"Exported successfully to {filename}")


# Export filtered data (by category)
def export_by_category(category):
    data = load_data()
    filtered = [e for e in data if e["category"] == category]

    if not filtered:
        print("No matching data found.")
        return

    filename = f"reports/{category}_expenses.csv"

    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["amount", "category", "date", "note"]
        )
        writer.writeheader()
        writer.writerows(filtered)

    print(f"{category} data exported successfully!")


# Export summary report (category-wise totals)
def export_summary():
    data = load_data()

    summary = {}
    for e in data:
        summary[e["category"]] = summary.get(e["category"], 0) + e["amount"]

    filename = "reports/summary.csv"

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Category", "Total"])
        for category, total in summary.items():
            writer.writerow([category, total])

    print("Summary report exported successfully!")
