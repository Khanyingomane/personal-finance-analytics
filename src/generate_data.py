
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

# Dataset configuration
start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 12, 31)
rng = np.random.default_rng(42)

income_categories = [
    "Salary",
    "Freelance Income",
    "Other Income"
]

expense_categories = [
    "Rent",
    "Groceries",
    "Transport",
    "Utilities",
    "Shopping",
    "Entertainment",
    "Healthcare",
    "Education",
    "Personal Care",
    "Miscellaneous"
]

payment_methods = ["Card", "Cash", "EFT"]

# Monthly income and expense ranges in ZAR
income_ranges = {
    "Salary": (12000, 18000),
    "Freelance Income": (500, 3500),
    "Other Income": (100, 1500)
}

expense_ranges = {
    "Rent": (3500, 5500),
    "Groceries": (150, 900),
    "Transport": (50, 600),
    "Utilities": (300, 1100),
    "Shopping": (100, 1500),
    "Entertainment": (80, 800),
    "Healthcare": (100, 1200),
    "Education": (200, 1800),
    "Personal Care": (80, 650),
    "Miscellaneous": (50, 1000)
}

transactions = []

def add_transaction(date, category, transaction_type, amount, payment_method):
    """Add a financial transaction to the dataset."""
    transactions.append({
        "date": date,
        "description": category,
        "category": category,
        "transaction_type": transaction_type,
        "amount": round(float(amount), 2),
        "payment_method": payment_method
    })


# Generate financial transactions for each month
months = pd.date_range(start=start_date, end=end_date, freq="MS")

for month in months:
    year = month.year
    month_number = month.month
    days_in_month = month.days_in_month

    # Apply gradual annual cost increases
    inflation_factor = 1.05 ** (year - 2024)

    # Monthly salary
    salary = rng.uniform(*income_ranges["Salary"])

    add_transaction(
        month.replace(day=25),
        "Salary",
        "Income",
        salary,
        "EFT"
    )

    # Occasional additional income
    for category in income_categories[1:]:
        if rng.random() < 0.35:
            amount = rng.uniform(*income_ranges[category])
            day = int(rng.integers(1, days_in_month + 1))

            add_transaction(
                month.replace(day=day),
                category,
                "Income",
                amount,
                "EFT"
            )

    # Monthly rent
    rent = rng.uniform(*expense_ranges["Rent"])
    rent *= inflation_factor

    add_transaction(
        month.replace(day=1),
        "Rent",
        "Expense",
        rent,
        "EFT"
    )

    # Monthly utilities
    utilities = rng.uniform(*expense_ranges["Utilities"])
    utilities *= inflation_factor

    add_transaction(
        month.replace(day=5),
        "Utilities",
        "Expense",
        utilities,
        "EFT"
    )

    # Variable monthly expenses
    for category in expense_categories:
        if category in ["Rent", "Utilities"]:
            continue

        if category == "Groceries":
            count = int(rng.integers(4, 9))
        elif category == "Transport":
            count = int(rng.integers(8, 17))
        elif category in ["Shopping", "Entertainment"]:
            count = int(rng.integers(1, 5))
        else:
            count = int(rng.integers(0, 4))

        for _ in range(count):
            minimum, maximum = expense_ranges[category]
            amount = rng.uniform(minimum, maximum)

            amount *= inflation_factor

            # Simulate higher shopping expenses in December
            if month_number == 12 and category == "Shopping":
                amount *= 1.5

            day = int(rng.integers(1, days_in_month + 1))
            payment_method = rng.choice(payment_methods)

            add_transaction(
                month.replace(day=day),
                category,
                "Expense",
                amount,
                payment_method
            )

    # Occasional unexpected expense
    if rng.random() < 0.20:
        day = int(rng.integers(1, days_in_month + 1))
        emergency_amount = rng.uniform(500, 3000)

        add_transaction(
            month.replace(day=day),
            "Miscellaneous",
            "Expense",
            emergency_amount,
            "Card"
        )


# Convert transactions into a Pandas DataFrame
df = pd.DataFrame(transactions)

# Sort transactions chronologically
df = df.sort_values("date").reset_index(drop=True)

# Generate unique transaction identifiers
df.insert(
    0,
    "transaction_id",
    [f"TXN{i + 1:05d}" for i in range(len(df))]
)

# Create additional date-related features
df["month"] = df["date"].dt.month
df["year"] = df["date"].dt.year

# Save the dataset
project_root = Path(__file__).resolve().parent.parent
output_folder = project_root / "data" / "raw"
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "personal_finance_transactions.csv"

df.to_csv(output_file, index=False)

# Display dataset summary
print("\nPERSONAL FINANCE DATASET GENERATED")
print("----------------------------------")
print("Dataset Start Date:", start_date.date())
print("Dataset End Date:", end_date.date())
print("Total Transactions:", len(df))
print("Income Transactions:", len(df[df["transaction_type"] == "Income"]))
print("Expense Transactions:", len(df[df["transaction_type"] == "Expense"]))
print("\nFirst Five Transactions:")
print(df.head())
print("\nDataset saved to:", output_file)
