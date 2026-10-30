
# Healthcare Claims Data Engineering Pipeline

## Project Overview

An end-to-end healthcare claims data engineering portfolio project that demonstrates data ingestion, validation, transformation, and business reporting using a Medallion Architecture.

The project uses synthetic healthcare claims data and currently runs locally using Python and CSV files.

## Architecture

Synthetic Claims Data
        |
        v
Bronze Layer (Raw Data + Metadata)
        |
        v
Data Quality Validation
        |
        v
Silver Layer (Cleaned Data)
        |
        v
Gold Layer (Aggregated Claims)
        |
        v
Healthcare KPI Reporting

## Technologies

- Python 3
- CSV Processing
- Git and GitHub
- Visual Studio Code
- Medallion Architecture

### Planned Enhancements

- PySpark and Spark SQL
- Azure Databricks
- Delta Lake
- Incremental Processing
- Automated Testing
- Azure Data Factory Orchestration

## Project Structure

```text
healthcare_claims/
├── data/
│   ├── claims.csv
│   ├── bronze/
│   │   └── claims_bronze.csv
│   ├── silver/
│   │   └── claims_silver.csv
│   └── gold/
│       └── claims_summary.csv
├── generate_claims.py
├── bronze_ingestion.py
├── validate_claims.py
├── silver_transformation.py
├── gold_transformation.py
└── healthcare_kpis.py
```

## Pipeline Features

### Bronze Layer
- Ingests synthetic healthcare claims.
- Preserves source records.
- Adds ingestion timestamps and source filenames.

### Data Validation
- Checks missing values.
- Identifies duplicate claim IDs.
- Detects invalid claim amounts.
- Validates claim statuses.

### Silver Layer
- Standardizes service dates.
- Normalizes claim statuses.
- Validates claim amounts.
- Removes duplicate claims.
- Produces cleaned records.

### Gold Layer
- Aggregates claims by status.
- Calculates claim counts and total claimed amounts.
- Generates reporting-ready CSV output.

### KPI Reporting
- Total claims
- Total claimed amount
- Approved claims and approval rate
- Denied claims and denial rate
- Pending claims and pending rate

## How to Run

From the repository root:

```powershell
python healthcare_claims/generate_claims.py
python healthcare_claims/bronze_ingestion.py
python healthcare_claims/validate_claims.py
python healthcare_claims/silver_transformation.py
python healthcare_claims/gold_transformation.py
python healthcare_claims/healthcare_kpis.py
```

## Sample Execution Results

The initial dataset contains 1,000 synthetic healthcare claims.

- Bronze records: 1,000
- Silver records: 1,000
- Rejected records: 0

KPI values are calculated dynamically from the generated data.

## Data Privacy

This project uses synthetic data only.

No real patient information, protected health information (PHI), or medical records are included.

This is a portfolio demonstration, not a HIPAA-certified production system.

## Future Roadmap

1. Convert local Python transformations to PySpark.
2. Implement Delta Lake Bronze, Silver, and Gold tables.
3. Add schema enforcement and data quality tests.
4. Introduce incremental ingestion.
5. Build Azure Data Factory orchestration.
6. Create healthcare analytics dashboards.

## Purpose

Demonstrate practical data engineering skills applicable to healthcare claims processing, data quality, ETL pipelines, and analytics.
