
import csv
from pathlib import Path

# Step 1: Locate the Bronze data file
base_dir = Path(__file__).resolve().parent
input_file = base_dir / "data" / "bronze" / "claims_bronze.csv"

# Step 2: Read the claims
with input_file.open("r", newline="", encoding="utf-8") as file:
    claims = list(csv.DictReader(file))

print(f"Total records: {len(claims)}")

# Step 3: Check for missing values
missing_values = sum(
    1 for row in claims
    if any(value is None or value.strip() == "" for value in row.values())
)
print(f"Records with missing values: {missing_values}")

# Step 4: Check for duplicate claim IDs
claim_ids = [row["claim_id"] for row in claims]
duplicates = len(claim_ids) - len(set(claim_ids))
print(f"Duplicate claim IDs: {duplicates}")

# Step 5: Check for invalid claim amounts
invalid_amounts = 0

for row in claims:
    try:
        if float(row["claim_amount"]) <= 0:
            invalid_amounts += 1
    except (ValueError, TypeError):
        invalid_amounts += 1

print(f"Invalid claim amounts: {invalid_amounts}")

# Step 6: Check claim statuses
valid_statuses = {"Approved", "Pending", "Denied"}
invalid_statuses = sum(
    1 for row in claims
    if row["claim_status"] not in valid_statuses
)

print(f"Invalid claim statuses: {invalid_statuses}")
