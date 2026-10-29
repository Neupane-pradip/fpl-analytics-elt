# FPL Analytics ELT Pipeline

A Python and DuckDB learning project that turns a Fantasy Premier League API snapshot into relational tables for player and team analysis.

```text
FPL bootstrap-static API
  → raw JSON
  → DuckDB raw tables
  → SQL dimensions and season-stat fact table
  → data-quality assertions
```

## What it does

- Downloads the FPL bootstrap-static response with a 10-second request timeout.
- Saves the raw response to `data/raw/bootstrap_static.json`.
- Loads player, team, and gameweek arrays into DuckDB.
- Builds analytics tables with `sql/02_star_schema.sql`.
- Checks keys, required values, team references, prices, and minutes played.
- Provides example queries for expected goals and points per million.

## Setup and run

Use Python 3.11, matching the configured GitHub Actions workflow.

```sh
git clone https://github.com/Neupane-pradip/fpl-analytics-elt.git
cd fpl-analytics-elt
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```sh
# macOS / Linux
source .venv/bin/activate
```

Install dependencies and run from the repository root:

```sh
python -m pip install -r requirements.txt
python main.py
python -m src.query_analytics
```

The main pipeline exits with status 1 if a stage raises an exception. Sample analytics queries run separately.

## Tables and outputs

| Artifact | Contents |
|---|---|
| `data/raw/bootstrap_static.json` | Latest downloaded response |
| `data/fpl.duckdb` | Local DuckDB database |
| `raw_elements`, `raw_teams`, `raw_events` | Source arrays expanded into tables |
| `dim_player`, `dim_team`, `dim_gameweek` | Player, team, and gameweek dimensions |
| `fact_player_season_stat` | Cumulative player statistics and current price/ownership |

Raw and analytics tables use `CREATE OR REPLACE TABLE`. Each run refreshes the latest state; it does not retain historical snapshots or a gameweek-by-player fact table.

The code currently uses module constants for paths and the API URL. No `.env.example` is committed, and the pipeline does not read the environment settings shown in older documentation.

## Data-quality checks

Run checks against an existing transformed database:

```sh
python -m src.data_quality
```

Assertions cover:

- Unique player and team keys.
- Nonempty player names and non-null total points.
- Team references from the fact table.
- Prices greater than zero and at most 30 million.
- Nonnegative minutes played.

These checks raise an error on detected violations. They do not constitute a complete automated test suite.

## Automation

[`scheduled_pipeline.yml`](.github/workflows/scheduled_pipeline.yml) configures a daily run at **06:00 UTC** and a manual Actions trigger.

The workflow installs dependencies, runs the pipeline, and attempts to upload `data/fpl.duckdb` as an artifact retained for seven days. Each hosted runner starts with a fresh checkout; the database artifact is the downloadable result, not persistent shared storage.

A failure-notification step references the repository secret `SLACK_WEBHOOK_URL`. Notifications require that secret and a working webhook. This README does not assert that a scheduled run or notification has succeeded.

## Project files

| File | Responsibility |
|---|---|
| `main.py` | Four-stage pipeline orchestration |
| `src/extract.py` | HTTP extraction and raw JSON persistence |
| `src/load.py` | Raw-table loading |
| `src/transform.py` | Execute SQL transformations |
| `src/data_quality.py` | SQL assertions |
| `src/query_analytics.py` | Example analysis queries |
| `sql/02_star_schema.sql` | Dimension and fact definitions |

## Limitations

The pipeline depends on the external API's availability and response schema. It has no extraction retry loop, incremental loading, historical retention, or transaction spanning every stage. A failed run can leave partially refreshed outputs. This is an independent learning project, not an official Fantasy Premier League service.
