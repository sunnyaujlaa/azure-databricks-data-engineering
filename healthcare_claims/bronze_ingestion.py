
from pathlib import Path
from datetime import datetime, timezone
import csv

# Step 1: Locate the source CSV
base_dir = Path(__file__).resolve().parent
source_file = base_dir / "data" / "claims.csv"

# Step 2: Create the Bronze folder
bronze_dir = base_dir / "data" / "bronze"
bronze_dir.mkdir(parents=True, exist_ok=True)

# Step 3: Define the output file
output_file = bronze_dir / "claims_bronze.csv"

# Step 4: Read raw claims and add ingestion metadata
with source_file.open("r", newline="", encoding="utf-8") as source:
    reader = csv.DictReader(source)
    fieldnames = reader.fieldnames + ["ingestion_timestamp", "source_file"]

    with output_file.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        count = 0
        for row in reader:
            row["ingestion_timestamp"] = datetime.now(timezone.utc).isoformat()
            row["source_file"] = source_file.name
            writer.writerow(row)
            count += 1

print(f"Bronze ingestion completed: {count} records")
print(f"Output: {output_file}")
