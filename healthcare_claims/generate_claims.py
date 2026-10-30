
import csv
import random
from datetime import date, timedelta
from pathlib import Path

# Synthetic healthcare insurance claims
# No real patient or protected health information

random.seed(42)

output_dir = Path(__file__).resolve().parent / "data"
output_dir.mkdir(exist_ok=True)

output_file = output_dir / "claims.csv"

diagnosis_codes = [
    "I10",     # Hypertension
    "E11.9",   # Type 2 diabetes
    "J06.9",   # Upper respiratory infection
    "M54.50",  # Low back pain
    "E78.5"    # Hyperlipidemia
]

claim_statuses = ["Approved", "Pending", "Denied"]

with output_file.open("w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "claim_id",
        "member_id",
        "provider_id",
        "service_date",
        "diagnosis_code",
        "claim_amount",
        "claim_status"
    ])

    for i in range(1, 1001):
        writer.writerow([
            f"CLM{i:06d}",
            f"MEM{random.randint(1, 300):04d}",
            f"PRV{random.randint(1, 50):03d}",
            (date(2026, 1, 1) +
             timedelta(days=random.randint(0, 298))).isoformat(),
            random.choice(diagnosis_codes),
            round(random.uniform(75, 5000), 2),
            random.choices(
                claim_statuses,
                weights=[75, 15, 10]
            )[0]
        ])

print(f"Successfully generated 1,000 synthetic claims: {output_file}")
