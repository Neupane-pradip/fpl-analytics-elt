import os
import duckdb
import pandas as pd

DB_PATH = os.path.join("data", "fpl.duckdb")


def run_sample_queries():
    con = duckdb.connect(DB_PATH)

    print("=== TOP 5 PLAYERS BY EXPECTED GOALS (xG) ===")
    query_xg = """
               SELECT
                   p.full_name,
                   t.short_name AS team,
                   p.position_code,
                   f.price_millions,
                   f.goals_scored,
                   f.expected_goals
               FROM fact_player_season_stat f
                        JOIN dim_player p ON f.player_id = p.player_id
                        JOIN dim_team t ON f.team_id = t.team_id
               ORDER BY f.expected_goals DESC
                   LIMIT 5; \
               """
    df_xg = con.execute(query_xg).df()
    print(df_xg.to_string(index=False))

    print("\n=== TOP 5 VALUE ASSETS (POINTS PER £ MILLION) ===")
    query_value = """
                  SELECT
                      p.full_name,
                      t.short_name AS team,
                      f.price_millions,
                      f.total_points,
                      ROUND(f.total_points / f.price_millions, 2) AS points_per_million
                  FROM fact_player_season_stat f
                           JOIN dim_player p ON f.player_id = p.player_id
                           JOIN dim_team t ON f.team_id = t.team_id
                  WHERE f.minutes_played > 450
                  ORDER BY points_per_million DESC
                      LIMIT 5; \
                  """
    df_value = con.execute(query_value).df()
    print(df_value.to_string(index=False))

    con.close()


if __name__ == "__main__":
    run_sample_queries()