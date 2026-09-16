import os
import sys
import duckdb

DB_PATH = os.path.join("data", "fpl.duckdb")
SQL_FILE_PATH = os.path.join("sql", "02_star_schema.sql")


def run_transformations(db_path: str = DB_PATH, sql_path: str = SQL_FILE_PATH) -> None:
    """Reads and executes SQL transformations to build the Star Schema."""
    if not os.path.exists(sql_path):
        raise FileNotFoundError(f"SQL file not found at: {sql_path}")

    print(f"Connecting to DuckDB database: {db_path}")
    con = duckdb.connect(db_path)

    try:
        with open(sql_path, "r", encoding="utf-8") as f:
            sql_script = f.read()

        print(f"Executing transformations from {sql_path}...")
        con.execute(sql_script)

        # Inspect resulting database tables
        tables = con.execute("SHOW TABLES").fetchall()
        print("\nPipeline execution complete. Active tables in DuckDB:")
        for t in tables:
            count = con.execute(f"SELECT COUNT(*) FROM {t[0]}").fetchone()[0]
            print(f" - {t[0]:<25} ({count} rows)")

    except Exception as e:
        print(f"Error during SQL transformation: {e}", file=sys.stderr)
        raise
    finally:
        con.close()


if __name__ == "__main__":
    run_transformations()