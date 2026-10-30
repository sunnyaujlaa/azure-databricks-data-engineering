
from pathlib import Path
from pyspark.sql import SparkSession

# Step 1: Start Spark
spark = (
    SparkSession.builder
    .master("local[*]")
    .appName("HealthcareSparkSQL")
    .getOrCreate()
)

# Step 2: Read Silver healthcare claims
base_dir = Path(__file__).resolve().parent
silver_file = base_dir / "data" / "silver" / "claims_silver.csv"

df = spark.read.csv(
    str(silver_file),
    header=True,
    inferSchema=True
)

# Step 3: Create a temporary SQL view
df.createOrReplaceTempView("healthcare_claims")

# Step 4: Run SQL query
result = spark.sql("""
    SELECT
        claim_status,
        COUNT(*) AS total_claims,
        ROUND(SUM(claim_amount), 2) AS total_amount
    FROM healthcare_claims
    GROUP BY claim_status
    ORDER BY claim_status
""")

# Step 5: Display results
print("===== HEALTHCARE SPARK SQL SUMMARY =====")
result.show(truncate=False)

# Step 6: Stop Spark
spark.stop()
