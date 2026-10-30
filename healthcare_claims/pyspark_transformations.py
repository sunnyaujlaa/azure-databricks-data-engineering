
from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, sum as spark_sum

# Step 1: Start Spark
spark = (
    SparkSession.builder
    .master("local[*]")
    .appName("HealthcareClaimsTransformations")
    .getOrCreate()
)

# Step 2: Read Silver claims
base_dir = Path(__file__).resolve().parent
silver_file = base_dir / "data" / "silver" / "claims_silver.csv"

df = spark.read.csv(
    str(silver_file),
    header=True,
    inferSchema=True
)

# Step 3: Filter approved claims
approved_df = df.filter(col("claim_status") == "Approved")

print("===== APPROVED CLAIMS =====")
approved_df.show(5)
print(f"Approved claims: {approved_df.count()}")

# Step 4: Filter denied claims
denied_df = df.filter(col("claim_status") == "Denied")

print("===== DENIED CLAIMS =====")
denied_df.show(5)
print(f"Denied claims: {denied_df.count()}")

# Step 5: Group claims by status
print("===== CLAIMS SUMMARY =====")

summary_df = (
    df.groupBy("claim_status")
    .agg(
        count("*").alias("total_claims"),
        spark_sum("claim_amount").alias("total_amount")
    )
    .orderBy("claim_status")
)

summary_df.show(truncate=False)

# Step 6: Stop Spark
spark.stop()
