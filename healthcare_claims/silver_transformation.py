
import csv
from pathlib import Path
from datetime import datetime
from decimal import Decimal, InvalidOperation

# Step 1: Define file paths
base_dir = Path(__file__).resolve().parent
bronze_file = base_dir / "data" / "bronze" / "claims_bronze.csv"

silver_dir = base_dir / "data" / "silver"
silver_dir.mkdir(parents=True, exist_ok=True)

silver_file = silver_dir / "claims_silver.csv"

# Step 2: Read Bronze claims
with bronze_file.open("r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    claims = list(reader)

# Step 3: Clean and transform claims
clean_claims = []
seen_claim_ids = set()
rejected_count = 0

valid_statuses = {
    "approved": "Approved",
    "pending": "Pending",
    "denied": "Denied"
}

for row in claims:
    claim_id = (row.get("claim_id") or "").strip()

    # Reject missing or duplicate claim IDs
    if not claim_id or claim_id in seen_claim_ids:
        rejected_count += 1
        continue

    try:
        amount = Decimal(row["claim_amount"].strip())
        if not amount.is_finite() or amount <= 0:
            raise ValueError("Invalid claim amount")

        service_date = datetime.strptime(
            row["service_date"].strip(), "%Y-%m-%d"
        ).date().isoformat()

        status = valid_statuses[
            row["claim_status"].strip().lower()
        ]

        # Standardize the claim amount to 2 decimals
        row["claim_amount"] = str(round(amount, 2))
        row["service_date"] = service_date
        row["claim_status"] = status

        clean_claims.append(row)
        seen_claim_ids.add(claim_id)

    except (InvalidOperation, ValueError, KeyError, AttributeError):
        rejected_count += 1

# Step 4: Write Silver claims
if clean_claims:
    with silver_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, fieldnames=clean_claims[0].keys()
        )
        writer.writeheader()
        writer.writerows(clean_claims)

# Step 5: Display results
print(f"Bronze records: {len(claims)}")
print(f"Silver records: {len(clean_claims)}")
print(f"Rejected records: {rejected_count}")
print(f"Silver output: {silver_file}")
