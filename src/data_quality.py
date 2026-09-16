import os
import sys
import duckdb

DB_PATH = os.path.join("data", "fpl.duckdb")


def run_data_quality_checks(db_path: str = DB_PATH) -> None:
    """Runs a suite of SQL data quality assertions against the transformed database."""
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database not found at {db_path}. Run ETL pipeline first.")

    con = duckdb.connect(db_path)
    print(f"Connecting to DuckDB for quality validation: {db_path}\n")

    # Defined as tuple: (Test Name, SQL Query to find violations, Expected Violation Count)
    dq_suite = [
        # 1. Uniqueness / Primary Key Integrity
        (
            "Primary Key Uniqueness - dim_player",
            "SELECT player_id, COUNT(*) FROM dim_player GROUP BY player_id HAVING COUNT(*) > 1;",
            0
        ),
        (
            "Primary Key Uniqueness - dim_team",
            "SELECT team_id, COUNT(*) FROM dim_team GROUP BY team_id HAVING COUNT(*) > 1;",
            0
        ),

        # 2. NOT NULL Checks
        (
            "NOT NULL Check - dim_player.full_name",
            "SELECT * FROM dim_player WHERE full_name IS NULL OR full_name = '';",
            0
        ),
        (
            "NOT NULL Check - fact_player_season_stat.total_points",
            "SELECT * FROM fact_player_season_stat WHERE total_points IS NULL;",
            0
        ),

        # 3. Referential Integrity (Foreign Keys)
        (
            "Referential Integrity - Orphaned team_id in fact table",
            """
            SELECT f.player_id, f.team_id 
            FROM fact_player_season_stat f 
            LEFT JOIN dim_team t ON f.team_id = t.team_id 
            WHERE t.team_id IS NULL;
            """,
            0
        ),

        # 4. Range & Value Validity
        (
            "Reasonability Range - Positive player pricing",
            "SELECT * FROM fact_player_season_stat WHERE price_millions <= 0 OR price_millions > 30.0;",
            0
        ),
        (
            "Reasonability Range - Non-negative minutes played",
            "SELECT * FROM fact_player_season_stat WHERE minutes_played < 0;",
            0
        )
    ]

    failed_tests = 0

    for test_name, sql, expected_violations in dq_suite:
        violating_rows = con.execute(sql).fetchall()
        actual_violations = len(violating_rows)

        if actual_violations != expected_violations:
            print(f"❌ FAIL: {test_name}")
            print(f"    Expected {expected_violations} violations, found {actual_violations}.", file=sys.stderr)
            failed_tests += 1
        else:
            print(f"✅ PASS: {test_name}")

    con.close()

    if failed_tests > 0:
        raise ValueError(f"Pipeline halted: {failed_tests} data quality assertion(s) failed!")

    print("\n🎉 All Data Quality Assertions Passed!")


if __name__ == "__main__":
    run_data_quality_checks()