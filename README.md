# FPL Analytics ELT Pipeline

A beginner-friendly data pipeline for collecting and analyzing Fantasy Premier League data using Python and DuckDB.

## What This Project Does

The pipeline:

1. Extracts data from the FPL API
2. Loads the data into DuckDB
3. Transforms the data into tables for analysis
4. Runs basic data quality checks

```text
FPL API → Extract → Load → Transform → Quality Checks
```

## Tools Used

- Python
- DuckDB
- Pandas
- Requests
- Python-dotenv

## Project Structure

```text
fpl-analytics-elt/
├── main.py                  # Runs the complete pipeline
├── requirements.txt         # Project dependencies
├── .env.example             # Example configuration file
├── src/
│   ├── extract.py           # Gets data from the FPL API
│   ├── load.py              # Loads data into DuckDB
│   ├── transform.py         # Transforms the data
│   ├── data_quality.py      # Checks data quality
│   └── query_analytics.py   # Runs analytics queries
├── sql/
│   ├── 01_raw_staging.sql   # Staging table definitions
│   └── 02_star_schema.sql   # Analytics table definitions
└── data/                    # Stores local data files
```

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Neupane-pradip/fpl-analytics-elt.git
cd fpl-analytics-elt
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

On Windows:

```bash
venv\\Scripts\\activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the environment file

```bash
cp .env.example .env
```

Update the `.env` file if needed.

### 5. Run the pipeline

```bash
python main.py
```

## Configuration

The project uses the following settings in the `.env` file:

```env
FPL_API_BASE_URL=https://fantasy.premierleague.com/api/
DATABASE_PATH=./data/fpl_analytics.duckdb
STAGING_SCHEMA=staging
ANALYTICS_SCHEMA=analytics
LOG_LEVEL=INFO
```

## Notes

- The pipeline creates a DuckDB database inside the `data/` folder.
- Raw data is stored locally and is not committed to the repository.
- Make sure you have Python 3.8 or newer installed.
