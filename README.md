# FPL Analytics ELT Pipeline

A complete Extract-Transform-Load (ETL) pipeline for Fantasy Premier League (FPL) analytics, built with Python and DuckDB.

## 📋 Project Overview

This project implements an automated data pipeline to extract FPL data, load it into a staging area, transform it into a star schema, and perform data quality checks. It's designed to support analytics and business intelligence workloads for Fantasy Premier League data.

### Architecture

```
Extract → Load → Transform → Data Quality Checks
   ↓        ↓         ↓              ↓
  API    Staging   Star Schema    Validation
```

## 🚀 Features

- **Extract**: Fetch raw FPL data from external APIs
- **Load**: Stage raw data into DuckDB for processing
- **Transform**: Convert staging data into dimensional star schema
- **Quality Assurance**: Automated data quality checks and assertions
- **Logging**: Comprehensive pipeline execution tracking

## 📦 Tech Stack

- **Python 3.x** - Core programming language
- **DuckDB** - Lightweight SQL database engine
- **Pandas** - Data manipulation and analysis
- **Requests** - HTTP client for API calls
- **Python-dotenv** - Environment variable management

### Dependencies

```
certifi==2026.7.22
charset-normalizer==3.5.1
duckdb==1.5.5
idna==3.19
numpy==2.1.3
pandas==3.0.5
python-dateutil==2.9.0.post0
python-dotenv==1.2.3
requests==2.34.2
six==1.17.0
tzdata==2026.4
urllib3==2.7.0
```

## 📂 Project Structure

```
fpl-analytics-elt/
├── main.py                      # Pipeline orchestration entry point
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore configuration
├── .env.example                 # Example environment variables
├── README.md                    # This file
│
├── src/                         # Source code modules
│   ├── __init__.py
│   ├── extract.py              # Data extraction from APIs
│   ├── load.py                 # Data loading to staging
│   ├── transform.py            # Data transformation logic
│   ├── data_quality.py         # Quality assurance checks
│   └── query_analytics.py      # Analytics queries
│
├── sql/                        # SQL scripts
│   ├── 01_raw_staging.sql      # Raw data staging tables
│   └── 02_star_schema.sql      # Dimensional star schema
│
└── data/                       # Data directory
    └── raw/                    # Raw extracted data (not committed)
```

## 🔧 Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Neupane-pradip/fpl-analytics-elt.git
   cd fpl-analytics-elt
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## ▶️ Running the Pipeline

Execute the complete ELT pipeline:

```bash
python main.py
```

### Pipeline Execution Flow

The pipeline runs sequentially through 4 stages:

1. **Extract** - Retrieves raw FPL data
2. **Load** - Stages data into DuckDB
3. **Transform** - Builds star schema for analytics
4. **Data Quality** - Validates data integrity and completeness

## 📊 Data Model

### Star Schema

The pipeline transforms raw data into a star schema consisting of:

- **Fact Tables**: Central tables containing measurable events
- **Dimension Tables**: Reference data for analysis (players, teams, gameweeks, etc.)

SQL definitions are located in `sql/02_star_schema.sql`

## 🔍 Core Modules

### `extract.py`
Handles data extraction from FPL APIs and external sources.

### `load.py`
Manages data loading from extraction to staging tables in DuckDB.

### `transform.py`
Implements SQL-based transformations from staging to star schema.

### `data_quality.py`
Runs validation checks ensuring data integrity:
- Completeness checks
- Consistency validations
- Referential integrity
- Business rule validation

### `query_analytics.py`
Contains pre-built analytics queries for common reports and insights.

## 📝 Configuration

Create a `.env` file based on `.env.example`:

```env
# API Configuration
FPL_API_BASE_URL=https://fantasy.premierleague.com/api/

# Database Configuration
DATABASE_PATH=./data/fpl_analytics.duckdb
STAGING_SCHEMA=staging
ANALYTICS_SCHEMA=analytics

# Logging
LOG_LEVEL=INFO
```

## 🧪 Data Quality Checks

The pipeline includes automated validations:

```python
# Examples of checks performed:
- NULL value validation
- Duplicate detection
- Referential integrity
- Business logic assertions
- Completeness metrics
```

## 📈 Performance

- Lightweight footprint using DuckDB
- Efficient processing with Pandas
- Optimized SQL transformations
- Typical execution time: < 1 minute

## 🐛 Troubleshooting

### Pipeline Fails During Extract
- Verify FPL API is accessible
- Check internet connection
- Ensure `.env` configuration is correct

### Database Errors
- Verify `data/` directory exists with write permissions
- Check DuckDB database file isn't locked
- Clear `data/raw/` for fresh extraction

### Data Quality Failures
- Review quality check assertions in `src/data_quality.py`
- Verify source data quality from FPL API
- Check transformation logic in `sql/02_star_schema.sql`

## 📚 Additional Resources

- [FPL Official API Documentation](https://fantasy.premierleague.com/api/)
- [DuckDB Documentation](https://duckdb.org/docs/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

[Neupane-pradip](https://github.com/Neupane-pradip)

## 📞 Support

For issues and questions:
- Open an issue on [GitHub Issues](https://github.com/Neupane-pradip/fpl-analytics-elt/issues)
- Review existing documentation and troubleshooting section

---

**Last Updated**: September 2026
