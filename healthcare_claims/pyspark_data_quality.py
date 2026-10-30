
from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, count, when

# Step 1: Start Spark
spark = (
    SparkSession.builder
    .master("local[*]")
    .appName("HealthcareDataQuality")
    .getOrCreate()
)

# Step 2: Read Bronze claims
base_dir = Path(__file__).resolve().parent
bronze_file = base_dir / "data" / "bronze" / "claims_bronze.csv"

df = spark.read.csv(
    str(bronze_file),
    header=True,
    inferSchema=True
)

print("===== HEALTHCARE DATA QUALITY REPORT =====")

# Step 3: Count all records
total_records = df.count()
print(f"Total records: {total_records}")

# Step 4: Find missing claim IDs
missing_ids = df.filter(
    col("claim_id").isNull() |
    (trim(col("claim_id")) == "")
).count()

print(f"Missing claim IDs: {missing_ids}")

# Step 5: Find duplicate claim IDs
duplicate_ids = (
    df.groupBy("claim_id")
    .agg(count("*").alias("record_count"))
    .filter(col("record_count") > 1)
    .count()
)

print(f"Duplicate claim ID groups: {duplicate_ids}")

# Step 6: Find invalid claim amounts
invalid_amounts = df.filter(
    col("claim_amount").isNull() |
    col("claim_amount").cast("double").isNull() |
    col("claim_amount").cast("double").isNaN() |
    (col("claim_amount").cast("double") <= 0)
).count()

print(f"Invalid claim amounts: {invalid_amounts}")

# Step 7: Find invalid statuses
valid_statuses = ["Approved", "Denied", "Pending"]

invalid_statuses = df.filter(
    col("claim_status").isNull() |
    (~col("claim_status").isin(valid_statuses))
).count()

print(f"Invalid claim statuses: {invalid_statuses}")

# Step 8: Display quality summary
print("========================================")

if (
    missing_ids == 0
    and duplicate_ids == 0
    and invalid_amounts == 0
    and invalid_statuses == 0
):
    print("DATA QUALITY CHECKS PASSED")
else:
    print("DATA QUALITY ISSUES DETECTED")

# Step 9: Stop Spark
spark.stop()
