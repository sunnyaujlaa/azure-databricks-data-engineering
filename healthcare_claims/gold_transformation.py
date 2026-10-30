
import csv
from pathlib import Path
from collections import defaultdict
from decimal import Decimal

# Step 1: Define input and output paths
base_dir = Path(__file__).resolve().parent

silver_file = base_dir / "data" / "silver" / "claims_silver.csv"
gold_dir = base_dir / "data" / "gold"
gold_dir.mkdir(parents=True, exist_ok=True)

gold_file = gold_dir / "claims_summary.csv"

# Step 2: Read clean Silver claims
with silver_file.open("r", newline="", encoding="utf-8") as file:
    claims = list(csv.DictReader(file))

# Step 3: Aggregate claims by status
summary = defaultdict(
    lambda: {"count": 0, "total_amount": Decimal("0.00")}
)

for claim in claims:
    status = claim["claim_status"]
    amount = Decimal(claim["claim_amount"])

    summary[status]["count"] += 1
    summary[status]["total_amount"] += amount

# Step 4: Calculate total claims
total_claims = len(claims)

# Step 5: Save Gold analytics output
with gold_file.open("w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "claim_status",
        "claim_count",
        "total_claim_amount",
        "percentage"
    ])

    for status in sorted(summary):
        values = summary[status]

        percentage = (
            values["count"] / total_claims * 100
            if total_claims else 0
        )

        writer.writerow([
            status,
            values["count"],
            f'{values["total_amount"]:.2f}',
            f"{percentage:.2f}"
        ])

# Step 6: Display results
print(f"Total claims processed: {total_claims}")
print("Gold layer summary:")

for status in sorted(summary):
    values = summary[status]
    print(
        f'{status}: {values["count"]} claims, '
        f'${values["total_amount"]:.2f}'
    )

print(f"Gold output: {gold_file}")
