-- ============================================================================
-- 1. DIMENSION TABLES
-- ============================================================================

-- Dimension: Teams / Clubs
CREATE OR REPLACE TABLE dim_team AS
SELECT
    id AS team_id,
    name AS team_name,
    short_name,
    code AS team_code,
    strength AS strength_overall
FROM raw_teams;

-- Dimension: Gameweeks / Events
CREATE OR REPLACE TABLE dim_gameweek AS
SELECT
    id AS gameweek_id,
    name AS gameweek_name,
    CAST(deadline_time AS TIMESTAMP) AS deadline_time,
    finished AS is_finished,
    is_current,
    is_next
FROM raw_events;

-- Dimension: Players
CREATE OR REPLACE TABLE dim_player AS
SELECT
    id AS player_id,
    first_name || ' ' || second_name AS full_name,
    web_name,
    team AS team_id,
    element_type AS position_id,
    CASE element_type
        WHEN 1 THEN 'GKP'
        WHEN 2 THEN 'DEF'
        WHEN 3 THEN 'MID'
        WHEN 4 THEN 'FWD'
        ELSE 'UNK'
    END AS position_code
FROM raw_elements;

-- ============================================================================
-- 2. FACT TABLE
-- ============================================================================

-- Fact: Player Season Stats (Cumulative Performance metrics)
CREATE OR REPLACE TABLE fact_player_season_stat AS
SELECT
    id AS player_id,
    team AS team_id,
    minutes AS minutes_played,
    goals_scored,
    assists,
    clean_sheets,
    goals_conceded,
    yellow_cards,
    red_cards,
    -- Type casting string/JSON values to explicitly typed numeric floats
    CAST(expected_goals AS DOUBLE) AS expected_goals,
    CAST(expected_assists AS DOUBLE) AS expected_assists,
    CAST(expected_goal_involvements AS DOUBLE) AS expected_goal_involvements,
    total_points,
    -- FPL prices are stored as integers multiplied by 10 (e.g., 125 = £12.5m)
    CAST(now_cost AS DOUBLE) / 10.0 AS price_millions,
    CAST(selected_by_percent AS DOUBLE) AS ownership_percent
FROM raw_elements;