import os
import sys
import duckdb

RAW_JSON_PATH = os.path.join("data", "raw", "bootstrap_static.json")
DB_PATH = os.path.join("data", "fpl.duckdb")


def load_raw_json_to_duckdb(json_path: str = RAW_JSON_PATH, db_path: str = DB_PATH) -> None:
    """Loads raw JSON arrays directly into DuckDB staging tables."""
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Raw data file not found at: {json_path}. Run extract.py first.")

    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Convert Windows backslashes to forward slashes to prevent SQL string escape errors
    clean_json_path = json_path.replace("\\", "/")

    print(f"Connecting to DuckDB database at: {db_path}")
    con = duckdb.connect(db_path)

    try:
        print("Ingesting raw JSON into staging tables...")

        # Subquery unnests array to structs; outer query expands struct keys into columns
        con.execute(f"""
            CREATE OR REPLACE TABLE raw_elements AS 
            SELECT elem.* FROM (
                SELECT unnest(elements) AS elem 
                FROM read_json_auto('{clean_json_path}')
            );
        """)

        con.execute(f"""
            CREATE OR REPLACE TABLE raw_teams AS 
            SELECT team.* FROM (
                SELECT unnest(teams) AS team 
                FROM read_json_auto('{clean_json_path}')
            );
        """)

        con.execute(f"""
            CREATE OR REPLACE TABLE raw_events AS 
            SELECT event.* FROM (
                SELECT unnest(events) AS event 
                FROM read_json_auto('{clean_json_path}')
            );
        """)

        elem_count = con.execute("SELECT COUNT(*) FROM raw_elements").fetchone()[0]
        teams_count = con.execute("SELECT COUNT(*) FROM raw_teams").fetchone()[0]
        events_count = con.execute("SELECT COUNT(*) FROM raw_events").fetchone()[0]

        print("Ingestion complete. Staging table summary:")
        print(f" - raw_elements (players) : {elem_count} rows")
        print(f" - raw_teams    (clubs)   : {teams_count} rows")
        print(f" - raw_events   (gameweeks): {events_count} rows")

    except Exception as e:
        print(f"Error during DuckDB ingestion: {e}", file=sys.stderr)
        raise
    finally:
        con.close()


def main():
    load_raw_json_to_duckdb()


if __name__ == "__main__":
    main()