
import csv
from pathlib import Path
from decimal import Decimal

# Step 1: Locate the Gold summary file
base_dir = Path(__file__).resolve().parent
gold_file = base_dir / "data" / "gold" / "claims_summary.csv"

# Step 2: Read Gold data
with gold_file.open("r", newline="", encoding="utf-8") as file:
    records = list(csv.DictReader(file))

# Step 3: Calculate totals
total_claims = sum(
    int(row["claim_count"]) for row in records
)

total_amount = sum(
    (Decimal(row["total_claim_amount"]) for row in records),
    Decimal("0.00")
)

# Step 4: Calculate claim status counts
status_counts = {
    row["claim_status"]: int(row["claim_count"])
    for row in records
}

approved = status_counts.get("Approved", 0)
denied = status_counts.get("Denied", 0)
pending = status_counts.get("Pending", 0)

# Step 5: Calculate KPI percentages
def calculate_rate(count, total):
    return (count / total * 100) if total else 0

approval_rate = calculate_rate(approved, total_claims)
denial_rate = calculate_rate(denied, total_claims)
pending_rate = calculate_rate(pending, total_claims)

# Step 6: Display KPI dashboard
print("\n===== HEALTHCARE CLAIMS KPI DASHBOARD =====")
print(f"Total Claims: {total_claims}")
print(f"Total Claimed Amount: ${total_amount:,.2f}")
print(f"Approved Claims: {approved}")
print(f"Denied Claims: {denied}")
print(f"Pending Claims: {pending}")
print(f"Approval Rate: {approval_rate:.2f}%")
print(f"Denial Rate: {denial_rate:.2f}%")
print(f"Pending Rate: {pending_rate:.2f}%")
print("==========================================")
