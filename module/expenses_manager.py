import json
import os
from datetime import datetime
import uuid


class ExpenseManager:
    def __init__(self, file_path="data/expenses.json"):
        self.file_path = file_path
        self.expenses = []
        self.categories = set(["Food", "Transport", "Shopping", "Bills", "Other"])
        self._load_data()

    # -------------------- FILE HANDLING --------------------

    def _load_data(self):
        """Load expenses from JSON file"""
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                try:
                    data = json.load(file)
                    self.expenses = data.get("expenses", [])
                    self.categories.update(data.get("categories", []))
                except json.JSONDecodeError:
                    self.expenses = []
        else:
            self._save_data()

    def _save_data(self):
        """Save expenses to JSON file"""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, "w") as file:
            json.dump({
                "expenses": self.expenses,
                "categories": list(self.categories)
            }, file, indent=4)

    # -------------------- VALIDATION --------------------

    def _validate_amount(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")

    def _validate_date(self, date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")

    # -------------------- CRUD OPERATIONS --------------------

    def add_expense(self, amount, category, date, note=""):
        """Add a new expense"""
        self._validate_amount(amount)
        self._validate_date(date)

        expense = {
            "id": str(uuid.uuid4()),
            "amount": float(amount),
            "category": category,
            "date": date,
            "note": note
        }

        self.expenses.append(expense)
        self.categories.add(category)
        self._save_data()

        return expense

    def edit_expense(self, expense_id, **updates):
        """Edit an existing expense"""
        for expense in self.expenses:
            if expense["id"] == expense_id:
                if "amount" in updates:
                    self._validate_amount(updates["amount"])
                    expense["amount"] = float(updates["amount"])

                if "date" in updates:
                    self._validate_date(updates["date"])
                    expense["date"] = updates["date"]

                if "category" in updates:
                    expense["category"] = updates["category"]
                    self.categories.add(updates["category"])

                if "note" in updates:
                    expense["note"] = updates["note"]

                self._save_data()
                return expense

        raise ValueError("Expense not found")

    def delete_expense(self, expense_id):
        """Delete an expense"""
        original_length = len(self.expenses)
        self.expenses = [e for e in self.expenses if e["id"] != expense_id]

        if len(self.expenses) == original_length:
            raise ValueError("Expense not found")

        self._save_data()

    # -------------------- FETCHING --------------------

    def get_all_expenses(self):
        """Return all expenses"""
        return self.expenses

    def get_categories(self):
        """Return all categories"""
        return list(self.categories)

    def filter_expenses(
        self,
        start_date=None,
        end_date=None,
        category=None,
        min_amount=None,
        max_amount=None
    ):
        """Filter expenses based on conditions"""
        filtered = self.expenses

        if start_date:
            self._validate_date(start_date)
            filtered = [e for e in filtered if e["date"] >= start_date]

        if end_date:
            self._validate_date(end_date)
            filtered = [e for e in filtered if e["date"] <= end_date]

        if category:
            filtered = [e for e in filtered if e["category"] == category]

        if min_amount is not None:
            filtered = [e for e in filtered if e["amount"] >= min_amount]

        if max_amount is not None:
            filtered = [e for e in filtered if e["amount"] <= max_amount]

        return filtered

    # -------------------- SUMMARY --------------------

    def get_total_expense(self):
        """Total spending"""
        return sum(e["amount"] for e in self.expenses)

    def get_category_summary(self):
        """Category-wise spending"""
        summary = {}
        for e in self.expenses:
            summary[e["category"]] = summary.get(e["category"], 0) + e["amount"]
        return summary

