# Data Engineering Project: Financial Data Pipeline

## Project Overview

This project is a beginner-friendly ETL (Extract, Transform, Load) pipeline that automates the process of extracting financial data from PDF reports, cleaning and transforming it, and loading it into a PostgreSQL database.

Use Case: Extracting bank financial statements from PDF files and storing them in a structured database for analysis.

---

## Project Idea

The pipeline solves a common data engineering challenge: unstructured data in PDFs into structured data in a database.

1. Extract: Automatically scan PDF files and extract tables and metadata
2. Transform: Clean column names, normalize numeric values, and create proper date formats
3. Load: Insert clean data into a database while avoiding duplicates

This follows the industry-standard ETL pattern used by data engineers daily.

---

## Project Structure

```
finance-docs-etl/
├── data/
│   ├── downloads/          # Input PDFs go here
│   ├── extracted_data.json # Raw extracted data 
│   └── transform_data.csv  # Cleaned data
├── src/
│   ├── etl.py              # Main pipeline orchestrator
│   ├── extract.py          # Extract tables and metadata from PDFs
│   ├── transform.py        # Clean and transform data
│   ├── load_data.py        # Load data to Supabase database
│   ├── supabase_client.py  # Database connection
│   ├── clean_columns.py    # Clean column names
│   ├── clean_numeric.py    # Clean numeric values
│   ├── handling_date.py    # Create and format dates
│   └── .env                # Environment variables (Supabase Key)
├── pyproject.toml          # Python dependencies
├── .python-version         # Python version
└── README.md               # This file
```

---

## Technology Stack

| Package | Purpose |
|---------|---------|
| pandas | Data manipulation and CSV handling |
| Camelot | Extract tables from PDF files |
| pdfplumber | Extract text and metadata from PDFs |
| Supabase | PostgreSQL database (cloud) |
| python-dotenv | Environment variable management |

---

## Setup

Install dependencies:
```bash
pip install -r pyproject.toml
```

Create `.env` file with Supabase credentials:
```bash
echo "SUPABASE_URL=your_url" > src/.env
echo "SUPABASE_KEY=your_key" >> src/.env
```

---

## How to Run

### Dry Run (Extract and Transform only, no database insert)

```bash
python src/etl.py
# Then modify the last line in etl.py to:
# run_pipeline(skip_load=True)
```

Or test individual stages:

```bash
python -c "from extract import extract; extract()"
python -c "from transform import transform; transform()"
```

### Full Pipeline (Extract, Transform, and Load)

```bash
python src/etl.py
```

This runs all three stages in sequence and loads data to Supabase.

---

## Data Flow

Extract Stage
- Scans data/downloads/ for PDF files
- Uses Camelot to extract financial tables
- Uses pdfplumber to extract company name and dates
- Output: data/extracted_data.json

Transform Stage
- Cleans column names (spaces, special characters)
- Converts numeric values (removes formatting, handles decimals)
- Creates standardized report_date field
- Removes unnecessary columns
- Output: data/transform_data.csv

Load Stage
- Reads cleaned CSV
- Connects to Supabase PostgreSQL database
- Converts data types (dates, integers)
- Checks for duplicates before inserting
- Skips records that already exist (idempotent)

---

## Next Steps

- Add more data source (bank)
- Implement data validation (schema checking)
- Serving data to Looker Studio dashboard/API