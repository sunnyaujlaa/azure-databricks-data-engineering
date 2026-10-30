
from pyspark.sql import SparkSession
from pathlib import Path

# Step 1: Start Apache Spark
spark = (
    SparkSession.builder
    .master("local[*]")
    .appName("HealthcareClaimsPipeline")
    .getOrCreate()
)

# Step 2: Find our Silver data
base_dir = Path(__file__).resolve().parent
silver_file = base_dir / "data" / "silver" / "claims_silver.csv"

# Step 3: Load CSV into a Spark DataFrame
df = spark.read.csv(
    str(silver_file),
    header=True,
    inferSchema=True
)

# Step 4: Display the first 5 claims
df.show(5, truncate=False)

# Step 5: Count all claims
print(f"Total healthcare claims: {df.count()}")

# Step 6: Stop Spark
spark.stop()
